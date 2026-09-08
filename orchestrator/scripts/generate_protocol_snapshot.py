#!/usr/bin/env python3
"""Regenerate the packaged, version-bound Protocol snapshot from canonical source.

The packaged resources are *derivatives*, never an independently edited prompt
authority. This script is the only writer, and
``tests/test_snapshot_parity.py`` proves the committed resources are exactly what
it produces from ``source/shared/references/development-workflow-prompts.md``.

Usage:  python orchestrator/scripts/generate_protocol_snapshot.py [--check]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SRC = REPO_ROOT / "orchestrator" / "packages" / "core" / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from sdp_orchestrator.core import _profile as P  # noqa: E402
from sdp_orchestrator.core._canonical import parse_document  # noqa: E402
from sdp_orchestrator.core._protocolsrc import (  # noqa: E402
    CANONICAL_PROMPTS_RELPATH,
    CANONICAL_VERSION_RELPATH,
    PACKAGED_PROFILE,
    PACKAGED_PROMPTS,
)

TARGET_DIR = (
    PACKAGE_SRC / "sdp_orchestrator" / "core" / "resources" / "protocol" / P.PROFILE_ID
)


def render() -> dict[str, str]:
    declared_version = (REPO_ROOT / CANONICAL_VERSION_RELPATH).read_text(
        encoding="utf-8"
    ).strip()
    if declared_version != P.PROFILE_PROTOCOL_VERSION:
        raise ValueError(
            "canonical source Protocol version does not match the packaged profile: "
            f"{declared_version!r} != {P.PROFILE_PROTOCOL_VERSION!r}"
        )
    prompts = (REPO_ROOT / CANONICAL_PROMPTS_RELPATH).read_text(encoding="utf-8")
    document = parse_document(prompts)
    snapshot = P.build_profile(document)
    return {
        PACKAGED_PROMPTS: prompts,
        PACKAGED_PROFILE: P.profile_to_json(snapshot.descriptor),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify the committed snapshot matches canonical source without writing",
    )
    args = parser.parse_args()

    try:
        expected = render()
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"snapshot generation failed: {exc}", file=sys.stderr)
        return 1
    if args.check:
        drift = []
        for name, text in expected.items():
            path = TARGET_DIR / name
            if not path.is_file() or path.read_text(encoding="utf-8") != text:
                drift.append(name)
        if drift:
            print(f"packaged snapshot is stale: {', '.join(drift)}", file=sys.stderr)
            return 1
        print("packaged snapshot matches canonical source")
        return 0

    TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in expected.items():
        (TARGET_DIR / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(expected)} snapshot files to {TARGET_DIR.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
