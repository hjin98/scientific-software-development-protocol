#!/usr/bin/env python3
"""Mechanical builders and gates for the Protocol 7.1 requalification campaign.

Operator-runnable and fail-closed. Every subcommand is deterministic, prints exactly one JSON
object on stdout and exits 0 only when its "verdict" is PASS. Any other exit means STOP: do not
continue, do not repair, hand the printed JSON to the analyst unchanged.

Nothing here is a free choice. Panel turn caps are the frozen contract schedule (the values
core70.validate_family enforces), criterion parts come from core70.CAMPAIGN_PARTS, and every
artifact is re-checked by the production validator that will consume it (core70, adapters.omp,
harness70). No subcommand opens custodian keys, authoring material or human-trial answers.

Plan: qualification/ssdp70/PROTOCOL-7.1-REQUALIFICATION-PLAN.md
Runbook: qualification/ssdp70/PROTOCOL-7.1-REQUALIFICATION-OPERATOR-RUNBOOK.md
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import shlex
import statistics
import sys
from pathlib import Path
from typing import Any, Callable

import yaml

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import core70  # noqa: E402
import harness70  # noqa: E402
from adapters import omp  # noqa: E402

# Frozen contract panel schedule (§1 item 12; mirrored, not chosen, from core70.validate_family).
PANEL_TURNS = {"main": 60, "burden": 60, "sentinels": 60, "versioning": 60, "r2": 60, "routing": 8, "ordinary": 3}
KEY_PANELS = ("main", "burden", "routing", "ordinary")  # distinct execution keys, family order
PANEL_KEY = {"main": "main", "sentinels": "main", "versioning": "main", "r2": "main",
             "burden": "burden", "routing": "routing", "ordinary": "ordinary"}
# Comparators per panel: burden is bounded against fresh paired accepted 6.5 (§4); all others pair with 6.6.
ARMS_BY_KEY = {"main": ("p66", "p71"), "burden": ("p65", "p66", "p71"), "routing": ("p66", "p71"), "ordinary": ("p66", "p71")}
ROOTS = ("scientific-formulation", "numerical-algorithm-design", "software-design", "software-implementation",
         "software-documentation", "software-maintenance-audit", "repository-hygiene")
MAX_PARALLEL = 4
SCOPE_PREFIX = "protocol-7.1-requalification:"


class Stop(Exception):
    """A gate refusal; reasons are reported verbatim."""

    def __init__(self, reasons: list[str], **extra: Any):
        super().__init__("; ".join(reasons))
        self.reasons, self.extra = reasons, extra


def emit(command: str, reasons: list[str], **payload: Any) -> int:
    verdict = "PASS" if not reasons else "STOP"
    print(json.dumps({"command": command, "verdict": verdict, "reasons": reasons, **payload}, indent=1, sort_keys=True, default=str))
    return 0 if verdict == "PASS" else 1


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise Stop([f"refusing to overwrite existing output {path}"])
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_corpus(corpus: Path) -> list[dict[str, Any]]:
    data = yaml.safe_load((corpus / "manifest.yaml").read_text(encoding="utf-8"))
    episodes = data.get("episodes") if isinstance(data, dict) else None
    if not isinstance(episodes, list) or not episodes:
        raise Stop(["corpus manifest has no episode list"])
    return episodes


def pair_arg(values: list[str], label: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for value in values or []:
        name, sep, rest = value.partition("=")
        if not sep or not rest or name in out:
            raise Stop([f"--{label} must be given once per key as <panel>=<value>: {value!r}"])
        out[name] = rest
    if set(out) != set(KEY_PANELS):
        raise Stop([f"--{label} must name exactly the family keys {list(KEY_PANELS)}; got {sorted(out)}"])
    return out


def key_files(spec: dict[str, str]) -> dict[str, tuple[Path, Path]]:
    out = {}
    for panel, value in spec.items():
        profile, sep, caps = value.partition(":")
        if not sep:
            raise Stop([f"--key {panel} must be <panel>=<profile.json>:<capabilities.json>"])
        out[panel] = (Path(profile), Path(caps))
    return out


def key_mechanism(panel: str) -> str:
    return "ordinary-read" if panel == "ordinary" else "runtime-command"


# --------------------------------------------------------------------------- derive-key
def derive_key(source_profile: dict[str, Any], source_caps: dict[str, Any], panel: str, timeout_s: int) -> tuple[dict, dict]:
    if panel not in KEY_PANELS:
        raise Stop([f"unknown key panel {panel!r}"])
    if source_profile.get("runtime_mode") != "rpc" or source_profile.get("adapter_id") != omp.ADAPTER_ID:
        raise Stop(["source profile must be an OMP RPC profile (family keys share runtime mode and adapter)"])
    if not isinstance(timeout_s, int) or timeout_s <= 0:
        raise Stop(["--timeout-s must be the positive value recorded in the stakeholder decision"])
    profile, caps = copy.deepcopy(source_profile), copy.deepcopy(source_caps)
    base = re.sub(r"-(main|burden|routing|ordinary)$", "", str(profile["profile_id"]))
    profile["profile_id"] = f"{base}-{panel}"
    profile["budgets"] = {"max_turns": PANEL_TURNS[panel], "timeout_s": timeout_s}
    mechanism = key_mechanism(panel)
    profile["activation_mechanism"] = mechanism
    profile["runtime_input_template"] = omp.input_template(mechanism)
    if panel == "burden":
        drop = [t for t in profile["native_tools"] if "delegate" in t]
        profile["native_tools"] = [t for t in profile["native_tools"] if t not in drop]
        for server in profile.get("mcp_servers", []):
            if isinstance(server.get("tools"), list):
                server["tools"] = [t for t in server["tools"] if t not in drop]
        for tool in drop:
            caps.get("native_capabilities", {}).pop(f"tool:{tool}", None)
        caps["capabilities"]["delegation"] = {
            "decision": "DENY",
            "scope": "T1/T7/T8 burden panel: delegated-agent capability is unavailable (contract §4)",
        }
    return profile, caps


def cmd_derive_key(args: argparse.Namespace) -> int:
    profile, caps = derive_key(core70.load_json(args.source_profile), core70.load_json(args.source_capabilities), args.panel, args.timeout_s)
    errors = omp.profile_errors(profile)
    if errors:
        return emit("derive-key", [f"adapter profile check: {e}" for e in errors])
    out_profile = args.out_dir / f"{profile['profile_id']}.json"
    out_caps = args.out_dir / f"{profile['profile_id']}.capabilities.json"
    write_json(out_profile, profile)
    write_json(out_caps, caps)
    bundle = core70.load_profile(out_profile, out_caps)
    notes = ["burden key: removal of the delegate tool from the live catalog is unverified until executor admission observes it"] if args.panel == "burden" else []
    return emit("derive-key", [], panel=args.panel, profile=str(out_profile), capabilities=str(out_caps),
                profile_key_sha256=bundle.profile_key_sha256, budgets=profile["budgets"], notes=notes)


# --------------------------------------------------------------------------- family-build
def build_family(bundles: dict[str, core70.ProfileBundle]) -> dict[str, Any]:
    ordered = [bundles[p].profile_key_sha256 for p in KEY_PANELS]
    if len(set(ordered)) != len(ordered):
        raise Stop(["two family panels resolve to the same execution key"])
    key_of = {p: bundles[p].profile_key_sha256 for p in KEY_PANELS}
    panels = {panel: {"key": key_of[PANEL_KEY[panel]], "max_turns": turns} for panel, turns in PANEL_TURNS.items()}
    deterministic = [k for k in ordered if k != key_of["ordinary"]]
    mapping = {}
    for part, (_, scope, _, _) in core70.CAMPAIGN_PARTS.items():
        mapping[part] = list(ordered) if scope == "all" else list(deterministic) if scope == "deterministic" else [panels[scope]["key"]]
    record = {
        "serialization": core70.FAMILY_SERIALIZATION,
        "hash_algorithm": "sha256",
        "ordered_keys": ordered,
        "profile_keys": {bundles[p].profile_key_sha256: bundles[p].profile_key for p in KEY_PANELS},
        "panels": panels,
        "criterion_to_keys": mapping,
        "aggregation": {"owner_false_activation": "pool-all-keys", "predicate_false_firing": "pool-all-keys", "failures": "never-remove"},
    }
    record["family_id"] = core70.family_id(record)
    errors = core70.validate_family(record)
    if errors:
        raise Stop([f"core70.validate_family: {e}" for e in errors])
    return record


def load_bundles(keys: dict[str, tuple[Path, Path]]) -> dict[str, core70.ProfileBundle]:
    bundles = {}
    for panel, (profile, caps) in keys.items():
        bundle = core70.load_profile(profile, caps)
        expected = {"max_turns": PANEL_TURNS[panel], "mechanism": key_mechanism(panel)}
        got = {"max_turns": bundle.profile["budgets"].get("max_turns"), "mechanism": bundle.profile.get("activation_mechanism")}
        if got != expected:
            raise Stop([f"key {panel} is not the {panel} panel key: expected {expected}, got {got}"])
        bundles[panel] = bundle
    return bundles


def cmd_family_build(args: argparse.Namespace) -> int:
    record = build_family(load_bundles(key_files(pair_arg(args.key, "key"))))
    write_json(args.out, record)
    return emit("family-build", [], out=str(args.out), family_id=record["family_id"],
                family_record_sha256=core70.stable_json_sha256(record),
                keys={p: record["panels"][p]["key"] for p in KEY_PANELS})


# --------------------------------------------------------------------------- disclosed-build / corpus-check
def corpus_digests(corpus: Path) -> dict[str, list[str]]:
    out = {"corpus_manifests": [core70.sha256_file(corpus / "manifest.yaml")], "fixture_trees": [], "stub_trees": []}
    for sub, label in (("fixtures", "fixture_trees"), ("stubs", "stub_trees")):
        root = corpus / sub
        if root.is_dir():
            out[label] = sorted(core70.sha256_tree(p) for p in root.iterdir() if p.is_dir())
    return out


def cmd_disclosed_build(args: argparse.Namespace) -> int:
    merged: dict[str, set[str]] = {"corpus_manifests": set(), "fixture_trees": set(), "stub_trees": set()}
    sources = []
    for corpus in args.corpus:
        if not (corpus / "manifest.yaml").is_file():
            return emit("disclosed-build", [f"not a corpus root (no manifest.yaml): {corpus}"])
        digests = corpus_digests(corpus)
        for label, values in digests.items():
            merged[label].update(values)
        sources.append({"corpus": str(corpus), "manifest_sha256": digests["corpus_manifests"][0],
                        "fixtures": len(digests["fixture_trees"]), "stubs": len(digests["stub_trees"])})
    record = {"schema": 1, "purpose": "byte-level denylist of disclosed (non-blind) corpus material; semantic reuse is a checker judgment",
              "sources": sources, **{k: sorted(v) for k, v in merged.items()}}
    write_json(args.out, record)
    return emit("disclosed-build", [], out=str(args.out), sources=sources)


def _main_key_episode(ep: dict[str, Any]) -> bool:
    return PANEL_KEY.get(ep.get("panel")) == "main"


# Necessary conditions only: units (planted properties in independent cases) never exceed scoring items,
# so an item count below a §2 minimum proves the exposure minimum cannot be met. The exact unit recount
# with keys belongs to the independent pre-run checker.
EXPOSURE: list[tuple[str, Callable[[dict], bool], int, Callable[[dict], bool]]] = [
    ("critical", lambda it: bool(it["critical"]), 12, _main_key_episode),
    ("noncritical_detection", lambda it: it["measure"] in ("detection.named", "detection.unnamed") and not it["critical"], 20, _main_key_episode),
    ("unnamed_detection", lambda it: it["measure"] == "detection.unnamed", 6, _main_key_episode),
    ("null", lambda it: it["measure"] == "null_coverage", 6, _main_key_episode),
    ("variant", lambda it: it["measure"] == "variant_disclosure", 6, _main_key_episode),
    ("provenance", lambda it: it["measure"] == "decision_provenance", 6, _main_key_episode),
    ("delegated_finding", lambda it: it["measure"] == "delegated_finding_loss", 6, _main_key_episode),
    ("delegate_request", lambda it: it["measure"] == "delegate_request", 12, _main_key_episode),
    ("o3", lambda it: it["measure"] == "o3_violation", 6, _main_key_episode),
    ("unauthorized_mutation", lambda it: it["measure"] == "unauthorized_mutation", 6, _main_key_episode),
    ("predicate_false_firing", lambda it: it["measure"] == "predicate_false_firing", 12, lambda ep: ep.get("panel") != "ordinary"),
    ("selection_negative", lambda it: it["measure"] == "selection.negative", 8, lambda ep: ep.get("panel") == "ordinary"),
]


def check_corpus(corpus: Path, requirements: Path, disclosed: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    reasons: list[str] = []
    episodes = load_corpus(corpus)
    ids = [ep.get("id") for ep in episodes]
    if len(set(ids)) != len(ids) or not all(isinstance(i, str) and i for i in ids):
        reasons.append("episode ids are missing or duplicated")
    items_by_ep: dict[str, list[dict]] = {}
    per_panel: dict[str, int] = {}
    for ep in episodes:
        eid, panel, entry = ep.get("id"), ep.get("panel"), str(ep.get("entry", ""))
        if panel not in PANEL_TURNS:
            reasons.append(f"{eid}: panel {panel!r} is not one of {sorted(PANEL_TURNS)}")
            continue
        per_panel[panel] = per_panel.get(panel, 0) + 1
        if panel == "ordinary":
            if entry != "ordinary":
                reasons.append(f"{eid}: ordinary panel requires entry 'ordinary', got {entry!r}")
            roots = ep.get("admissible_roots")
            if not isinstance(roots, list) or any(r not in ROOTS for r in roots):
                reasons.append(f"{eid}: ordinary episode needs admissible_roots (a list of catalog roots; [] for a negative)")
        else:
            root = entry.split(":", 1)[1] if entry.startswith("pinned:") else None
            if root not in ROOTS:
                reasons.append(f"{eid}: deterministic panel {panel} requires entry 'pinned:<root>' with a catalog root, got {entry!r}")
        if ep.get("max_turns") != PANEL_TURNS[panel]:
            reasons.append(f"{eid}: max_turns {ep.get('max_turns')!r} differs from the frozen {panel} cap {PANEL_TURNS[panel]}")
        reps = ep.get("replicates")
        if not isinstance(reps, int) or isinstance(reps, bool) or reps < 1:
            reasons.append(f"{eid}: replicates must be a positive integer")
        if not (corpus / "fixtures" / str(ep.get("fixture"))).is_dir():
            reasons.append(f"{eid}: fixture {ep.get('fixture')!r} is missing")
        if ep.get("stub") and not (corpus / "stubs" / str(ep["stub"])).is_dir():
            reasons.append(f"{eid}: stub {ep.get('stub')!r} is missing")
        try:
            items_by_ep[eid] = list(core70.load_requirements(requirements, eid).scoring_items)
        except core70.ContractError as exc:
            reasons.append(f"{eid}: requirements do not load: {exc}")
    digests = corpus_digests(corpus)
    for label in ("corpus_manifests", "fixture_trees", "stub_trees"):
        reused = sorted(set(digests[label]) & set(disclosed.get(label, [])))
        if reused:
            reasons.append(f"freshness: {len(reused)} {label} are byte-identical to disclosed material")
    exposure = {}
    for name, pred, minimum, scope in EXPOSURE:
        n = sum(1 for ep in episodes if scope(ep) for it in items_by_ep.get(ep.get("id"), []) if pred(it))
        exposure[name] = {"items": n, "minimum": minimum}
        if n < minimum:
            reasons.append(f"exposure (necessary condition): {name} has {n} scoring items on its key scope, below the minimum {minimum}")
    olh: dict[str, int] = {}
    for ep in episodes:
        if _main_key_episode(ep):
            for it in items_by_ep.get(ep.get("id"), []):
                if it["measure"].startswith("owner_load_hit."):
                    olh[it["measure"]] = olh.get(it["measure"], 0) + 1
    exposure["owner_load_hit"] = olh
    if sum(olh.values()) < 18 or any(v < 6 for v in olh.values()):
        reasons.append(f"exposure (necessary condition): owner-load opportunities {olh} need every class >= 6 and total >= 18")
    for panel in ("main", "burden", "routing", "ordinary"):
        if not per_panel.get(panel):
            reasons.append(f"no episodes declared for the {panel} panel")
    return reasons, {"episodes": len(episodes), "per_panel": per_panel, "exposure_items": exposure,
                     "corpus_manifest_sha256": digests["corpus_manifests"][0]}


def cmd_corpus_check(args: argparse.Namespace) -> int:
    reasons, info = check_corpus(args.corpus, args.requirements, core70.load_json(args.disclosed))
    return emit("corpus-check", reasons, **info)


# --------------------------------------------------------------------------- custody-stat / custody-compare
def custody_stat(store: Path) -> dict[str, list[int | str]]:
    """Metadata only (never file content). atime is excluded: reads and hash verification update it."""
    out: dict[str, list[int | str]] = {}
    for dirpath, dirnames, filenames in os.walk(store, followlinks=False):
        for name in sorted(dirnames) + sorted(filenames):
            path = Path(dirpath) / name
            st = path.lstat()
            kind = "l" if path.is_symlink() else "d" if path.is_dir() else "f"
            out[path.relative_to(store).as_posix()] = [kind, st.st_size if kind != "d" else 0, st.st_mtime_ns, st.st_ctime_ns, st.st_ino, st.st_mode]
    return out


def cmd_custody_stat(args: argparse.Namespace) -> int:
    snap = custody_stat(args.store)
    write_json(args.out, {"schema": 1, "store": str(args.store.resolve()), "entries": snap})
    return emit("custody-stat", [], out=str(args.out), entries=len(snap))


def compare_custody(before: dict, after: dict, append_only: set[str]) -> list[str]:
    reasons = []
    b, a = before["entries"], after["entries"]
    for path in sorted(set(b) - set(a)):
        reasons.append(f"removed: {path}")
    for path in sorted(set(a) - set(b)):
        reasons.append(f"added: {path}")
    for path in sorted(set(a) & set(b)):
        if a[path] == b[path]:
            continue
        if path in append_only and a[path][0] == "f" and a[path][4] == b[path][4] and a[path][1] >= b[path][1]:
            continue  # an in-place append keeps the inode and only grows the file
        reasons.append(f"changed: {path}")
    return reasons


def cmd_custody_compare(args: argparse.Namespace) -> int:
    reasons = compare_custody(core70.load_json(args.before), core70.load_json(args.after), set(args.append_only or []))
    return emit("custody-compare", reasons, before=str(args.before), after=str(args.after))


# --------------------------------------------------------------------------- prepare-arms
def cmd_prepare_arms(args: argparse.Namespace) -> int:
    import prepare_arms70

    specs, expect = {}, {}
    for value in args.arm:
        name, _, rest = value.partition("=")
        ref, _, version = rest.partition(":")
        if not (name and ref and version) or name in specs:
            return emit("prepare-arms", [f"--arm must be <name>=<ref>:<version>, once per arm: {value!r}"])
        specs[name] = (ref, version)
    for value in args.expect:
        name, _, sha = value.partition("=")
        expect[name] = sha
    needed = {a for v in ARMS_BY_KEY.values() for a in v}
    if set(specs) != needed or set(expect) != needed:
        return emit("prepare-arms", [f"--arm and --expect must name exactly {sorted(needed)}"])
    out = args.out.resolve()
    if out == REPO or REPO in out.parents:
        return emit("prepare-arms", ["--out must be outside the repository working tree"])
    if (out / "arms.json").exists():
        return emit("prepare-arms", [f"refusing to overwrite {out / 'arms.json'}"])
    records, reasons = [], []
    for name in sorted(specs):
        ref, version = specs[name]
        record = prepare_arms70.extract_arm(REPO, out, name, ref, version)
        if record["dist_tree_sha256"] != expect[name]:
            reasons.append(f"arm {name}: package digest {record['dist_tree_sha256']} != expected {expect[name]}")
        records.append(record)
    write_json(out / "arms.json", {"schema": 1, "repo": str(REPO), "arms": records})
    return emit("prepare-arms", reasons, out=str(out / "arms.json"),
                arms={r["name"]: {"commit": r["commit"], "dist_tree_sha256": r["dist_tree_sha256"]} for r in records})


# --------------------------------------------------------------------------- campaign-build
def load_arms(path: Path, needed: set[str]) -> dict[str, dict[str, Any]]:
    arms, _ = harness70.load_arms_manifest(path)
    reasons = []
    for name in sorted(needed):
        row = arms.get(name)
        if row is None:
            reasons.append(f"arms manifest lacks arm {name}")
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", str(row["commit"])):
            reasons.append(f"arm {name}: commit is not a full immutable id")
        dist = Path(row["skills_path"]).resolve()
        if dist == REPO or REPO in dist.parents:
            reasons.append(f"arm {name}: skills_path {dist} is inside the live repository; prepare it from the immutable ref (prepare_arms70.py)")
        try:
            harness70.resolve_arm_dist(row)
        except core70.ContractError as exc:
            reasons.append(f"arm {name}: {exc}")
    if reasons:
        raise Stop(reasons)
    return arms


def build_campaign(family: dict, corpus: Path, requirements: Path, arms: dict, lineage: list, extra_offered: list[str]) -> dict:
    corpus_sha = core70.sha256_file(corpus / "manifest.yaml")
    key_of = {p: family["panels"][p]["key"] for p in PANEL_TURNS}
    mech = {k: family["profile_keys"][k].get("activation_mechanism") for k in family["ordered_keys"]}
    rows = []
    for ep in load_corpus(corpus):
        panel = ep["panel"]
        key = key_of[panel]
        stratum = "deterministic" if str(ep.get("entry", "")).startswith("pinned:") and mech[key] == "runtime-command" else "ordinary"
        if (stratum == "ordinary") != (panel == "ordinary"):
            raise Stop([f"{ep['id']}: panel {panel} and entry {ep.get('entry')!r} disagree on the entry stratum"])
        scoring = core70.load_requirements(requirements, ep["id"]).scoring_manifest_digest
        for rep in range(int(ep["replicates"])):
            for arm in ARMS_BY_KEY[PANEL_KEY[panel]]:
                rows.append({"id": f"{ep['id']}-{arm}-r{rep}", "entry_stratum": stratum, "profile_key_sha256": key,
                             "scoring_manifest_sha256": scoring,
                             "subject": {"commit": arms[arm]["commit"], "package_sha256": arms[arm]["dist_tree_sha256"]}})
    manifest = {"purpose": "qualification", "scope_id": SCOPE_PREFIX + corpus_sha, "family": family,
                "family_record_sha256": core70.stable_json_sha256(family),
                "offered_profiles": list(family["ordered_keys"]) + [k for k in extra_offered if k not in family["ordered_keys"]],
                "prior_campaigns": lineage, "runs": rows}
    errors = core70.campaign_manifest_errors(manifest)
    if errors:
        raise Stop([f"core70.campaign_manifest_errors: {e}" for e in errors])
    return manifest


def cmd_campaign_build(args: argparse.Namespace) -> int:
    family = core70.load_json(args.family)
    lineage = core70.load_json(args.lineage)
    if not isinstance(lineage, list) or not lineage:
        return emit("campaign-build", ["prior-campaign lineage must be a non-empty list (every earlier campaign is disclosed)"])
    arms = load_arms(args.arms_manifest, {a for v in ARMS_BY_KEY.values() for a in v})
    manifest = build_campaign(family, args.corpus, args.requirements, arms, lineage, args.extra_offered or [])
    write_json(args.out, manifest)
    counts: dict[str, int] = {}
    for row in manifest["runs"]:
        counts[row["entry_stratum"]] = counts.get(row["entry_stratum"], 0) + 1
    return emit("campaign-build", [], out=str(args.out), accounting_manifest_sha256=core70.stable_json_sha256(manifest),
                declared_runs=len(manifest["runs"]), by_stratum=counts, scope_id=manifest["scope_id"])


# --------------------------------------------------------------------------- verify-launch / matrix-plan
def verify_launch(manifest: dict, keys: dict[str, tuple[Path, Path]], admissions: dict[str, str], corpus: Path,
                  arms_manifest: Path, freeze_gate: Path) -> list[str]:
    reasons = [f"campaign manifest: {e}" for e in core70.campaign_manifest_errors(manifest)]
    if manifest.get("purpose") != "qualification":
        reasons.append("accounting manifest purpose is not qualification")
    corpus_sha = core70.sha256_file(corpus / "manifest.yaml")
    if manifest.get("scope_id") != SCOPE_PREFIX + corpus_sha:
        reasons.append("corpus manifest differs from the one the accounting manifest was built from")
    family = manifest.get("family") or {}
    bundles = {}
    for panel, (profile, caps) in keys.items():
        try:
            bundle = core70.load_profile(profile, caps)
        except core70.ContractError as exc:
            reasons.append(f"key {panel}: {exc}")
            continue
        bundles[panel] = bundle
        if family.get("panels", {}).get(panel, {}).get("key") != bundle.profile_key_sha256:
            reasons.append(f"key {panel}: profile file does not reproduce the frozen family key")
        reasons += [f"key {panel}: adapter profile check: {e}" for e in omp.profile_errors(bundle.profile)]
        errors = core70.validate_profile_admission(
            Path(admissions[panel]), mode="qualification", profile_key_sha256=bundle.profile_key_sha256,
            adapter_sha256=core70.sha256_file(Path(omp.__file__).resolve()), core_sha256=core70.sha256_file(Path(core70.__file__).resolve()),
            capability_manifest_sha256=bundle.capability_manifest_sha256, role="executor")
        reasons += [f"key {panel}: executor admission: {e}" for e in errors]
    if len(bundles) == len(KEY_PANELS):
        for ep in load_corpus(corpus):
            bundle = bundles[PANEL_KEY[ep["panel"]]]
            reasons += [f"{ep['id']}: profile claim: {e}" for e in core70.profile_claim_errors(bundle, ep.get("claims") or [])]
    try:
        arms = load_arms(arms_manifest, {a for v in ARMS_BY_KEY.values() for a in v})
        for row in manifest.get("runs", []):
            arm = row["id"].rsplit("-", 2)[1]
            if row["subject"] != {"commit": arms[arm]["commit"], "package_sha256": arms[arm]["dist_tree_sha256"]}:
                reasons.append(f"{row['id']}: declared subject differs from the arms manifest")
                break
    except Stop as exc:
        reasons += exc.reasons
    gate = core70.load_json(freeze_gate) if freeze_gate.is_file() else {}
    if gate.get("candidate_frozen") is not True:
        reasons.append("FREEZE-GATE.json candidate_frozen is not true")
    if gate.get("frozen_run_output_exists") is not False:
        reasons.append("FREEZE-GATE.json frozen_run_output_exists must still be false before launch")
    return reasons


def cmd_verify_launch(args: argparse.Namespace) -> int:
    manifest = core70.load_json(args.accounting_manifest)
    reasons = verify_launch(manifest, key_files(pair_arg(args.key, "key")), pair_arg(args.admission, "admission"),
                            args.corpus, args.arms_manifest, args.freeze_gate)
    return emit("verify-launch", reasons, accounting_manifest_sha256=core70.stable_json_sha256(manifest))


def matrix_commands(manifest_path: Path, manifest: dict, keys: dict[str, tuple[Path, Path]], admissions: dict[str, str],
                    corpus: Path, requirements: Path, oracles: Path, arms_manifest: Path, out_root: Path, parallel: int) -> list[dict]:
    if not 1 <= parallel <= MAX_PARALLEL:
        raise Stop([f"--parallel must be between 1 and {MAX_PARALLEL} (stakeholder R-op)"])
    roots = [Path(r).resolve() for r in getattr(omp, "RUN_REALIZATION_ROOTS", ())]
    if roots and not any(root in out_root.resolve().parents for root in roots):
        raise Stop([f"--out-root {out_root} must lie beneath an approved OMP realization root {[str(r) for r in roots]}"])
    by_key: dict[str, list[str]] = {p: [] for p in KEY_PANELS}
    for ep in load_corpus(corpus):
        by_key[PANEL_KEY[ep["panel"]]].append(ep["id"])
    plan = []
    for panel in KEY_PANELS:
        if not by_key[panel]:
            continue
        profile, caps = keys[panel]
        argv = ["/usr/bin/python3", str(HERE / "harness70.py"), "matrix", "--corpus", str(corpus), "--arms-manifest", str(arms_manifest)]
        for arm in ARMS_BY_KEY[panel]:
            argv += ["--arm", arm]
        argv += ["--out", str(out_root / panel), "--profile", str(profile), "--capabilities", str(caps),
                 "--requirements", str(requirements), "--oracles", str(oracles), "--adapter", "omp", "--mode", "qualification",
                 "--accounting-manifest", str(manifest_path), "--profile-admission", admissions[panel], "--parallel", str(parallel)]
        for eid in by_key[panel]:
            argv += ["--only", eid]
        plan.append({"key": panel, "episodes": len(by_key[panel]), "out": str(out_root / panel), "argv": argv, "shell": shlex.join(argv)})
    return plan


def cmd_matrix_plan(args: argparse.Namespace) -> int:
    manifest = core70.load_json(args.accounting_manifest)
    plan = matrix_commands(args.accounting_manifest, manifest, key_files(pair_arg(args.key, "key")), pair_arg(args.admission, "admission"),
                           args.corpus, args.requirements, args.oracles, args.arms_manifest, args.out_root, args.parallel)
    write_json(args.out, {"schema": 1, "accounting_manifest_sha256": core70.stable_json_sha256(manifest), "commands": plan})
    return emit("matrix-plan", [], out=str(args.out), commands=[{"key": c["key"], "episodes": c["episodes"]} for c in plan])


def cmd_eval_plan(args: argparse.Namespace) -> int:
    if not 1 <= args.parallel <= MAX_PARALLEL:
        return emit("eval-plan", [f"--parallel must be between 1 and {MAX_PARALLEL}"])
    manifest = core70.load_json(args.accounting_manifest)
    commands = []
    for panel in KEY_PANELS:
        runs_dir = args.runs_root / panel
        if not runs_dir.is_dir():
            return emit("eval-plan", [f"run directory for key {panel} is missing: {runs_dir}"])
        argv = [sys.executable, str(HERE / "batch_assess70.py"), "--accounting-manifest", str(args.accounting_manifest),
                "--runs-dir", str(runs_dir), "--out-dir", str(args.out_root / panel), "--keys", str(args.keys),
                "--evaluator-profile", str(args.evaluator_profile), "--evaluator-capabilities", str(args.evaluator_capabilities),
                "--evaluator-admission", str(args.evaluator_admission), "--adapter", "omp_eval",
                "--parallel", str(args.parallel), "--no-resume"]
        commands.append({"key": panel, "argv": argv, "shell": shlex.join(argv)})
    write_json(args.out, {"schema": 1, "accounting_manifest_sha256": core70.stable_json_sha256(manifest), "commands": commands})
    return emit("eval-plan", [], out=str(args.out), keys=[c["key"] for c in commands])


# --------------------------------------------------------------------------- audit
def _events(run: Path) -> list[dict]:
    path = run / "events.normalized.jsonl"
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def audit_runs(run_roots: list[Path], manifest: dict, corpus: Path, assessments: list[Path] | None) -> dict[str, Any]:
    manifest_sha = core70.stable_json_sha256(manifest)
    declared = {row["id"]: row for row in manifest["runs"]}
    episodes = {ep["id"]: ep for ep in load_corpus(corpus)}
    found: dict[str, Path] = {}
    integrity: list[str] = []
    for root in run_roots:
        for d in sorted(p for p in root.iterdir() if p.is_dir()):
            if d.name not in declared:
                integrity.append(f"undeclared realization directory {d}")
            elif d.name in found:
                integrity.append(f"realization {d.name} exists twice ({found[d.name]}, {d})")
            else:
                found[d.name] = d
    missing = sorted(set(declared) - set(found))
    ledger, escalate = [], []
    for rid in sorted(found):
        run, decl = found[rid], declared[rid]
        try:
            ident = core70.load_json(run / "run-identity.json")
            summary = core70.load_json(run / "summary.json")
        except core70.ContractError as exc:
            integrity.append(f"{rid}: {exc}")
            continue
        acc = ident.get("accounting") or {}
        checks = {
            "purpose": acc.get("purpose") == "qualification",
            "campaign_record": acc.get("campaign_record_sha256") == manifest_sha,
            "execution_mode": ident.get("execution_mode") == "qualification",
            "admission_bound": bool(ident.get("profile_admission_sha256")),
            "profile_key": ident.get("profile_key_sha256") == decl["profile_key_sha256"],
            "entry_stratum": ident.get("entry_stratum") == decl["entry_stratum"],
            "corpus": manifest["scope_id"] == SCOPE_PREFIX + str(ident.get("corpus_manifest_sha256")),
        }
        integrity += [f"{rid}: {name} mismatch" for name, ok in checks.items() if not ok]
        events = _events(run)
        term = next((e["payload"] for e in events if e.get("kind") == "termination"), {})
        usage = next((e["payload"] for e in events if e.get("kind") == "usage_timing"), {})
        roots = [e["payload"].get("logical_root") for e in events if e.get("kind") == "root_selection"]
        row = {"id": rid, "stratum": decl["entry_stratum"], "key": decl["profile_key_sha256"][:12],
               "evidence_state": summary.get("evidence_state"), "termination": term.get("state"),
               "requests": usage.get("observer_request_count"), "wall_s": summary.get("wall_s"), "selected_roots": roots}
        if decl["entry_stratum"] == "deterministic":
            row["deterministic_activation"] = (summary.get("criteria") or {}).get("deterministic activation")
            if not ident.get("declared_root"):
                integrity.append(f"{rid}: deterministic run without a declared root")
            if row["deterministic_activation"] != "PASS":
                escalate.append(f"{rid}: deterministic activation {row['deterministic_activation']} (fails the profile; no rerun rescue)")
        else:
            ep = episodes.get(rid.rsplit("-", 2)[0], {})
            admissible = ep.get("admissible_roots") or []
            row["ordinary_group"] = "no-selection" if not roots else "admissible-root" if roots[0] in admissible else "wrong-root"
        if row["evidence_state"] != "COMPLETE_ADMISSIBLE":
            escalate.append(f"{rid}: evidence {row['evidence_state']} (termination {row['termination']})")
        if assessments is not None and row["evidence_state"] == "COMPLETE_ADMISSIBLE":
            candidates = [root / rid for root in assessments if (root / rid).is_dir()]
            arun = candidates[0] if len(candidates) == 1 else (assessments[0] / rid)
            if len(candidates) > 1:
                integrity.append(f"{rid}: assessed more than once ({candidates})")
            try:
                a = core70.load_json(arun / "assessment.json")
                aid = core70.load_json(arun / "assessment-identity.json")
            except core70.ContractError as exc:
                escalate.append(f"{rid}: assessment missing or unreadable ({exc})")
            else:
                row["assessment_status"] = a.get("assessment_status")
                if aid.get("run_identity_sha256") != ident.get("identity_sha256") or not aid.get("evaluator_admission_sha256"):
                    integrity.append(f"{rid}: assessment is not bound to this run and an admitted evaluator")
                if a.get("assessment_status") != "VALID":
                    escalate.append(f"{rid}: assessment {a.get('assessment_status')}")
                res: dict[str, int] = {}
                for disp in a.get("dispositions") or []:
                    res[disp.get("result")] = res.get(disp.get("result"), 0) + 1
                row["disposition_counts"] = res
        ledger.append(row)
    if missing:
        escalate.append(f"{len(missing)} declared realizations are missing")
    req = [r["requests"] for r in ledger if isinstance(r.get("requests"), int)]
    summary_counts: dict[str, dict[str, int]] = {}
    for r in ledger:
        for field in ("evidence_state", "termination", "ordinary_group", "deterministic_activation", "assessment_status"):
            if field in r:
                bucket = summary_counts.setdefault(f"{r['stratum']}:{field}", {})
                bucket[str(r[field])] = bucket.get(str(r[field]), 0) + 1
    return {"integrity": integrity, "escalate": escalate, "missing": missing, "declared": len(declared), "found": len(found),
            "counts": summary_counts,
            "requests_quantiles": statistics.quantiles(req, n=10) if len(req) >= 2 else req, "ledger": ledger}


def cmd_audit(args: argparse.Namespace) -> int:
    manifest = core70.load_json(args.accounting_manifest)
    result = audit_runs(args.runs, manifest, args.corpus, args.assessments)
    write_json(args.out, result)
    reasons = [f"INTEGRITY: {r}" for r in result["integrity"]] + [f"ESCALATE: {r}" for r in result["escalate"]]
    return emit("audit", reasons[:200], reasons_total=len(reasons), ledger=str(args.out), declared=result["declared"],
                found=result["found"], counts=result["counts"])


# --------------------------------------------------------------------------- set-freeze-gate
def set_freeze_gate(gate: Path, field: str, audit: Path | None) -> list[str]:
    state = core70.load_json(gate)
    if state.get(field) is not False:
        return [f"{field} is {state.get(field)!r}; it may only move from false to true once"]
    if field == "frozen_run_output_exists":
        if state.get("candidate_frozen") is not True:
            return ["candidate_frozen must be true before frozen run output can exist"]
        verdict = core70.load_json(audit) if audit and audit.is_file() else {}
        if verdict.get("command") != "audit" or verdict.get("verdict") != "PASS":
            return ["frozen_run_output_exists needs the PASS verdict JSON of the post-run audit (--audit)"]
    state[field] = True
    gate.write_text(json.dumps(state, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    return []


def cmd_set_freeze_gate(args: argparse.Namespace) -> int:
    return emit("set-freeze-gate", set_freeze_gate(args.gate, args.field, args.audit), gate=str(args.gate), field=args.field)


# --------------------------------------------------------------------------- CLI
def parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)
    p = sub.add_parser("derive-key", help="derive one family key profile from the frozen primary profile")
    p.add_argument("--source-profile", type=Path, required=True)
    p.add_argument("--source-capabilities", type=Path, required=True)
    p.add_argument("--panel", choices=KEY_PANELS, required=True)
    p.add_argument("--timeout-s", type=int, required=True)
    p.add_argument("--out-dir", type=Path, required=True)
    p.set_defaults(func=cmd_derive_key)
    p = sub.add_parser("family-build", help="assemble and validate the primary-family record")
    p.add_argument("--key", action="append", required=True, help="<panel>=<profile.json>:<capabilities.json>, once per key")
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_family_build)
    p = sub.add_parser("disclosed-build", help="byte-level denylist of disclosed corpora")
    p.add_argument("--corpus", type=Path, action="append", required=True)
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_disclosed_build)
    p = sub.add_parser("corpus-check", help="mechanical stratification/freshness/exposure gate on a custodian corpus")
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--requirements", type=Path, required=True)
    p.add_argument("--disclosed", type=Path, required=True)
    p.set_defaults(func=cmd_corpus_check)
    p = sub.add_parser("custody-stat", help="metadata-only snapshot of a custody store")
    p.add_argument("--store", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_custody_stat)
    p = sub.add_parser("custody-compare", help="compare two custody snapshots")
    p.add_argument("--before", type=Path, required=True)
    p.add_argument("--after", type=Path, required=True)
    p.add_argument("--append-only", action="append", help="store-relative path allowed only to grow (the access log)")
    p.set_defaults(func=cmd_custody_compare)
    p = sub.add_parser("prepare-arms", help="extract p65/p66/p71 packages from immutable refs and pin their digests")
    p.add_argument("--arm", action="append", required=True, help="<name>=<ref>:<version>")
    p.add_argument("--expect", action="append", required=True, help="<name>=<expected dist tree sha256>")
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_prepare_arms)
    p = sub.add_parser("campaign-build", help="build the frozen qualification accounting manifest")
    p.add_argument("--family", type=Path, required=True)
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--requirements", type=Path, required=True)
    p.add_argument("--arms-manifest", type=Path, required=True)
    p.add_argument("--lineage", type=Path, required=True)
    p.add_argument("--extra-offered", action="append", help="additional offered profile key (stakeholder decision only)")
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_campaign_build)
    for name, func in (("verify-launch", cmd_verify_launch), ("matrix-plan", cmd_matrix_plan)):
        p = sub.add_parser(name)
        p.add_argument("--accounting-manifest", type=Path, required=True)
        p.add_argument("--key", action="append", required=True)
        p.add_argument("--admission", action="append", required=True, help="<panel>=<profile-admission.json>, once per key")
        p.add_argument("--corpus", type=Path, required=True)
        p.add_argument("--arms-manifest", type=Path, required=True)
        if name == "verify-launch":
            p.add_argument("--freeze-gate", type=Path, required=True)
        else:
            p.add_argument("--requirements", type=Path, required=True)
            p.add_argument("--oracles", type=Path, required=True)
            p.add_argument("--out-root", type=Path, required=True)
            p.add_argument("--parallel", type=int, default=MAX_PARALLEL)
            p.add_argument("--out", type=Path, required=True)
        p.set_defaults(func=func)
    p = sub.add_parser("eval-plan", help="print the blinded-evaluator launch commands, one per key")
    p.add_argument("--accounting-manifest", type=Path, required=True)
    p.add_argument("--runs-root", type=Path, required=True)
    p.add_argument("--out-root", type=Path, required=True)
    p.add_argument("--keys", type=Path, required=True, help="custodian keys directory (passed to the evaluator; never opened here)")
    p.add_argument("--evaluator-profile", type=Path, required=True)
    p.add_argument("--evaluator-capabilities", type=Path, required=True)
    p.add_argument("--evaluator-admission", type=Path, required=True)
    p.add_argument("--parallel", type=int, default=MAX_PARALLEL)
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_eval_plan)
    p = sub.add_parser("audit", help="post-run (and post-assessment) completeness and integrity audit")
    p.add_argument("--runs", type=Path, action="append", required=True)
    p.add_argument("--accounting-manifest", type=Path, required=True)
    p.add_argument("--corpus", type=Path, required=True)
    p.add_argument("--assessments", type=Path, action="append", default=None, help="assessment output dir; once per key")
    p.add_argument("--out", type=Path, required=True)
    p.set_defaults(func=cmd_audit)
    p = sub.add_parser("set-freeze-gate", help="flip one FREEZE-GATE.json field to true, in order, never back")
    p.add_argument("--gate", type=Path, required=True)
    p.add_argument("--field", choices=("candidate_frozen", "frozen_run_output_exists"), required=True)
    p.add_argument("--audit", type=Path, help="required for frozen_run_output_exists: the PASS audit verdict JSON")
    p.set_defaults(func=cmd_set_freeze_gate)
    return ap


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    try:
        return args.func(args)
    except Stop as exc:
        return emit(args.command, exc.reasons, **exc.extra)
    except (core70.ContractError, OSError, KeyError, TypeError, ValueError, yaml.YAMLError) as exc:
        return emit(args.command, [f"{type(exc).__name__}: {exc}"])


if __name__ == "__main__":
    sys.exit(main())
