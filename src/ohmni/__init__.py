from __future__ import annotations

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("ohmni")
except PackageNotFoundError:  # pragma: no cover - local editable checkout
    __version__ = "0.0.0"

