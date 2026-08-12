from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import asdict, is_dataclass
from typing import Any

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from langchain_core.messages.chat import ChatMessage


_SENSITIVE_KEYS = {"api_key", "apikey", "token", "secret", "password", "authorization", "credentials"}


def _is_text_block_dict(value: dict[str, Any]) -> bool:
    block_type = str(value.get("type", "")).lower()
    if not block_type:
        return "text" in value
    return block_type in {"text", "plain_text", "text_block", "paragraph"}


def _block_to_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, Mapping):
        if _is_text_block_dict(dict(value)):
            if "text" in value:
                return str(value["text"])
            if "content" in value:
                return str(value["content"])
        raise NotImplementedError("Unsupported multimodal/tool content block in LangChain message")
    if hasattr(value, "text"):
        return str(getattr(value, "text"))
    if is_dataclass(value):
        data = asdict(value)
        return _block_to_text(data)
    raise NotImplementedError(f"Unsupported message content block type: {type(value)!r}")


def content_to_text(content: Any) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    if isinstance(content, Sequence) and not isinstance(content, (str, bytes, bytearray)):
        parts = [_block_to_text(block) for block in content]
        if any(part == "" for part in parts) and any(part != "" for part in parts):
            # Let empty blocks pass through without forcing textification.
            parts = [part for part in parts if part]
        text = "".join(parts)
        if not text.strip():
            raise NotImplementedError("Message content contains no text")
        return text
    return _block_to_text(content)


def render_messages_for_harness(messages: Sequence[BaseMessage]) -> tuple[str | None, str]:
    system_parts: list[str] = []
    conversation: list[tuple[str, str]] = []

    for message in messages:
        if isinstance(message, SystemMessage):
            text = content_to_text(message.content).strip()
            if text:
                system_parts.append(text)
            continue
        if isinstance(message, HumanMessage):
            role = "Human"
        elif isinstance(message, AIMessage):
            role = "Assistant"
        elif isinstance(message, ChatMessage):
            role = (message.role or "Chat").strip() or "Chat"
            role = role[:1].upper() + role[1:]
        else:
            raise NotImplementedError(f"Unsupported message type: {type(message).__name__}")

        text = content_to_text(message.content).strip()
        if not text:
            raise NotImplementedError(f"Unsupported empty content for {type(message).__name__}")
        conversation.append((role, text))

    instructions = "\n\n".join(system_parts) if system_parts else None
    if len(conversation) == 1 and conversation[0][0] == "Human":
        prompt = conversation[0][1]
    else:
        prompt = "\n".join(f"{role}: {text}" for role, text in conversation)
    if not prompt.strip():
        raise NotImplementedError("No prompt content could be rendered from the provided messages")
    return instructions, prompt


def extract_assistant_text(raw: Any) -> str:
    if raw is None:
        return ""
    if isinstance(raw, AIMessage):
        return content_to_text(raw.content)
    if isinstance(raw, str):
        return raw
    if isinstance(raw, Mapping):
        for key in ("result", "response", "content", "text", "output", "message"):
            if key in raw:
                try:
                    text = extract_assistant_text(raw[key])
                except NotImplementedError:
                    text = ""
                if text.strip():
                    return text
        return ""
    if isinstance(raw, Sequence) and not isinstance(raw, (str, bytes, bytearray)):
        pieces: list[str] = []
        for item in raw:
            if isinstance(item, str):
                pieces.append(item)
            elif isinstance(item, Mapping):
                try:
                    text = extract_assistant_text(item)
                except NotImplementedError:
                    text = ""
                if text:
                    pieces.append(text)
            elif hasattr(item, "text"):
                pieces.append(str(getattr(item, "text")))
        return "".join(pieces)
    for attr in ("result", "response", "content", "text", "output"):
        if hasattr(raw, attr):
            try:
                text = extract_assistant_text(getattr(raw, attr))
            except NotImplementedError:
                text = ""
            if text.strip():
                return text
    return ""


def usage_from_mapping(value: Any) -> dict[str, int] | None:
    if value is None:
        return None
    if isinstance(value, Mapping):
        prompt_tokens = value.get("input_tokens", value.get("prompt_tokens"))
        completion_tokens = value.get("output_tokens", value.get("completion_tokens"))
        total_tokens = value.get("total_tokens")
        if total_tokens is None and prompt_tokens is not None and completion_tokens is not None:
            total_tokens = int(prompt_tokens) + int(completion_tokens)
        if prompt_tokens is None and completion_tokens is None and total_tokens is None:
            return None
        return {
            "input_tokens": int(prompt_tokens or 0),
            "output_tokens": int(completion_tokens or 0),
            "total_tokens": int(total_tokens or 0),
        }
    if is_dataclass(value):
        return usage_from_mapping(asdict(value))
    attrs = {
        "input_tokens": getattr(value, "input_tokens", None),
        "prompt_tokens": getattr(value, "prompt_tokens", None),
        "output_tokens": getattr(value, "output_tokens", None),
        "completion_tokens": getattr(value, "completion_tokens", None),
        "total_tokens": getattr(value, "total_tokens", None),
    }
    if all(v is None for v in attrs.values()):
        return None
    return usage_from_mapping(attrs)


def sanitize_metadata(value: Any) -> Any:
    if isinstance(value, Mapping):
        sanitized: dict[str, Any] = {}
        for key, item in value.items():
            key_str = str(key)
            if key_str.lower() in _SENSITIVE_KEYS:
                continue
            sanitized[key_str] = sanitize_metadata(item)
        return sanitized
    if isinstance(value, list):
        return [sanitize_metadata(item) for item in value]
    if isinstance(value, tuple):
        return [sanitize_metadata(item) for item in value]
    if is_dataclass(value):
        return sanitize_metadata(asdict(value))
    return value
