from __future__ import annotations

import unittest

from ohmni.model.contracts import FakeModelBackend, ModelRequest, ModelResponse, ModelUsage


class ModelContractTests(unittest.TestCase):
    def test_blank_request_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ModelRequest(prompt=" ")

    def test_fake_backend_records_request(self) -> None:
        seen: list[str] = []

        def callback(request: ModelRequest):
            seen.append(request.prompt)
            return ModelResponse(content="ok", usage=ModelUsage(prompt_tokens=1))

        backend = FakeModelBackend(callback)
        response = backend.invoke(ModelRequest(prompt="hello", system_prompt="sys"))
        self.assertEqual(response.content, "ok")
        self.assertEqual(seen, ["hello"])
        self.assertEqual(len(backend.requests), 1)
        self.assertEqual(backend.requests[0].system_prompt, "sys")

    def test_model_response_serializes(self) -> None:
        response = ModelResponse(content="netlist", usage=ModelUsage(prompt_tokens=1, total_tokens=2), metadata={"a": 1})
        payload = response.to_dict()
        self.assertEqual(payload["content"], "netlist")
        self.assertEqual(payload["usage"]["total_tokens"], 2)
        self.assertEqual(payload["metadata"]["a"], 1)


if __name__ == "__main__":
    unittest.main()
