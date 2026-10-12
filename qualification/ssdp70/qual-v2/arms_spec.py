#!/usr/bin/env python3
"""Campaign arms specification shared by prepare_campaign, campaign_run, campaign_assess and build_campaign_record.

One JSON file, WORK/arms-spec.json (copied there by `prepare_campaign.py init --arms-spec F`), gives each arm's run-name, git ref, version,
h4 label (cand, b1, b2, b65), whether the evaluator assesses it, and per panel the arms that run it and the number of replicates:

  {"schema": 1,
   "arms": [{"name": "p721", "ref": "<commit>", "version": "7.2.1", "label": "cand", "assessed": true}, ...],
   "panels": {"main": {"arms": ["p721", "p72aa"], "replicates": 2}, "burden": {"arms": ["p721", "p72aa", "p65"]}, ...}}

`replicates` (default 1) is the number of identical command sets a panel runs. Set 0 is the ordinary plan (`main-c01` ...). Set k >= 1 repeats
the same chunks with the unchanged corpus manifest under the next command keys (`main-c09` ...); a replicate is identified by its command key,
never by a derived manifest. The runs of set k >= 1 keep the harness run names (`EP-001-p721-r0`) and are named `<command>/<run>` wherever
a run name must be unique (campaign record, dispositions). Set 0 keeps the bare run name.

Without a specification file the hardcoded 72b campaign applies (DEFAULT_SPEC), unchanged.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path

SPEC_NAME = "arms-spec.json"
LABEL_NAMES = ("cand", "b1", "b2", "b65")
CANDIDATE_REF = "2dedcfa3408f62bc11a696ac3776183a87b40438"
B_REF = "22f4bdba53795da3a6f13f162529f3a843fc37ae"       # accepted 6.6.0, PROTOCOL-RELEASE-STATE.yaml
OLD_REF = "7f7b5e24858e813e45ace867a7f8ea5180f43bf0"     # 6.5.0 public source, same file
_THREE = ["p72", "p66", "p66b"]
DEFAULT_SPEC = {
    "schema": 1,
    "arms": [{"name": "p72", "ref": CANDIDATE_REF, "version": "7.2.0", "label": "cand", "assessed": True},
             {"name": "p66", "ref": B_REF, "version": "6.6.0", "label": "b1", "assessed": True},
             {"name": "p66b", "ref": B_REF, "version": "6.6.0", "label": "b2", "assessed": True},
             {"name": "p65", "ref": OLD_REF, "version": "6.5.0", "label": "b65", "assessed": False}],
    "panels": {"main": {"arms": _THREE}, "routing": {"arms": _THREE}, "versioning": {"arms": _THREE}, "r2": {"arms": _THREE},
               "ordinary": {"arms": _THREE}, "burden": {"arms": ["p72", "p65"]}, "sentinels": {"arms": ["p72"]},
               "unversioned": {"arms": ["p72"]}},
}


class SpecError(ValueError):
    pass


def validate(spec: dict) -> dict:
    """Refuse a malformed specification; return it with defaults filled in (assessed False, replicates 1)."""
    if not isinstance(spec, dict) or spec.get("schema") != 1 or not isinstance(spec.get("arms"), list) or not isinstance(spec.get("panels"), dict):
        raise SpecError("arms specification must be an object with schema 1, an arms list and a panels object")
    spec = copy.deepcopy(spec)
    names, labels = [], []
    for arm in spec["arms"]:
        if not isinstance(arm, dict) or not all(isinstance(arm.get(k), str) and arm[k] for k in ("name", "ref", "version", "label")):
            raise SpecError(f"arm needs non-empty string name, ref, version and label: {arm!r}")
        if arm["label"] not in LABEL_NAMES:
            raise SpecError(f"arm {arm['name']}: h4 label {arm['label']!r} is not one of {LABEL_NAMES}")
        arm["assessed"] = bool(arm.get("assessed", False))
        names.append(arm["name"])
        labels.append(arm["label"])
    if len(set(names)) != len(names) or len(set(labels)) != len(labels):
        raise SpecError("arm names and h4 labels must each be unique")
    if "cand" not in labels:
        raise SpecError("the specification needs a cand arm")
    for panel, row in spec["panels"].items():
        if panel.endswith("-add") or not isinstance(row, dict) or not isinstance(row.get("arms"), list) or not row["arms"]:
            raise SpecError(f"panel {panel!r} needs an arms list (an -add panel inherits its base panel)")
        if not set(row["arms"]) <= set(names) or len(set(row["arms"])) != len(row["arms"]):
            raise SpecError(f"panel {panel!r} names arms outside the specification or repeats one")
        reps = row.get("replicates", 1)
        if not isinstance(reps, int) or isinstance(reps, bool) or reps < 1:
            raise SpecError(f"panel {panel!r}: replicates must be a positive integer")
        row["replicates"] = reps
    return spec


def load(work: Path | None) -> dict:
    """WORK/arms-spec.json if present, else the 72b defaults."""
    path = Path(work) / SPEC_NAME if work is not None else None
    if path is not None and path.is_file():
        return validate(json.loads(path.read_text(encoding="utf-8")))
    return validate(DEFAULT_SPEC)


def by_label(spec: dict) -> dict:
    """h4 label -> arm row."""
    return {a["label"]: a for a in spec["arms"]}


def label_of(spec: dict) -> dict:
    """run-name arm key -> h4 label."""
    return {a["name"]: a["label"] for a in spec["arms"]}


def name_of(spec: dict) -> dict:
    """h4 label -> run-name arm key (the declaration's `arms`)."""
    return {a["label"]: a["name"] for a in spec["arms"]}


def assessed(spec: dict) -> tuple:
    return tuple(a["name"] for a in spec["arms"] if a["assessed"])


def base_panel(panel: str) -> str:
    return panel[:-4] if panel.endswith("-add") else panel


def panel_arms(spec: dict, panel: str):
    row = spec["panels"].get(base_panel(panel))
    return list(row["arms"]) if row else None


def panel_sets(spec: dict, panel: str) -> int:
    row = spec["panels"].get(base_panel(panel))
    return row["replicates"] if row else 1


def run_id(name: str, command: str | None, set_index: int = 0) -> str:
    """The unique run id used in the campaign record and in disposition keys: the bare run name in set 0, `<command>/<name>` after."""
    return name if not set_index or not command else f"{command}/{name}"


def command_sets(work: Path) -> dict:
    """command key -> replicate set index, from WORK/commands.json (0 when absent or when the command has no `set`)."""
    path = Path(work) / "commands.json"
    if not path.is_file():
        return {}
    return {c["key"]: int(c.get("set", 0)) for c in json.loads(path.read_text(encoding="utf-8")).get("commands", [])}
