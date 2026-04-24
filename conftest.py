"""Pytest configuration: make repo root importable so tests can do
``from scripts.bimodal_compliance import ...`` without setting ``PYTHONPATH``.

Newer pytest versions stopped implicitly inserting the rootdir into
``sys.path``, so without this shim the test modules fail to import the
``scripts`` package on a fresh clone (``ModuleNotFoundError: No module named
'scripts'``).
"""

from __future__ import annotations

import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
