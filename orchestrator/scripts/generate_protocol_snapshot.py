#!/usr/bin/env python3
"""Generate/check current Protocol 6.3 snapshot and prove frozen profile parity."""
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
from sdp_orchestrator.core.protocol_source import CANONICAL_PROMPTS_RELPATH, CANONICAL_VERSION_RELPATH, PACKAGED_PROFILE, PACKAGED_PROMPTS  # noqa: E402

RESOURCE_ROOT = PACKAGE_SRC / "sdp_orchestrator" / "core" / "resources" / "protocol"
CURRENT_TARGET_DIR = RESOURCE_ROOT / P.DEFAULT_PROFILE_ID
FROZEN = {
    P.PROFILE_ID: {PACKAGED_PROMPTS: "3730b06393843e9c24406a324f981ab4481858da", PACKAGED_PROFILE: "b3d4257fcd18af7bdb1799b2db742659bb2403fc"},
    P.SSDP6_PROFILE_ID: {PACKAGED_PROMPTS: "d127b9eb8da165afd905d4c35cc8b7572b201d56", PACKAGED_PROFILE: "76c53539a985bc8408f8432932e91e5477696db9"},
    P.SSDP61_PROFILE_ID: {PACKAGED_PROMPTS: "4e79f1c5c10fb4f867595ba6ade391a6d97020dc", PACKAGED_PROFILE: "c74b4e0f4cc40530710fea21c83268d917f03612"},
    P.SSDP62_PROFILE_ID: {PACKAGED_PROMPTS: "159c58cbac0a8cf66311ddf7e11ad8eb03644e8c", PACKAGED_PROFILE: "6f21ad0592da343db951ffd56d25aa74a881bd8c"},
}

def _git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()  # noqa: S324

def validate_frozen() -> list[str]:
    drift: list[str] = []
    for profile_id, expected in FROZEN.items():
        root = RESOURCE_ROOT / profile_id
        texts: dict[str, str] = {}
        for name, expected_sha in expected.items():
            path = root / name
            if not path.is_file():
                drift.append(f"{profile_id}:{name}:missing")
                continue
            data = path.read_bytes()
            if _git_blob_sha(data) != expected_sha:
                drift.append(f"{profile_id}:{name}:immutable-bytes-changed")
            try:
                texts[name] = data.decode("utf-8")
            except UnicodeDecodeError:
                drift.append(f"{profile_id}:{name}:not-utf8")
        if set(texts) == {PACKAGED_PROMPTS, PACKAGED_PROFILE}:
            document = parse_document(texts[PACKAGED_PROMPTS], profile_id=profile_id)
            derived = P.profile_to_json(P.build_profile(document, profile_id).descriptor)
            if derived != texts[PACKAGED_PROFILE]:
                drift.append(f"{profile_id}:profile-not-derived-from-prompts")
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

render = render_current

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    drift = validate_frozen()
    if drift:
        print("frozen Protocol profile drift: " + ", ".join(drift), file=sys.stderr)
        return 1
    try:
        expected = render_current()
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"snapshot generation failed: {exc}", file=sys.stderr)
        return 1
    if args.check:
        stale = [name for name, text in expected.items() if not (CURRENT_TARGET_DIR / name).is_file() or (CURRENT_TARGET_DIR / name).read_text(encoding="utf-8") != text]
        if stale:
            print(f"current packaged snapshot is stale: {', '.join(stale)}", file=sys.stderr)
            return 1
        print("current Protocol 6.3 snapshot matches canonical source; Protocol 5.16, 6.0, 6.1, and 6.2 snapshots are immutable and coherent")
        return 0
    CURRENT_TARGET_DIR.mkdir(parents=True, exist_ok=True)
    for name, text in expected.items():
        (CURRENT_TARGET_DIR / name).write_text(text, encoding="utf-8")
    print(f"wrote {len(expected)} current snapshot files to {CURRENT_TARGET_DIR.relative_to(REPO_ROOT)}")
    print("validated frozen Protocol 5.16, 6.0, 6.1, and 6.2 snapshots without rewriting them")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
