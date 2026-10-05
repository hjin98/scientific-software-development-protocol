#!/usr/bin/env python3
"""Test rig that drives the REAL production path for the OMP D4 verification.

`harness70.run_episode` -> `adapters.omp` (real realization, principals, sandbox, launch) -> the
real frozen OMP executable -> the trusted observer -> the qualification MCP bridge + unchanged
mediator -> a deterministic local model-provider stand-in (the only substituted component: the
external provider, which lies below every semantic owner being accepted) -> raw evidence ->
adapter normalization -> core validation.

No real provider secret is used or required: the observer is given a harmless sentinel credential
and the stand-in verifies that exactly that credential arrives upstream.
"""
from __future__ import annotations

import json
import os
import sys
import subprocess
import threading
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import harness70  # noqa: E402
import stand_in_provider  # noqa: E402
from adapters import omp  # noqa: E402

REPO = HERE.parents[2]
DIST_SKILLS = REPO / "dist" / "skills"
STAGEF_WORKSPACE_ROOT = Path.home() / "ssdp70-omp-stagef"
QUALIFICATION_ROOT = STAGEF_WORKSPACE_ROOT / "qualification"
OMP_EXE = Path(os.environ.get("SSDP70_OMP_EXE", os.path.expanduser("~/.local/bin/omp")))
CREDENTIAL_ENV = "SSDP70_OMP_PROVIDER_CREDENTIAL"
SENTINEL_CREDENTIAL = "SENTINEL-PROVIDER-CREDENTIAL-D4-NOT-A-SECRET"


PROMPT_DEFAULT = "Do the task."


def prerequisites() -> list[str]:
    missing = []
    if not OMP_EXE.is_file():
        missing.append(f"OMP executable {OMP_EXE}")
    elif core70.sha256_file(OMP_EXE) != omp.OMP_BUILD["sha256"]:
        missing.append("OMP executable differs from the exact frozen build")
    if not Path("/usr/bin/bwrap").is_file():
        missing.append("bubblewrap")
    if not DIST_SKILLS.is_dir():
        missing.append("dist/skills protocol package")
    return missing


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


class Rig:
    """One corpus + arm + frozen profile; `run(scenario, ...)` performs one real episode."""

    def __init__(self, root: Path, *, reasoning: bool = True, thinking: str = "high", max_turns: int = 30,
                 timeout_s: int = 120, claims: list[str] | None = None, entry: str = "ordinary",
                 project_files: dict[str, str] | None = None, prompt: str = "Do the task."):
        QUALIFICATION_ROOT.mkdir(parents=True, exist_ok=True)
        candidate = subprocess.run(
            ["git", "rev-parse", "--short=12", "HEAD"], cwd=REPO, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.root = QUALIFICATION_ROOT / f"OMP-STANDIN-{stamp}-{candidate}-{uuid.uuid4().hex[:12]}"
        self.root.mkdir()
        root = self.root
        self.reasoning = reasoning
        self.thinking = thinking
        self.max_turns = max_turns
        self.timeout_s = timeout_s
        self.claims = claims if claims is not None else []
        self.entry = entry
        self.prompt = prompt
        self.known_premise_construction = not project_files
        self.corpus = root / "corpus"
        fixture = self.corpus / "fixtures" / "f1" / "project"
        fixture.mkdir(parents=True)
        (fixture / "README.md").write_text("fixture readme\n")
        (fixture / "notes.txt").write_text("alpha\nbeta\n")
        for rel, text in (project_files or {}).items():
            target = fixture / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        stub = self.corpus / "stubs" / "s1" / "issues"
        (stub / "local").mkdir(parents=True)
        (stub / "_config.yaml").write_text(yaml.safe_dump({"locations": {"local": "available", "remote": "unavailable"}}))
        (stub / "local" / "A-1.yaml").write_text(yaml.safe_dump({"title": "first issue", "labels": [], "body": "b", "comments": []}))
        (self.corpus / "stubs" / "s1" / "delegates").mkdir(parents=True)
        (self.corpus / "stubs" / "s1" / "delegates" / "reviewer.yaml").write_text(yaml.safe_dump({"return": "scripted delegate says ok"}))
        self.episode = {
            "id": "E1", "fixture": "f1", "stub": "s1", "prompt": prompt, "claims": self.claims,
            "entry": entry, "account": "agent-account",
        }
        (self.corpus / "manifest.yaml").write_text(yaml.safe_dump({"episodes": [self.episode]}))
        self.arm = {
            "name": "p70", "requested_ref": "test-ref", "commit": "a" * 40, "version": "7.0.0",
            "skills_path": str(DIST_SKILLS), "dist_tree_sha256": core70.sha256_tree(DIST_SKILLS),
        }
        self.arms_manifest = root / "arms.json"
        write_json(self.arms_manifest, {"schema": 1, "arms": [self.arm]})
        self.arms_manifest_sha, = (core70.sha256_file(self.arms_manifest),)
        self.cap_path = HERE / "capabilities" / "omp-headless.json"
        self.req_root = root / "requirements"
        write_json(self.req_root / "required_artifacts.json", {"schema": 1, "episodes": {"E1": [
            "summary.json", "run-identity.json", "trace.jsonl", "events.normalized.jsonl", "normalization-map.json",
            "final-report.md", "final-tree", "oracle.json", "requirements-snapshot.json",
            "adapter-artifacts", "project-control-record.json",
        ]}})
        write_json(self.req_root / "required_oracles.json", {"schema": 1, "episodes": {"E1": [{"id": "o1", "path": "check_o1.py"}]}})
        write_json(self.req_root / "expected_scoring_items.json", {"schema": 1, "episodes": {"E1": [
            {"id": "i1", "measure": "critical", "critical": True, "branch": "main", "allowed_dispositions": ["pass", "fail", "unresolved"]}
        ]}})
        self.oracles = root / "oracles"
        (self.oracles / "E1").mkdir(parents=True)
        (self.oracles / "E1" / "check_o1.py").write_text("import sys\nsys.exit(0)\n")
        self.stand_in_log = root / "stand-in.jsonl"

    # ---------------------------------------------------------------- profile
    def profile(self, upstream: str, *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
        template = json.loads((HERE / "profiles" / "omp-headless.template.json").read_text())
        profile = omp.freeze_profile(
            template,
            executable_path=str(OMP_EXE),
            provider_route={
                "provider_id": "stand", "model_id": "stand-model", "upstream": upstream,
                "context_window": 32000, "max_tokens": 4000, "reasoning": self.reasoning,
            },
            reasoning={"thinking": self.thinking, "source": "--thinking"},
            profile_id="omp-headless-d4-standin",
            budgets={"max_turns": self.max_turns, "timeout_s": self.timeout_s},
        )
        if not self.entry.startswith("pinned:"):
            profile["activation_mechanism"] = "ordinary-read"
            profile["runtime_input_template"] = omp.input_template("ordinary-read")
        if extra:
            profile.update(extra)
        return profile

    # -------------------------------------------------------------------- run
    def run(self, scenario: dict[str, Any], *, out_name: str = "run", mutate_profile=None, claims: list[str] | None = None,
            mode: str = "probe", stand_in_credential: str | None = SENTINEL_CREDENTIAL) -> dict[str, Any]:
        os.environ[CREDENTIAL_ENV] = SENTINEL_CREDENTIAL
        server, _state = stand_in_provider.serve(
            scenario, port=0, log=str(self.stand_in_log), expected_credential=stand_in_credential)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            profile = self.profile(f"http://127.0.0.1:{port}")
            if mutate_profile is not None:
                profile = mutate_profile(profile)
            profile_path = self.root / f"{out_name}-profile.json"
            write_json(profile_path, profile)
            bundle = core70.load_profile(profile_path, self.cap_path)
            episode = dict(self.episode)
            if claims is not None:
                episode["claims"] = claims
            requirements = core70.load_requirements(self.req_root, "E1")
            adapter = harness70.load_adapter("omp")
            arm = self.arm
            dist = harness70.resolve_arm_dist(arm)
            identity = harness70.run_identity(
                corpus=self.corpus, episode=episode, arm=arm, arms_manifest_sha256=self.arms_manifest_sha, dist=dist,
                profile_bundle=bundle, profile_path=profile_path, capability_path=self.cap_path,
                requirements=requirements, requirements_root=self.req_root, adapter_module=adapter,
                oracles=self.oracles, mode=mode, admission=None, rep=0, pair_order=["p70"],
            )
            out = self.root / out_name
            original_launch = adapter.launch
            def launch_with_fixture_witness(*args, **kwargs):
                if self.known_premise_construction and kwargs.get("accounting_purpose") != "qualification":
                    import package_premise
                    def supplied_witness(package, sources, mounts):
                        return package_premise.development_witness(package, sources, mounts=mounts,
                            construction_record={"record":"omp_rig known development fixture construction",
                            "evidence":"Fixed README/notes and synthetic issue seeds; explicit runtime closure, supervisor control generators and closed stand-in tools. Development evidence only; not independent admission."})
                    kwargs["premise_witness_provider"] = supplied_witness
                return original_launch(*args, **kwargs)
            adapter.launch = launch_with_fixture_witness
            try:
                summary = harness70.run_episode(
                corpus=self.corpus, episode=episode, arm=arm, arms_manifest_sha256=self.arms_manifest_sha, dist=dist,
                out=out, profile_bundle=bundle, profile_path=profile_path, capability_path=self.cap_path,
                requirements=requirements, requirements_root=self.req_root, adapter_module=adapter,
                oracles=self.oracles, mode=mode, admission=None, identity=identity, pair_order=["p70"],
                )
            finally:
                adapter.launch = original_launch
            summary["_out"] = str(out)
            summary["_stand_in_requests"] = self.read_stand_in()
            return summary
        finally:
            server.shutdown()
            server.server_close()

    def read_stand_in(self) -> list[dict[str, Any]]:
        if not self.stand_in_log.is_file():
            return []
        rows = [json.loads(line) for line in self.stand_in_log.read_text().splitlines() if line.strip()]
        return rows

    def reset_stand_in_log(self) -> None:
        if self.stand_in_log.exists():
            self.stand_in_log.unlink()


def load_events(out: str | Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in (Path(out) / "events.normalized.jsonl").read_text().splitlines() if line.strip()]


def scenario_steps(*steps: dict[str, Any]) -> dict[str, Any]:
    return {"steps": list(steps)}


def call(name: str, **arguments: Any) -> dict[str, Any]:
    return {"tool_calls": [{"name": name, "arguments": arguments}]}


def calls(*items: tuple[str, dict[str, Any]]) -> dict[str, Any]:
    return {"tool_calls": [{"name": name, "arguments": args} for name, args in items]}


def text(value: str) -> dict[str, Any]:
    return {"text": value}
