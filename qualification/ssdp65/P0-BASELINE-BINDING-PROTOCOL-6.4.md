---
kind: ssdp65-frozen-control-binding
investigation: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
governing_protocol_version: 6.4.0
authority: non-normative-experimental-control-binding
p0_protocol: 6.4.0
p0_repository_state: 55c085261eb827e3047637d045a8e6917ea6b962
p0_accepted_recovery: 74bc572ef516cae417437a2027eeff52a2e25c15
p0_public_bootstrap: e09a9d1480211eea2d16d722182bb5c6de1bee12
p0_recovery_mapping_descendant: 6e66478f37de197b6d28707e087c61d687fcfa41
p0_stage_f_run: 35153901722
historical_rollback_6_3: 9f353097fab36e325a325f1c2f9d9cec32e86177
successor_branch: ssdp-6.5-frontier-model-re-evaluation
created: 2026-09-24
---

# P0 — Frozen Protocol 6.4 Control Binding

## Purpose

This record binds the experimental control `P0 = P_6.4` for the Protocol 6.5 frontier-model re-evaluation. It is evidence/coordination state, not protocol authority. It must not be edited after the Phase-I–III diagnostic commit except to append a clearly dated correction whose reason is recorded (see `BENCHMARK-AND-EVALUATION-DESIGN.md` §8).

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** separates D1 scientific/mathematical formulation, D2 algorithm/numerical method, D3 software architecture and D4 specification/implementation authority. A **recovery** identity is the immutable commit accepted for rollback of a protocol version. A **public-source bootstrap** is the immutable commit an agent may fetch as version-bound fallback source when no compatible local source exists. A **mapping descendant** is a later commit that publishes an identity, because a Git commit cannot name its own hash.

## Bound identities (verified 2026-09-24 against the full, unshallowed clone)

| Role | Identity | Verification |
| --- | --- | --- |
| Accepted Protocol 6.4 recovery | `74bc572ef516cae417437a2027eeff52a2e25c15` ("Record Protocol 6.4 independent Review PASS", 2026-09-16) | commit exists; ancestor of P0 state |
| Protocol 6.4 public-source bootstrap (distinct) | `e09a9d1480211eea2d16d722182bb5c6de1bee12` ("Add Protocol 6.4 QF64 counterfactual qualification", 2026-09-15) | commit exists; ancestor of recovery and P0 state |
| Recovery-mapping descendant | `6e66478f37de197b6d28707e087c61d687fcfa41` | commit exists; ancestor of P0 state |
| **P0 repository state (experimental control)** | `55c085261eb827e3047637d045a8e6917ea6b962` = `main` = merge of PR #32, containing Stage-F closeout | tip of `origin/main` and of this branch at creation |
| Protocol 6.3 historical rollback | `9f353097fab36e325a325f1c2f9d9cec32e86177` | ancestor of P0 state |
| `source/PROTOCOL_VERSION` at P0 | `6.4.0` | read directly |

### Why P0 is the repository state and not the recovery commit

`74bc572` is the accepted rollback identity, but it predates Stage-F cutover. Between `74bc572` and `55c0852` only three canonical `source/` files changed (`source/README.md`, `source/SEMANTIC_DEPENDENCIES.md`, `source/shared/references/protocol-versioning-and-compatibility.md`), all of them lifecycle/version-identity text (24 insertions, 14 deletions). No D1–D4, evidence, PEM, representation or routing doctrine changed. P0 is therefore the *assembled accepted-current state as actually deployed*, which is what a fresh agent on `main` would load; the recovery commit remains the version-bound rollback identity. Both are recorded so that any later comparison can use either, and the difference is itself a diagnostic observation (see reviewer findings).

The bootstrap `e09a9d1` and recovery `74bc572` are distinct commits. The content relationship between them is part of the subject under review and is deliberately not characterized in this shared binding.

## Canonical-source classification at P0

| Artifact | Class | Notes |
| --- | --- | --- |
| `source/roles/*/SKILL.md`, `source/specialists/*/SKILL.md` | canonical (role/specialist entrypoints, root routing) | frontmatter `description` fields are the runtime skill-selection text |
| `source/shared/references/*.md` | canonical (kernel, D1–D4 domain owners, concern owners) | kernel = `abstraction-and-concretization.md` |
| `source/shared/templates/*.md` | canonical (operational templates) | D1/D2 paper templates self-label "Protocol 6.1" |
| `source/PROTOCOL_VERSION` | canonical version identity | `6.4.0` |
| `source/project_engineering_memory.py` | canonical executable PEM validator (declared a concretization of documented schema) | |
| `source/build_skills.py`, `validate_packages.py`, `check_dist.py` | canonical build/validation tooling | |
| `source/README.md`, `source/SEMANTIC_DEPENDENCIES.md` | canonical-tree navigation / declared derived dependency view | declared non-authoritative |
| `source/shared/references/development-workflow-prompts.md` | canonical human-facing orchestration source | parsed into machine profile |
| `dist/skills/*`, `dist/*.zip`, `dist/BUILD_INDEX.json` | generated | parity checked by `check_dist.py` |
| `orchestrator/src/sdp_orchestrator/core/resources/protocol/ssdp-protocol-6.4/*` | generated (current snapshot) | parity checked by snapshot `--check` |
| `orchestrator/.../ssdp-protocol-{5.16,6.0,6.1,6.2,6.3}/*` | frozen historical (byte-pinned) | |
| `AGENTS.md` | project instruction (harness-injected), restates doctrine | outside `source/` |
| `README.md`, `PORTABILITY.md` | human-facing explanatory | |
| `PROJECT-ENGINEERING-MEMORY.md` | project-local state (self-hosted PEM), never packaged | |
| `history/SEMANTIC_EVOLUTION.md` | historical explanation | |
| `workplans/active/*`, `workplans/archive/*` | coordination authority for bounded cycles / historical | |
| `qualification/**` | qualification evidence / review records | |
| `tests/*.py`, `orchestrator/tests/*` | executable evidence specifications | |

## Baseline acceptance realization (fresh, this session)

Executed on P0 `55c0852` in an isolated virtual environment (Python 3.11.15, `PyYAML==6.0.2`, orchestrator + dev requirements):

| Documented acceptance step | Result |
| --- | --- |
| `python -m unittest discover -s tests` | 249 tests, OK (3 skipped) |
| `python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md` | `PEM schema 1 valid: 3 families, 0 notices` |
| `python source/build_skills.py --output <scratch>` | built 7 skills + ZIPs |
| `python source/validate_packages.py --dist <scratch>` | all bundles/ZIPs structurally valid |
| `python source/check_dist.py --expected <scratch> --committed dist` | committed dist matches fresh build |
| `git diff --check` | clean |
| `python orchestrator/scripts/generate_protocol_snapshot.py --check` | 6.4 snapshot matches source; 5.16–6.3 frozen |
| `python orchestrator/scripts/run_core_tests.py` | 382 tests across 12 modules, OK |

CI (`.github/workflows/protocol-check.yml`) runs the same steps on Python 3.12 except the standalone PEM validator command. This realization is evidence about P0 at `55c0852` only.

## Immutability rule for the experiment

- `P0` is `55c0852` (assembled accepted-current) with version-bound rollback `74bc572`. Neither is altered by this investigation.
- Any candidate `P1` is developed only on `ssdp-6.5-frontier-model-re-evaluation` and compared against `P0` by the pre-registered design in `BENCHMARK-AND-EVALUATION-DESIGN.md`.
- The diagnostic pass (Phases I–III) does not modify `source/`, `dist/`, orchestrator resources, frozen profiles, `AGENTS.md`, `README.md`, `PROJECT-ENGINEERING-MEMORY.md`, or any archived artifact.
