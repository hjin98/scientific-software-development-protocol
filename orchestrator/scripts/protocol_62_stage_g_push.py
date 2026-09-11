#!/usr/bin/env python3
"""One-use Protocol 6.2 Stage G runner; workflow cleanup is external."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

RECOVERY = "b59adc77efe6951912cfd705cc43830c58ca27d0"
BOOTSTRAP = "5a062ebc472755607b9dc66d33a5ebbc4b7429aa"
INVALIDATED = "1181c2031710c5d343194d87d08543290fded0ab"
TEMPORARY = (
    ".github/scripts/protocol_62_stage_g.py",
    ".github/workflows/protocol-62-stage-g-materialize.yml",
    ".github/workflows/protocol-62-stage-g-materialize-v2.yml",
    ".github/workflows/protocol-62-stage-g-materialize-v3.yml",
    ".github/workflows/protocol-62-stage-g-materialize-v4.yml",
    ".github/workflows/protocol-62-core-diagnose.yml",
    "qualification/ssdp6/STAGE-G-CORE-DIAGNOSTIC.txt",
    "orchestrator/scripts/protocol_62_stage_g_materialize.py",
    "orchestrator/scripts/protocol_62_stage_g_push.py",
)


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def hide_temporary_surfaces() -> None:
    for raw in TEMPORARY:
        path = Path(raw)
        if path.exists():
            path.unlink()


def restore_temporary_surfaces() -> None:
    tracked = [raw for raw in TEMPORARY if subprocess.run(["git", "cat-file", "-e", f"HEAD:{raw}"], check=False).returncode == 0]
    if tracked:
        run("git", "checkout", "HEAD", "--", *tracked)


def patch_mapping() -> None:
    version_path = Path("source/shared/references/protocol-versioning-and-compatibility.md")
    text = version_path.read_text(encoding="utf-8")
    old_map = (
        "5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3\n"
        "6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2\n"
        "6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639"
    )
    if old_map not in text or f"6.2.0  -> {RECOVERY}" in text:
        raise RuntimeError("unexpected Protocol 6.2 recovery-map precondition")
    text = text.replace(old_map, old_map + f"\n6.2.0  -> {RECOVERY}", 1)

    old_stage = (
        "After candidate qualification and independent Review, choose a separate immutable recovery commit containing the accepted semantic candidate and required decision evidence through ancestry. Only a later mapping commit may publish `6.2.0 -> <recovery SHA>`; the public-source bootstrap is not acceptance/recovery identity.\n\n"
        "Until all 6.2 acceptance stages complete, Protocol 6.1 remains accepted-current/rollback authority."
    )
    new_stage = f"""The accepted Protocol 6.2 recovery target is:

```text
6.2.0 -> {RECOVERY}
```

That immutable commit contains semantic candidate `ebbc4591bdfed039512026b8acb3a6749475c1c5` through ancestry together with its qualification/requalification/generated evidence and independent Review PASS. The public-source bootstrap remains `{BOOTSTRAP}` and is intentionally distinct from recovery identity.

Git commits cannot self-name, so this recovery mapping is published only by a later descendant after the recovery target already exists. Until mapping-bearing generated descendants, targeted recovery/parity checks, semantic-evolution/Protocol-7 reconciliation, and lifecycle closeout pass, Protocol 6.1 remains accepted-current/rollback authority."""
    if old_stage not in text:
        raise RuntimeError("unexpected Protocol 6.2 staging-text precondition")
    version_path.write_text(text.replace(old_stage, new_stage, 1), encoding="utf-8")

    portability_path = Path("PORTABILITY.md")
    text = portability_path.read_text(encoding="utf-8")
    old = f"6.2.0 public bootstrap -> {BOOTSTRAP}\n"
    if old not in text or f"6.2.0 recovery -> {RECOVERY}" in text:
        raise RuntimeError("unexpected PORTABILITY recovery-map precondition")
    text = text.replace(old, old + f"6.2.0 recovery -> {RECOVERY}\n", 1)
    anchor = "If neither a compatible installed source nor the compatible immutable public source can be read, report truthful non-closure rather than executing the protocol from memory."
    note = (
        f"Protocol 6.2 recovery is separately pinned to `{RECOVERY}` after independent Review PASS. "
        f"Recovery contains the accepted candidate and decision evidence through ancestry; public fallback continues to use bootstrap `{BOOTSTRAP}`, not the recovery snapshot.\n\n"
        + anchor
    )
    if anchor not in text:
        raise RuntimeError("unexpected PORTABILITY note anchor")
    portability_path.write_text(text.replace(anchor, note, 1), encoding="utf-8")


def add_recovery_oracle() -> None:
    path = Path("tests/test_protocol_62_representation.py")
    text = path.read_text(encoding="utf-8")
    if "test_accepted_62_recovery_and_bootstrap_remain_distinct" in text:
        return
    marker = '\n\nif __name__ == "__main__":\n'
    method = f'''
    def test_accepted_62_recovery_and_bootstrap_remain_distinct(self):
        recovery = "{RECOVERY}"
        bootstrap = "{BOOTSTRAP}"
        invalidated = "{INVALIDATED}"
        versioning = (REFERENCES / "protocol-versioning-and-compatibility.md").read_text()
        portability = (ROOT / "PORTABILITY.md").read_text()
        self.assertIn(f"6.2.0  -> {{recovery}}", versioning)
        self.assertIn(f"6.2.0 recovery -> {{recovery}}", portability)
        self.assertIn(f"6.2.0 public-source bootstrap -> {{bootstrap}}", versioning)
        self.assertIn(f"6.2.0 public bootstrap -> {{bootstrap}}", portability)
        self.assertNotEqual(recovery, bootstrap)
        self.assertNotEqual(recovery, invalidated)
        self.assertNotIn(f"6.2.0  -> {{invalidated}}", versioning)
'''
    if marker not in text:
        raise RuntimeError("test insertion anchor not found")
    path.write_text(text.replace(marker, "\n" + method + marker, 1), encoding="utf-8")


def main() -> None:
    run("git", "config", "user.name", "github-actions[bot]")
    run("git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com")

    patch_mapping()
    run("git", "diff", "--check")
    run("git", "add", "PORTABILITY.md", "source/shared/references/protocol-versioning-and-compatibility.md")
    run("git", "commit", "-m", "Publish Protocol 6.2 recovery mapping")

    add_recovery_oracle()
    hide_temporary_surfaces()

    run("python", "-m", "pip", "install", "-r", "source/requirements-validation.txt")
    out = Path("/tmp/protocol-dist")
    shutil.rmtree(out, ignore_errors=True)
    run("python", "source/build_skills.py", "--output", str(out))
    run("python", "source/validate_packages.py", "--dist", str(out))
    shutil.rmtree("dist")
    shutil.copytree(out, "dist")
    run("python", "source/check_dist.py", "--expected", str(out), "--committed", "dist")
    run("python", "-m", "unittest", "tests.test_protocol_62_representation", "-v")
    run("python", "-m", "unittest", "discover", "-s", "tests", "-v")
    run("git", "diff", "--check")

    run("python", "-m", "pip", "install", "./orchestrator", "-r", "orchestrator/requirements-dev.txt")
    run("python", "orchestrator/scripts/generate_protocol_snapshot.py", "--check")
    run("python", "orchestrator/scripts/run_core_tests.py")

    restore_temporary_surfaces()
    run("git", "add", "dist", "tests/test_protocol_62_representation.py")
    run("git", "commit", "-m", "Regenerate Protocol 6.2 recovery-mapped distributions")
    run("git", "push", "origin", "HEAD:ssdp-6.2-lossless-representation")


if __name__ == "__main__":
    main()
