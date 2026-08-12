from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest import mock

from langchain_core.callbacks.manager import CallbackManagerForLLMRun
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import ConfigDict, Field, PrivateAttr

from ohmni._vendor.agent_harness import RunResult
from ohmni.config.settings import Settings
from ohmni.model.backends.factory import build_model_backend
from ohmni.model.backends.harness_backend import HarnessModelBackend
from ohmni.model.backends.langchain_api_backend import LangChainModelBackend
from ohmni.model.contracts import ModelRequest
from ohmni.model.errors import ModelConfigurationError, ModelOutputError, ModelTimeoutError
from ohmni.model.infrastructure.chat_model import HarnessChatModel
from ohmni.model.infrastructure.translation import content_to_text


class DummyChatModel(BaseChatModel):
    response_content: object = Field()
    response_metadata_value: dict[str, object] = Field(default_factory=dict)
    usage_value: dict[str, int] | None = Field(default=None)

    _invocations: list[list[object]] = PrivateAttr(default_factory=list)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def _llm_type(self) -> str:
        return "dummy-chat"

    @property
    def _identifying_params(self) -> dict[str, object]:
        return {"response_content": self.response_content}

    def _generate(
        self,
        messages: list[object],
        stop: list[str] | None = None,
        run_manager: CallbackManagerForLLMRun | None = None,
        **kwargs,
    ) -> ChatResult:
        self._invocations.append(messages)
        message = AIMessage(
            content=self.response_content,
            response_metadata=self.response_metadata_value,
            usage_metadata=self.usage_value,
        )
        return ChatResult(generations=[ChatGeneration(message=message)], llm_output={"ok": True})


class ExplodingChatModel(BaseChatModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    @property
    def _llm_type(self) -> str:
        return "exploding"

    @property
    def _identifying_params(self) -> dict[str, object]:
        return {}

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        raise TimeoutError("boom")


class BackendTests(unittest.TestCase):
    def test_harness_chat_model_translates_messages_and_extracts_result(self) -> None:
        captured = {}

        def fake_run_spec(spec):
            captured["spec"] = spec
            return RunResult(
                stdout="ignored",
                stderr="",
                returncode=0,
                workspace=Path("/tmp/ohmni-harness"),
                command=tuple(spec.command or ()),
                raw={"result": "V1 in 0 5\nR1 in out 1k\n.end\n"},
                timed_out=False,
                duration_seconds=1.25,
            )

        with mock.patch("ohmni.model.infrastructure.chat_model.run_spec", side_effect=fake_run_spec):
            model = HarnessChatModel(provider="agy", model="Gemini 3.6 Flash (Low)", timeout_seconds=5)
            result = model.invoke([SystemMessage(content="You are a netlist generator."), HumanMessage(content="Build an RC filter.")])

        self.assertEqual(result.content.strip(), "V1 in 0 5\nR1 in out 1k\n.end")
        self.assertEqual(model._llm_type, "ohmni-harness")
        self.assertEqual(model._identifying_params["provider"], "agy")
        self.assertEqual(captured["spec"].instructions, "You are a netlist generator.")
        self.assertEqual(captured["spec"].prompt, "Build an RC filter.")

    def test_harness_chat_model_rejects_stop_sequences(self) -> None:
        model = HarnessChatModel(provider="agy", model="Gemini 3.6 Flash (Low)", timeout_seconds=5)
        with self.assertRaises(NotImplementedError):
            model.invoke([HumanMessage(content="hi")], stop=["END"])

    def test_harness_chat_model_rejects_unsupported_tool_messages(self) -> None:
        model = HarnessChatModel(provider="agy", model="Gemini 3.6 Flash (Low)", timeout_seconds=5)
        with self.assertRaises(NotImplementedError):
            model.invoke([HumanMessage(content=[{"type": "image_url", "image_url": "x"}])])

    def test_harness_backend_wraps_chat_model(self) -> None:
        with mock.patch("ohmni.model.infrastructure.chat_model.run_spec") as run_spec:
            run_spec.return_value = RunResult(
                stdout="V1 in 0 5\n.end\n",
                stderr="",
                returncode=0,
                workspace=Path("/tmp/ohmni-harness"),
                command=("agy",),
                raw="V1 in 0 5\n.end\n",
                timed_out=False,
                duration_seconds=0.5,
            )
            backend = HarnessModelBackend(provider="agy", model="Gemini 3.6 Flash (Low)", timeout_seconds=5)
            response = backend.invoke(ModelRequest(prompt="Build an RC filter", system_prompt="Use ngspice"))

        self.assertEqual(response.content.strip(), "V1 in 0 5\n.end")
        self.assertIsInstance(backend.chat_model, HarnessChatModel)

    def test_harness_backend_rejects_invalid_provider(self) -> None:
        with self.assertRaises(ModelConfigurationError):
            HarnessModelBackend(provider="nope", model="m", timeout_seconds=1)

    def test_langchain_backend_maps_messages_response_and_metadata(self) -> None:
        model = DummyChatModel(
            response_content=[{"type": "text", "text": "V1 in 0 5\n.end\n"}],
            response_metadata_value={
                "provider": "dummy",
                "api_key": "secret",
                "nested": {"token": "hidden", "ok": 1},
            },
            usage_value={"input_tokens": 3, "output_tokens": 4, "total_tokens": 7},
        )
        backend = LangChainModelBackend(chat_model=model, backend_name="langchain", provider="dummy", model_name="demo")
        response = backend.invoke(ModelRequest(prompt="Build", system_prompt="System"))

        self.assertEqual(response.content.strip(), "V1 in 0 5\n.end")
        self.assertEqual(response.usage.total_tokens, 7)
        self.assertNotIn("api_key", response.metadata)
        self.assertNotIn("token", str(response.metadata))
        self.assertEqual(model._invocations[0][0].content, "System")
        self.assertEqual(model._invocations[0][1].content, "Build")

    def test_langchain_backend_rejects_non_text_only_content(self) -> None:
        model = DummyChatModel(response_content=[{"type": "image_url", "image_url": "x"}])
        backend = LangChainModelBackend(chat_model=model, backend_name="langchain", provider="dummy", model_name="demo")
        with self.assertRaises(ModelOutputError):
            backend.invoke(ModelRequest(prompt="Build"))

    def test_langchain_backend_maps_timeout(self) -> None:
        backend = LangChainModelBackend(chat_model=ExplodingChatModel(), backend_name="langchain", provider="dummy", model_name="demo")
        with self.assertRaises(ModelTimeoutError):
            backend.invoke(ModelRequest(prompt="Build"))

    def test_gemini_factory_selection_uses_chat_google_generative_ai(self) -> None:
        captured = {}

        class FakeGoogleChatModel(DummyChatModel):
            def __init__(self, **kwargs):
                captured["kwargs"] = kwargs
                super().__init__(response_content="V1 in 0 5\n.end\n")

        settings = Settings.from_env(
            {
                "OHMNI_MODEL_BACKEND": "api",
                "OHMNI_MODEL_PROVIDER": "google",
                "OHMNI_MODEL": "gemini-2.5-flash",
                "GOOGLE_API_KEY": "secret",
                "OHMNI_ENABLE_DOTENV": "0",
            }
        )
        with mock.patch("ohmni.model.backends.factory.ChatGoogleGenerativeAI", FakeGoogleChatModel):
            backend = build_model_backend(settings)

        self.assertIsInstance(backend, LangChainModelBackend)
        self.assertIsInstance(backend.chat_model, DummyChatModel)
        self.assertEqual(captured["kwargs"]["model"], "gemini-2.5-flash")
        self.assertEqual(captured["kwargs"]["vertexai"], False)

    def test_api_google_settings_do_not_require_google_key_for_harness(self) -> None:
        settings = Settings.from_env(
            {
                "OHMNI_MODEL_BACKEND": "harness",
                "OHMNI_MODEL_PROVIDER": "agy",
                "OHMNI_MODEL": "Gemini 3.6 Flash (Low)",
                "OHMNI_ENABLE_DOTENV": "0",
            }
        )
        self.assertEqual(settings.model_provider, "agy")


if __name__ == "__main__":
    unittest.main()
