# Scientific Software Development Protocol

Current accepted document-controlled release: **Protocol 6.3**. Accepted recovery is `9f353097fab36e325a325f1c2f9d9cec32e86177` and the distinct immutable public-source bootstrap is `86c13cab6bdd1991dffa94e277db8eacf87e2e11`. Protocol 6.2 recovery `b59adc77efe6951912cfd705cc43830c58ca27d0` remains immutable historical rollback for explicitly version-bound 6.2 work. Protocol 7 remains a proposed deterministic-control-plane successor and is not cut over.

## Core model

The Scientific Software Development Protocol (SSDP) separates four semantic authority domains:

```text
D1 scientific/mathematical formulation
 -> D2 algorithm/numerical method
 -> D3 software architecture
 -> D4 specification/implementation
```

This is a semantic hierarchy, not a mandatory waterfall. A child concretization must preserve every applicable parent abstraction and directly governed external constraint. Among admissible concretizations prefer domain engineering fitness, then minimum justified total complexity, then development economy.

The universal current kernel is `source/shared/references/abstraction-and-concretization.md`. Role entrypoints route progressively to concern owners rather than loading the complete reference library up front.

## Protocol 6.3 project engineering memory

Protocol 6.3 adds **Project Engineering Memory (PEM)** as evidence-backed, project-local decision support. PEM is not D5 and cannot become authority through frequency, successful history, temperature, maturity, documentation, or package placement. Current D1-D4/project/external owners remain authoritative.

PEM is conditionally activated only when demonstrated project history can materially change the decision—for example substantial mature rework/replacement, suspected recurrence, substantial optimization/scaling, or migration/recovery/revert/restoration. A first clean local defect or unrelated task keeps memory cold. When activated, the workflow resolves the exact accepted/base memory and validated branch overlay, searches canonical metadata for applicable entries regardless of temperature, and records task-local dispositions in a Historical Applicability Set (HAS).

The canonical doctrine owner is `source/shared/references/project-engineering-memory.md`; the human-editable schema-1 template is `source/shared/templates/project_engineering_memory_template.md`. This repository's self-hosted `PROJECT-ENGINEERING-MEMORY.md` is deliberately partial candidate project state backed by immutable evidence and is **not** copied into generic skills, distributions, profiles, or snapshots.

Current statistics are derived from current admissible assessments while historical observations remain recoverable. Stable family IDs represent semantic identity; temperature is salience rather than applicability/authority; maturity is claim-relative evidence strength; comparative/default/best guidance requires genuine comparator evidence or real-owner priority. Evidence and memory text are data, not instruction/authorization channels.

## Lossless representation and routing

Protocol 6.3 preserves all accepted Protocol 6.2 doctrine and still-valid historical capability while adding project-learning support. Among lossless representations prefer semantic correctness/completeness, precision, importance-weighted attention, cognitive digestibility, context/routing efficiency, then compactness. A writer may not shrink governed scope, hide a mandatory lower-salience constraint, or remove globally required doctrine merely because it is cold for one task.

Activation is explicit and typed:

```text
task/orchestration
 -> role or specialist SKILL.md
      -> universal kernel + owning domain
      -> conditional concern owner
           -> conditional concern-local leaf
```

Ordinary Markdown links, semantic dependencies, PEM relations/indexes, and package membership do not themselves activate context. Router prose remains authoritative; graphs/traces/summaries/indexes are derived aids.

## Roles and specialists

Authority-bearing roles are `scientific-formulation` (D1), `numerical-algorithm-design` (D2), `software-design` (D3), and `software-implementation` (D4). Optional `software-documentation`, `software-maintenance-audit`, and `repository-hygiene` specialists support the lifecycle but cannot create approval authority or self-promote project-memory findings.

Current human-facing documents define newly introduced non-common terminology for their intended competent reader and expand non-obvious abbreviations on first explanatory use (`full term (ABC)`). Current documents explain present truth; PEM summarizes bounded reusable project learning; semantic history explains why material semantics changed.

## Version compatibility

Frozen accepted historical mappings remain immutable:

```text
5.16.0 -> e151daaf5c8eebb351a85cfed86170fda80fb5e3
6.0.0  -> 21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2
6.1.0  -> 802e75af261efb4f70d71284d860613a2197b639
6.2.0  -> b59adc77efe6951912cfd705cc43830c58ca27d0
6.3.0  -> 9f353097fab36e325a325f1c2f9d9cec32e86177
```

Protocol 6.2 public-source bootstrap remains **`5a062ebc472755607b9dc66d33a5ebbc4b7429aa`** for version-bound 6.2 work. The earlier `1181c2031710c5d343194d87d08543290fded0ab` attempt remains invalidated historical evidence only. Bootstrap and recovery identities are intentionally distinct.

**Earlier Protocol 6.3 bootstrap attempts `1484c1d3caa49d87cc15bc52a5e775399c1dae1b`, `5ee4b3ac3ca1666b0499f7a72f55adcc411bf4bb`, owner-binding-invalidated `e12572c021087308570abfa41657a910c6896457`, and D4R3 snapshot `dc22f09fd38dbbfeaeb0160152da9b284654f66e` are historical only. Current authorized version-bound 6.3 public fallback is bootstrap `86c13cab6bdd1991dffa94e277db8eacf87e2e11`; accepted recovery is `9f353097fab36e325a325f1c2f9d9cec32e86177`; bootstrap and recovery are intentionally distinct.** Bootstrap mapping descendant `a8dac814cc2813b3bb336e5b6abde5fbcf44949e`, recovery mapping descendant `0c76c0461b7376f17182d29ba145a198a092463c`, and generated reconciliation `e75282ae850b774a9466902f4c74ba6a179116bd` preserve self-reference-safe publication. Stage G acceptance passed in run `34699052516`.

## Canonical source and acceptance

`source/` is canonical. `dist/skills/`, top-level skill ZIPs, and orchestrator protocol resources are generated/packaged descendants. Live `PROJECT-ENGINEERING-MEMORY.md` is project state and is excluded from those generic outputs.

```bash
python -m pip install -r source/requirements-validation.txt
python -m unittest discover -s tests -v
python source/project_engineering_memory.py PROJECT-ENGINEERING-MEMORY.md
python source/build_skills.py --output /tmp/protocol-dist
python source/validate_packages.py --dist /tmp/protocol-dist
python source/check_dist.py --expected /tmp/protocol-dist --committed dist
git diff --check

python -m pip install ./orchestrator -r orchestrator/requirements-dev.txt
python orchestrator/scripts/generate_protocol_snapshot.py --check
python orchestrator/scripts/run_core_tests.py
```

Protocol 6.3 additionally requires inherited scenarios 1-115, Q63/F63 counterfactual qualification, static routing/package sensors, the workplan's falsification passes, independent assembled-candidate D3/Protocol Review, then self-reference-safe recovery mapping and regenerated Core/package parity. A governing Serious Challenge or required unexecuted check blocks closure.
