from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from pathlib import Path
from tempfile import mkdtemp
import subprocess
from typing import Sequence

AVAILABLE_PROVIDERS = {"agy", "codex", "claude_code", "opencode"}


@dataclass(slots=True)
class RunSpec:
    provider: str
    model: str
    prompt: str
    instructions: str | None
    timeout_seconds: float
    workspace_dir: Path | None = None
    command: Sequence[str] | None = None


@dataclass(slots=True)
class RunResult:
    stdout: str
    stderr: str
    returncode: int
    workspace: Path
    command: tuple[str, ...]
    raw: object | None = None
    timed_out: bool = False
    duration_seconds: float | None = None


def _make_workspace(base_dir: Path | None) -> Path:
    if base_dir is None:
        return Path(mkdtemp(prefix="ohmni-harness-"))
    base_dir.mkdir(parents=True, exist_ok=True)
    return Path(mkdtemp(prefix="run-", dir=str(base_dir)))


def run_spec(spec: RunSpec) -> RunResult:
    workspace = _make_workspace(spec.workspace_dir)
    prompt_file = workspace / "prompt.txt"
    prompt_file.write_text(spec.prompt, encoding="utf-8")
    instructions_file = workspace / "instructions.txt"
    instructions_file.write_text(spec.instructions or "", encoding="utf-8")
    command = tuple(spec.command or (spec.provider, "run", spec.model, str(prompt_file)))
    start = perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=str(workspace),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=spec.timeout_seconds,
            shell=False,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        return RunResult(
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            returncode=124,
            workspace=workspace,
            command=command,
            raw=None,
            timed_out=True,
            duration_seconds=perf_counter() - start,
        )
    return RunResult(
        stdout=completed.stdout or "",
        stderr=completed.stderr or "",
        returncode=completed.returncode,
        workspace=workspace,
        command=command,
        raw=completed.stdout or "",
        timed_out=False,
        duration_seconds=perf_counter() - start,
    )
