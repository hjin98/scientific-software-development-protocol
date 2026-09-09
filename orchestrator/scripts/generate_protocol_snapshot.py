#!/usr/bin/env python3
"""Generate/check current Protocol 6 snapshot and prove frozen 5.16 parity."""

from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGE_SRC = REPO_ROOT / "orchestrator" / "src"
sys.path.insert(0, str(PACKAGE_SRC))

from sdp_orchestrator.core import profile as P  # noqa: E402
from sdp_orchestrator.core.canonical import parse_document  # noqa: E402
from sdp_orchestrator.core.protocol_source import (  # noqa: E402
    CANONICAL_PROMPTS_RELPATH,
    CANONICAL_VERSION_RELPATH,
    PACKAGED_PROFILE,
    PACKAGED_PROMPTS,
)

RESOURCE_ROOT = PACKAGE_SRC / "sdp_orchestrator" / "core" / "resources" / "protocol"
CURRENT_TARGET_DIR = RESOURCE_ROOT / P.DEFAULT_PROFILE_ID
LEGACY_TARGET_DIR = RESOURCE_ROOT / P.PROFILE_ID
LEGACY_GIT_BLOBS = {
    PACKAGED_PROMPTS: "3730b06393843e9c24406a324f981ab4481858da",
    PACKAGED_PROFILE: "b3d4257fcd18af7bdb1799b2db742659bb2403fc",
}


def _git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324


def validate_legacy() -> list[str]:
    drift: list[str] = []
    texts: dict[str, str] = {}
    for name, expected_sha in LEGACY_GIT_BLOBS.items():
        path = LEGACY_TARGET_DIR / name
        if not path.is_file():
            drift.append(f"legacy:{name}:missing")
            continue
        data = path.read_bytes()
        if _git_blob_sha(data) != expected_sha:
            drift.append(f"legacy:{name}:immutable-bytes-changed")
        try:
            texts[name] = data.decode("utf-8")
        except UnicodeDecodeError:
            drift.append(f"legacy:{name}:not-utf8")
    if set(texts) == {PACKAGED_PROMPTS, PACKAGED_PROFILE}:
        document = parse_document(texts[PACKAGED_PROMPTS], profile_id=P.PROFILE_ID)
        derived = P.profile_to_json(P.build_profile(document, P.PROFILE_ID).descriptor)
        if derived != texts[PACKAGED_PROFILE]:
            drift.append("legacy:profile-not-derived-from-prompts")
    return drift


def render_current() -> dict[str, str]:
    defn = P.definition(P.DEFAULT_PROFILE_ID)
    declared_version = (REPO_ROOT / CANONICAL_VERSION_RELPATH).read_text(encoding="utf-8").strip()
    if declared_version != defn.protocol_version:
        raise ValueError(f"canonical source Protocol version does not match current profile: {declared_version!r} != {defn.protocol_version!r}")
    prompts = (REPO_ROOT / CANONICAL_PROMPTS_RELPATH).read_text(encoding="utf-8")
    document = parse_document(prompts, profile_id=P.DEFAULT_PROFILE_ID)
    snapshot = P.build_profile(document, P.DEFAULT_PROFILE_ID)
    return {PACKAGED_PROMPTS: prompts, PACKAGED_PROFILE: P.profile_to_json(snapshot.descriptor)}


# Backward-compatible script seam retained for existing Core tests/importers.
render = render_current


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    legacy_drift = validate_legacy()
    if legacy_drift:
        print("legacy Protocol 5.16 snapshot drift: " + ", ".join(legacy_drift), file=sys.stderr)
        return 1
    try:
        expected = render_current()
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"snapshot generation failed: {exc}", file=sys.stderr)
        return 1
    if args.check:
        drift = [name for name, text in expected.items() if not (CURRENT_TARGET_DIR / name).is_file() or (CURRENT_TARGET_DIR / name).read_text(encoding="utf-8") != text]
        if drift:
            print(f"current packaged snapshot is stale: {', '.join(drift)}", file=sys.stderr)
            return 1
        print("current Protocol 6 snapshot matches canonical source; Protocol 5.16 snapshot is immutable and coherent")
        return 0
    CURRENT_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in expected.items():
        (CURRENT_TARGET_DIR / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(expected)} current snapshot files to {CURRENT_TARGET_DIR.relative_to(REPO_ROOT)}")
    print("validated frozen Protocol 5.16 snapshot without rewriting it")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
