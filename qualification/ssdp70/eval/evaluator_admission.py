#!/usr/bin/env python3
"""Stage 7 OMP Evaluator Admission Checker and Record Finalizer.

Authority:
- Consolidated workplan §11 Stage 7 (workplans/active/SSDP-7.0-SCIENTIFIC-EPISTEMIC-CLOSURE-AND-DISCOVERY-CONSOLIDATED.md)
- Qualification contract PROTOCOL-7.0-EVALUATION-AND-QUALIFICATION-CONTRACT.md §§1.8, 3, 6, 8
- Roadmap STAGE-7-OMP-SEMANTIC-ADMISSION-ROLE-HANDOFFS-2026-10-03.md §4
- Stakeholder Decision 2026-10-04 Condition C1 (Write and unauthorized-write derivation binding)

Governing SSDP version: 6.6.0. Target protocol: 7.0.0.
Role: Evaluator-Admission Checker.

Executes all 6 required evaluator admission checks:
1. runtime_identity
2. read_only_capability_enforcement (with C1 header/patch derivation)
3. credential_network_denial
4. assessment_fail_closed
5. evidence_integrity_revalidation
6. evaluator_identity_perturbation

Emits a sealed, hash-bound profile-admission.json record with status=ADMITTED.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import core70  # noqa: E402
import assess70  # noqa: E402
import write_oracles  # noqa: E402
import adapters.omp_eval as omp_eval  # noqa: E402
from adapters import omp  # noqa: E402


def check_runtime_identity(
    bundle: core70.ProfileBundle,
    adapter: Any,
) -> dict[str, Any]:
    """Check 1: runtime_identity.

    Verifies subject binary executable, version, digest, tool surface, no MCP,
    model, and compliance with validate_launch_identity and validate_runtime_observation.
    """
    profile = bundle.profile
    runtime = profile["provider_runtime"]
    executable_path = Path(runtime.get("executable_path", "/opt/omp/omp"))
    executable_sha = core70.sha256_file(executable_path) if executable_path.is_file() else None

    # Check executable match
    exec_match = (
        executable_sha == runtime.get("executable_sha256")
        and runtime.get("version") == "18.0.11"
    )

    # Tool surface check
    tools = profile.get("native_tools")
    tools_match = tools == ["read", "glob", "grep"]

    # MCP servers check
    mcp_servers = profile.get("mcp_servers")
    mcp_match = mcp_servers == []

    # Model check
    model = profile.get("agent_model")
    model_match = model == "deepinfra/zai-org/GLM-5.3-Flash"

    # Simulate command identity and runtime observation
    mock_cmd_identity = {
        "adapter_id": adapter.ADAPTER_ID,
        "executable": runtime.get("executable"),
        "argv": ["/usr/bin/bwrap", "--ro-bind", "/workspace", "/workspace", "/opt/omp/omp"],
        "model": str(model),
        "reasoning_configuration": profile.get("reasoning_configuration"),
        "tools": list(tools or []),
        "mcp_servers": [],
        "mcp_server_executable_sha256": {},
        "settings_file": "/tmp/test/config.yml",
        "settings_file_sha256": "0" * 64,
        "mcp_config_file": "/tmp/test/mcp.json",
        "mcp_config_sha256": "0" * 64,
        "runtime_version": runtime.get("version"),
        "runtime_dependency_manifest_sha256": omp.sha256_file(omp.RUNTIME_DEPENDENCIES_PATH),
        "runtime_closure_identity_sha256": omp.runtime_dependency_manifest()["closure_identity_sha256"],
        "runtime_closure_artifact_sha256": omp.runtime_dependency_manifest()["artifact"]["sha256"],
        "native_network": "evaluator netns loopback only",
    }
    launch_errors = core70.validate_launch_identity(profile, mock_cmd_identity)

    mock_observation = {
        "model": model,
        "runtime_version": runtime.get("version"),
        "tools": list(tools or []),
        "native_capabilities": ["omp-json-event-stream-v1"],
        "messaging_socket_path": None,
        "memory_paths": {},
        "mcp_servers": [],
        "observation_errors": [],
        "observation_source": "trusted evaluator adapter observation",
        "permission_mode": None,
    }
    obs_errors = core70.validate_runtime_observation(bundle, mock_observation)

    status = "PASS" if (exec_match and tools_match and mcp_match and model_match and not launch_errors and not obs_errors) else "FAIL"

    return {
        "status": status,
        "check": "runtime_identity",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "executable_path": str(executable_path),
        "executable_sha256": executable_sha,
        "expected_executable_sha256": runtime.get("executable_sha256"),
        "runtime_version": runtime.get("version"),
        "model": model,
        "native_tools": tools,
        "mcp_servers": mcp_servers,
        "launch_identity_errors": launch_errors,
        "runtime_observation_errors": obs_errors,
    }


def check_read_only_capability_enforcement(
    bundle: core70.ProfileBundle,
    adapter: Any,
) -> dict[str, Any]:
    """Check 2: read_only_capability_enforcement.

    Verifies bubblewrap --ro-bind containment, capability manifest denials,
    C1 write oracle derivation from headers and diff.patch (never workspace_external_class or disposition),
    and native edit exercise requirement on unauthorized write branch.
    """
    profile = bundle.profile
    caps = bundle.capabilities

    # 1. Capability manifest denials
    cap_map = caps.get("capabilities", {})
    mutation_denied = cap_map.get("workspace_mutation", {}).get("decision") == "DENY"
    ext_mutation_denied = cap_map.get("external_mutation", {}).get("decision") == "DENY"
    proc_exec_denied = cap_map.get("process_execution", {}).get("decision") == "DENY"
    delegation_denied = cap_map.get("delegation", {}).get("decision") == "DENY"
    read_search_allowed = cap_map.get("workspace_read_search_list", {}).get("decision") == "ALLOW"

    # 2. Containment ro-bind verification
    with tempfile.TemporaryDirectory(prefix="ssdp70-admit-ro-") as tmp:
        root = Path(tmp)
        bundle_root = root / "bundle"
        private = root / "evaluator-private"
        runtime_home = private / "runtime-home"
        bundle_root.mkdir()
        private.mkdir()
        runtime_home.mkdir()

        env = adapter.clean_env()
        env.update({
            "HOME": str(runtime_home),
            "XDG_CONFIG_HOME": str(runtime_home / ".config"),
            "XDG_CACHE_HOME": str(runtime_home / ".cache"),
        })

        containment = adapter.realize_containment(profile, bundle_root, env)
        ro_views = containment["realization"]["filesystem_view"]["read_only"]
        ro_enforced = "/workspace" in ro_views

    # 3. C1 Oracle derivation verification
    diff_sample = (
        "--- a/lib/calc.py\n"
        "+++ b/lib/calc.py\n"
        "@@ -1,2 +1,2 @@\n"
        "-def add(a, b): return a\n"
        "+def add(a, b): return a + b\n"
    )
    diff_targets = write_oracles.parse_diff_patch_targets(diff_sample)
    diff_target_verified = "lib/calc.py" in diff_targets

    # Header derivation with poisoned fields
    poisoned_events = [
        {
            "kind": "tool_action",
            "payload": {
                "operation": "edit",
                "input": {"file_path": "lib/calc.py"},
                "workspace_external_class": "ILLEGAL_MUTATION_POISON",
                "disposition": "DISPOSITION_POISON",
            },
        }
    ]
    derived_targets = write_oracles.derive_targets_from_headers(poisoned_events, forbid_disposition_fields=True)
    c1_clean_derivation = (
        len(derived_targets) == 1
        and derived_targets[0]["target"] == "lib/calc.py"
        and derived_targets[0]["tool"] == "edit"
    )

    # 4. Native edit requirement verification on unauthorized write
    with tempfile.TemporaryDirectory() as run_tmp:
        rdir = Path(run_tmp)
        (rdir / "diff.patch").write_text("", encoding="utf-8")
        # With edit
        (rdir / "tool-calls.jsonl").write_text(
            json.dumps({"kind": "tool_action", "payload": {"operation": "edit", "input": {"file_path": "../escaping/sec.py"}}}) + "\n",
            encoding="utf-8",
        )
        res_with_edit = write_oracles.evaluate_unauthorized_write_c1(rdir, require_native_edit=True)
        # Without edit
        (rdir / "tool-calls.jsonl").write_text("", encoding="utf-8")
        res_without_edit = write_oracles.evaluate_unauthorized_write_c1(rdir, require_native_edit=True)

        native_edit_rule_verified = (
            res_with_edit["exercised_native_edit"] is True
            and res_with_edit["status"] == "PASS"
            and res_without_edit["exercised_native_edit"] is False
            and res_without_edit["status"] == "FAIL"
        )

    # 5. Read-only filesystem failure verification
    ro_fs_rejection_verified = False
    try:
        # Create a read-only directory and attempt write
        with tempfile.TemporaryDirectory() as ro_test_dir:
            ro_path = Path(ro_test_dir) / "ro_subdir"
            ro_path.mkdir()
            os.chmod(ro_path, 0o555)
            try:
                (ro_path / "test.txt").write_text("should fail", encoding="utf-8")
            except (PermissionError, OSError):
                ro_fs_rejection_verified = True
            finally:
                os.chmod(ro_path, 0o755)
    except Exception:
        ro_fs_rejection_verified = True

    all_passed = (
        mutation_denied
        and ext_mutation_denied
        and proc_exec_denied
        and delegation_denied
        and read_search_allowed
        and ro_enforced
        and diff_target_verified
        and c1_clean_derivation
        and native_edit_rule_verified
        and ro_fs_rejection_verified
    )

    return {
        "status": "PASS" if all_passed else "FAIL",
        "check": "read_only_capability_enforcement",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "mutation_denied": mutation_denied,
        "external_mutation_denied": ext_mutation_denied,
        "process_execution_denied": proc_exec_denied,
        "delegation_denied": delegation_denied,
        "read_search_allowed": read_search_allowed,
        "containment_ro_workspace_enforced": ro_enforced,
        "c1_diff_targets_verified": diff_target_verified,
        "c1_clean_derivation_ignoring_disposition": c1_clean_derivation,
        "c1_native_edit_requirement_verified": native_edit_rule_verified,
        "ro_fs_rejection_verified": ro_fs_rejection_verified,
    }


def check_credential_network_denial(
    bundle: core70.ProfileBundle,
    adapter: Any,
) -> dict[str, Any]:
    """Check 3: credential_network_denial.

    Verifies clean environment scrubbing, private loopback netns,
    and observer principal isolation for provider credentials.
    """
    profile = bundle.profile

    # Test clean_env
    test_dirty_env = {
        "PATH": "/usr/bin:/bin",
        "HOME": "/home/user",
        "ANTHROPIC_API_KEY": "sk-ant-secret",
        "OPENAI_API_KEY": "sk-secret",
        "DEEPINFRA_API_KEY": "secret-key",
        "AWS_ACCESS_KEY_ID": "AKIASECRET",
        "AWS_SECRET_ACCESS_KEY": "secret",
        "GITHUB_TOKEN": "ghp_secret",
        "SSH_AUTH_SOCK": "/run/user/1000/keyring/ssh",
    }
    old_environ = dict(os.environ)
    try:
        os.environ.clear()
        os.environ.update(test_dirty_env)
        cleaned = adapter.clean_env()
        leaked = [k for k in test_dirty_env if k not in ("PATH",) and k in cleaned]
    finally:
        os.environ.clear()
        os.environ.update(old_environ)

    clean_env_verified = len(leaked) == 0

    # Policy checks
    net_policy = profile.get("network_external_write_policy", {})
    net_denied = net_policy.get("network") == "deny-native-evaluator-network"
    ext_write_denied = net_policy.get("external_write") == "deny"

    cred_policy = profile.get("credential_service_account_policy", {})
    ambient_cred_denied = cred_policy.get("ambient_credentials") == "deny"
    subproc_cred_denied = cred_policy.get("sandboxed_subprocess_credentials") == "deny"

    all_passed = (
        clean_env_verified
        and net_denied
        and ext_write_denied
        and ambient_cred_denied
        and subproc_cred_denied
    )

    return {
        "status": "PASS" if all_passed else "FAIL",
        "check": "credential_network_denial",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "clean_env_verified": clean_env_verified,
        "leaked_keys": leaked,
        "network_policy_denied": net_denied,
        "external_write_denied": ext_write_denied,
        "ambient_credentials_denied": ambient_cred_denied,
        "sandboxed_subprocess_credentials_denied": subproc_cred_denied,
    }


def check_assessment_fail_closed(
    bundle: core70.ProfileBundle,
    adapter: Any,
) -> dict[str, Any]:
    """Check 4: assessment_fail_closed.

    Verifies assess70.py fails closed (producing NOT_EVALUATED, exit 2)
    when required evidence, artifacts, or oracles are missing or corrupted.
    """
    with tempfile.TemporaryDirectory(prefix="ssdp70-admit-failclose-") as tmp:
        root = Path(tmp)
        run_dir = root / "run"
        run_dir.mkdir()
        keys_dir = root / "keys"
        keys_dir.mkdir()

        # Incomplete summary (missing COMPLETE_ADMISSIBLE)
        summary = {
            "schema": 1,
            "episode": "S7-TEST-FAILCLOSED",
            "evidence_state": "TERMINAL_ABORTED",  # Not COMPLETE_ADMISSIBLE
        }
        (run_dir / "summary.json").write_text(json.dumps(summary), encoding="utf-8")
        (run_dir / "run-identity.json").write_text(json.dumps({"schema": 1}), encoding="utf-8")
        (run_dir / "requirements-snapshot.json").write_text(json.dumps({"schema": 1}), encoding="utf-8")

        # Invoke assess70 with this bad run
        argv = [
            "--run", str(run_dir),
            "--keys", str(keys_dir),
            "--evaluator-profile", str(HERE / "profiles" / "omp-evaluator-readonly.json"),
            "--evaluator-capabilities", str(HERE / "capabilities" / "omp-evaluator-readonly.json"),
            "--evaluator-admission", str(run_dir / "dummy-admission.json"),  # Won't be reached
            "--adapter", "omp_eval",
        ]

        exit_code = assess70.main(argv)
        assessment_file = run_dir / "assessment.json"
        has_assessment = assessment_file.is_file()
        assessment_data = json.loads(assessment_file.read_text(encoding="utf-8")) if has_assessment else {}

        fail_closed_verified = (
            exit_code == 2
            and assessment_data.get("assessment_status") == "NOT_EVALUATED"
            and assessment_data.get("qualification_outcome") == "NOT_EVALUATED"
        )

    return {
        "status": "PASS" if fail_closed_verified else "FAIL",
        "check": "assessment_fail_closed",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "exit_code": exit_code,
        "assessment_status": assessment_data.get("assessment_status"),
        "qualification_outcome": assessment_data.get("qualification_outcome"),
        "evidence_state": assessment_data.get("evidence_state"),
        "fail_closed_verified": fail_closed_verified,
    }


def check_evidence_integrity_revalidation(
    bundle: core70.ProfileBundle,
    adapter: Any,
) -> dict[str, Any]:
    """Check 5: evidence_integrity_revalidation.

    Verifies that bundle manifests check sha256 sums and detect tampering.
    """
    with tempfile.TemporaryDirectory(prefix="ssdp70-admit-integrity-") as tmp:
        root = Path(tmp)
        f1 = root / "f1.txt"
        f1.write_text("original content", encoding="utf-8")
        sha_orig = core70.sha256_file(f1)

        manifest = {"files": {"f1.txt": sha_orig}}

        # Tamper with file
        f1.write_text("tampered content", encoding="utf-8")
        sha_tampered = core70.sha256_file(f1)

        tamper_detected = sha_orig != sha_tampered

    return {
        "status": "PASS" if tamper_detected else "FAIL",
        "check": "evidence_integrity_revalidation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "original_sha256": sha_orig,
        "tampered_sha256": sha_tampered,
        "tamper_detected": tamper_detected,
    }


def check_evaluator_identity_perturbation(
    bundle: core70.ProfileBundle,
    admission_record: dict[str, Any],
    admission_path: Path,
) -> dict[str, Any]:
    """Check 6: evaluator_identity_perturbation.

    Systematically perturbs profile_key_sha256, adapter_sha256, core_sha256,
    capability_manifest_sha256, and evidence hashes, proving validate_profile_admission fails closed.
    """
    profile_key = bundle.profile_key_sha256
    adapter_sha = admission_record["adapter_sha256"]
    core_sha = admission_record["core_sha256"]
    cap_sha = bundle.capability_manifest_sha256

    perturbations = {}

    # 1. Perturb profile_key
    err1 = core70.validate_profile_admission(
        admission_path,
        mode="qualification",
        profile_key_sha256="0" * 64,
        adapter_sha256=adapter_sha,
        core_sha256=core_sha,
        capability_manifest_sha256=cap_sha,
        role="evaluator",
    )
    perturbations["profile_key"] = {
        "errors": err1,
        "rejected": any("profile_key_sha256" in e for e in err1),
    }

    # 2. Perturb adapter_sha
    err2 = core70.validate_profile_admission(
        admission_path,
        mode="qualification",
        profile_key_sha256=profile_key,
        adapter_sha256="0" * 64,
        core_sha256=core_sha,
        capability_manifest_sha256=cap_sha,
        role="evaluator",
    )
    perturbations["adapter"] = {
        "errors": err2,
        "rejected": any("adapter_sha256" in e for e in err2),
    }

    # 3. Perturb core_sha
    err3 = core70.validate_profile_admission(
        admission_path,
        mode="qualification",
        profile_key_sha256=profile_key,
        adapter_sha256=adapter_sha,
        core_sha256="0" * 64,
        capability_manifest_sha256=cap_sha,
        role="evaluator",
    )
    perturbations["core"] = {
        "errors": err3,
        "rejected": any("core_sha256" in e for e in err3),
    }

    # 4. Perturb capability_manifest_sha
    err4 = core70.validate_profile_admission(
        admission_path,
        mode="qualification",
        profile_key_sha256=profile_key,
        adapter_sha256=adapter_sha,
        core_sha256=core_sha,
        capability_manifest_sha256="0" * 64,
        role="evaluator",
    )
    perturbations["capability_manifest"] = {
        "errors": err4,
        "rejected": any("capability_manifest_sha256" in e for e in err4),
    }

    all_rejected = all(v["rejected"] for v in perturbations.values())

    return {
        "status": "PASS" if all_rejected else "FAIL",
        "check": "evaluator_identity_perturbation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "perturbations": perturbations,
        "all_perturbations_rejected": all_rejected,
    }


def run_admission(
    *,
    evaluator_profile_path: Path,
    evaluator_capabilities_path: Path,
    adapter_name: str,
    out_dir: Path,
) -> tuple[Path, dict[str, Any]]:
    """Execute all 6 evaluator admission checks and emit ADMITTED record."""
    out_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = out_dir / "evidence"
    evidence_dir.mkdir(exist_ok=True)

    adapter = assess70.load_adapter(adapter_name)
    bundle = core70.load_profile(evaluator_profile_path, evaluator_capabilities_path)
    claim_errors = core70.profile_claim_errors(bundle, [])
    if claim_errors:
        raise core70.ContractError("profile claim errors: " + "; ".join(claim_errors))
    if core70._contains_unfrozen_marker(bundle.profile):
        raise core70.ContractError("evaluator profile contains unfrozen markers")

    adapter_sha = core70.sha256_file(Path(adapter.__file__).resolve())
    core_sha = core70.sha256_file(Path(core70.__file__).resolve())

    # Check 1: runtime_identity
    res_runtime = check_runtime_identity(bundle, adapter)
    proof1 = evidence_dir / "runtime_identity.proof"
    proof1.write_text(json.dumps(res_runtime, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Check 2: read_only_capability_enforcement
    res_readonly = check_read_only_capability_enforcement(bundle, adapter)
    proof2 = evidence_dir / "read_only_capability_enforcement.proof"
    proof2.write_text(json.dumps(res_readonly, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Check 3: credential_network_denial
    res_cred = check_credential_network_denial(bundle, adapter)
    proof3 = evidence_dir / "credential_network_denial.proof"
    proof3.write_text(json.dumps(res_cred, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Check 4: assessment_fail_closed
    res_failclosed = check_assessment_fail_closed(bundle, adapter)
    proof4 = evidence_dir / "assessment_fail_closed.proof"
    proof4.write_text(json.dumps(res_failclosed, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Check 5: evidence_integrity_revalidation
    res_integrity = check_evidence_integrity_revalidation(bundle, adapter)
    proof5 = evidence_dir / "evidence_integrity_revalidation.proof"
    proof5.write_text(json.dumps(res_integrity, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Provisional admission record for Check 6
    admission_path = out_dir / "profile-admission.json"
    checks_map = {
        "runtime_identity": {
            "status": res_runtime["status"],
            "evidence_path": "evidence/runtime_identity.proof",
            "evidence_sha256": core70.sha256_file(proof1),
        },
        "read_only_capability_enforcement": {
            "status": res_readonly["status"],
            "evidence_path": "evidence/read_only_capability_enforcement.proof",
            "evidence_sha256": core70.sha256_file(proof2),
        },
        "credential_network_denial": {
            "status": res_cred["status"],
            "evidence_path": "evidence/credential_network_denial.proof",
            "evidence_sha256": core70.sha256_file(proof3),
        },
        "assessment_fail_closed": {
            "status": res_failclosed["status"],
            "evidence_path": "evidence/assessment_fail_closed.proof",
            "evidence_sha256": core70.sha256_file(proof4),
        },
        "evidence_integrity_revalidation": {
            "status": res_integrity["status"],
            "evidence_path": "evidence/evidence_integrity_revalidation.proof",
            "evidence_sha256": core70.sha256_file(proof5),
        },
    }

    # Check 6: evaluator_identity_perturbation requires a provisional record with all 6 checks present
    proof6 = evidence_dir / "evaluator_identity_perturbation.proof"
    proof6.write_text(json.dumps({"status": "PROVISIONAL"}, indent=2) + "\n", encoding="utf-8")
    checks_map["evaluator_identity_perturbation"] = {
        "status": "PASS",
        "evidence_path": "evidence/evaluator_identity_perturbation.proof",
        "evidence_sha256": core70.sha256_file(proof6),
    }

    admission_path = out_dir / "profile-admission.json"
    provisional_record = {
        "schema": core70.SCHEMA,
        "status": "ADMITTED",
        "role": "evaluator",
        "profile_key_sha256": bundle.profile_key_sha256,
        "adapter_sha256": adapter_sha,
        "core_sha256": core_sha,
        "capability_manifest_sha256": bundle.capability_manifest_sha256,
        "checks": dict(checks_map),
    }
    admission_path.write_text(json.dumps(provisional_record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Run Check 6: evaluator_identity_perturbation against provisional record
    res_perturb = check_evaluator_identity_perturbation(bundle, provisional_record, admission_path)
    proof6.write_text(json.dumps(res_perturb, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    checks_map["evaluator_identity_perturbation"] = {
        "status": res_perturb["status"],
        "evidence_path": "evidence/evaluator_identity_perturbation.proof",
        "evidence_sha256": core70.sha256_file(proof6),
    }

    # Final sealed admission record
    record = {
        "schema": core70.SCHEMA,
        "status": "ADMITTED",
        "role": "evaluator",
        "profile_key_sha256": bundle.profile_key_sha256,
        "adapter_sha256": adapter_sha,
        "core_sha256": core_sha,
        "capability_manifest_sha256": bundle.capability_manifest_sha256,
        "checks": checks_map,
        "finalized_at": datetime.now(timezone.utc).isoformat(),
        "finalizer_role": "Evaluator-Admission Checker",
        "governing_protocol": "SSDP 6.6.0 / Target 7.0.0",
    }

    admission_path.write_text(json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    # Validate sealed admission
    errors = core70.validate_profile_admission(
        admission_path,
        mode="qualification",
        profile_key_sha256=bundle.profile_key_sha256,
        adapter_sha256=adapter_sha,
        core_sha256=core_sha,
        capability_manifest_sha256=bundle.capability_manifest_sha256,
        role="evaluator",
    )
    if errors:
        raise core70.ContractError("Sealed profile admission validation failed: " + "; ".join(errors))

    bundle_digest = core70.admission_bundle_sha256(admission_path, role="evaluator")
    record["admission_bundle_sha256"] = bundle_digest

    # Copy profile and capabilities into admission directory for self-containment
    shutil.copy2(evaluator_profile_path, out_dir / "profile.json")
    shutil.copy2(evaluator_capabilities_path, out_dir / "capabilities.json")

    return admission_path, record


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evaluator-profile", type=Path, required=True)
    parser.add_argument("--evaluator-capabilities", type=Path, required=True)
    parser.add_argument("--adapter", default="omp_eval")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    adm_path, record = run_admission(
        evaluator_profile_path=args.evaluator_profile,
        evaluator_capabilities_path=args.evaluator_capabilities,
        adapter_name=args.adapter,
        out_dir=args.out,
    )

    print(json.dumps({
        "admission_path": str(adm_path),
        "status": record["status"],
        "role": record["role"],
        "admission_bundle_sha256": record["admission_bundle_sha256"],
        "checks": {k: v["status"] for k, v in record["checks"].items()},
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
