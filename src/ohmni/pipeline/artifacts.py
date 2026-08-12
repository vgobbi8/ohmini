from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
from tempfile import mkdtemp
from typing import Any
from uuid import uuid4


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def make_run_id() -> str:
    return f"{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}-{uuid4().hex[:8]}"


def _atomic_write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    tmp.replace(path)


def _atomic_write_text(path: Path, text: str) -> None:
    _atomic_write_bytes(path, text.encode("utf-8"))


@dataclass(slots=True)
class RunArtifacts:
    root_dir: Path
    run_id: str

    @classmethod
    def create(cls, output_dir: Path, run_id: str | None = None) -> "RunArtifacts":
        run_id = run_id or make_run_id()
        root_dir = Path(output_dir) / run_id
        root_dir.mkdir(parents=True, exist_ok=False)
        return cls(root_dir=root_dir, run_id=run_id)

    def relpath(self, path: Path) -> str:
        return str(path.relative_to(self.root_dir))

    def write_text(self, relative_path: str, content: str) -> Path:
        path = self.root_dir / relative_path
        _atomic_write_text(path, content)
        return path

    def write_json(self, relative_path: str, payload: Any) -> Path:
        text = json.dumps(payload, indent=2, sort_keys=True, default=str)
        return self.write_text(relative_path, text + "\n")

    def path(self, relative_path: str) -> Path:
        return self.root_dir / relative_path

    def ensure_dir(self, relative_path: str) -> Path:
        path = self.root_dir / relative_path
        path.mkdir(parents=True, exist_ok=True)
        return path
