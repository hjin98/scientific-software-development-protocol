#!/usr/bin/env python3
"""Extract exact Protocol 6.5/6.6/7.0 evaluation arms from immutable Git refs.

This prepares scratch packages without checking out or mutating the repository. It verifies
source and generated-package version stamps and records full commit identities plus tree
hashes so Stage F runs can bind evidence to exact subjects.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import shutil
import subprocess
import tarfile
from pathlib import Path

DEFAULT_ARMS = {
    "p65": ("7f7b5e24858e813e45ace867a7f8ea5180f43bf0", "6.5.0"),
    "p66": ("22f4bdba53795da3a6f13f162529f3a843fc37ae", "6.6.0"),
    "p70": ("db94a2dfb7fef480f37227eab5c45256e89901b8", "7.0.0"),
}
SKILLS = (
    "scientific-formulation",
    "numerical-algorithm-design",
    "software-design",
    "software-implementation",
    "software-documentation",
    "software-maintenance-audit",
    "repository-hygiene",
)


def git(repo: Path, *args: str, text: bool = True) -> str | bytes:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=text,
    )
    if proc.returncode != 0:
        detail = proc.stderr.strip() if text else proc.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout


def tree_sha256(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        digest.update(path.relative_to(root).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def safe_extract_tar(payload: bytes, destination: Path) -> None:
    with tarfile.open(fileobj=io.BytesIO(payload), mode="r:") as archive:
        for member in archive.getmembers():
            member_path = Path(member.name)
            if member_path.is_absolute() or ".." in member_path.parts:
                raise RuntimeError(f"unsafe archive member: {member.name}")
        archive.extractall(destination, filter="data")


def extract_arm(repo: Path, out: Path, name: str, ref: str, expected_version: str) -> dict:
    resolved = str(git(repo, "rev-parse", f"{ref}^{{commit}}")).strip()
    source_version = str(git(repo, "show", f"{resolved}:source/PROTOCOL_VERSION")).strip()
    if source_version != expected_version:
        raise RuntimeError(f"{name}: source version {source_version!r} != {expected_version!r}")

    target = out / name
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    payload = git(repo, "archive", "--format=tar", resolved, "dist/skills", text=False)
    assert isinstance(payload, bytes)
    safe_extract_tar(payload, target)
    skills_root = target / "dist" / "skills"

    actual = {path.name for path in skills_root.iterdir() if path.is_dir()}
    missing = set(SKILLS) - actual
    if missing:
        raise RuntimeError(f"{name}: generated dist is missing SSDP skills: {sorted(missing)}")
    package_versions = {}
    for skill in SKILLS:
        stamp = (skills_root / skill / "PROTOCOL_VERSION").read_text(encoding="utf-8").strip()
        package_versions[skill] = stamp
        if stamp != expected_version:
            raise RuntimeError(f"{name}:{skill}: package version {stamp!r} != {expected_version!r}")

    return {
        "name": name,
        "requested_ref": ref,
        "commit": resolved,
        "version": source_version,
        "skills_path": str(skills_root.resolve()),
        "dist_tree_sha256": tree_sha256(skills_root),
        "package_versions": package_versions,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--candidate-ref", default=DEFAULT_ARMS["p70"][0])
    args = parser.parse_args()

    repo = args.repo.resolve()
    out = args.out.resolve()
    arms = dict(DEFAULT_ARMS)
    arms["p70"] = (args.candidate_ref, "7.0.0")
    out.mkdir(parents=True, exist_ok=True)

    records = []
    for name, (ref, version) in arms.items():
        records.append(extract_arm(repo, out, name, ref, version))
    manifest = {"schema": 1, "repo": str(repo), "arms": records}
    (out / "arms.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
