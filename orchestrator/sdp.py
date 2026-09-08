#!/usr/bin/env python3
"""Zero-install checkout launcher for the packaged Core CLI."""

from pathlib import Path
import sys


SOURCE_DIR = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SOURCE_DIR))

from sdp_orchestrator.core.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
