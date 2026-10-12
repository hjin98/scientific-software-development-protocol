# Project Engineering Memory

Own the agent-facing contract for **Project Engineering Memory (PEM)**: when project memory activates, how to retrieve it, how to decide and record applicability in a **Historical Applicability Set (HAS)**, how authority-bound capabilities differ from evidence-only learning, how counterevidence and uncertainty survive use, and when a durable memory update is justified. PEM is a compact project-local, evidence-backed, non-authoritative record of demonstrated recurring failures, successful patterns, discoveries, preservation capabilities and temporary notices. It helps a fresh-context engineer reuse project experience without turning history, statistics, reviews, tests, benchmarks or old mechanisms into D1-D4 authority.

Storage/governance mechanics—schema 1 fields, record/ledger shapes, maturity rules, assessment succession, derived statistics, summary rendering, partitioning, base/overlay publication, fork/rollback—are owned by the cold [Project Engineering Memory schema and governance](project-engineering-memory-schema.md) owner. Load it only when the current decision authors, changes, validates, partitions, migrates or restores memory records, reconciles accepted-base/overlay/publication state, or adjudicates a binding, maturity, recurrence, statistics or notice question. Ordinary consumption of memory does not load it.

## Authority boundary

```text
accepted D1-D4 / project / external authority -> what must be true
historical evidence                           -> what was observed
PEM                                            -> compact current learning representation
workplan/HAS                                   -> bounded cycle coordination
```

A test, benchmark, commit, review, count, temperature, maturity, or repeated historical success cannot promote a mechanism into authority. Memory temperature (`HOT`, `WARM`, `COLD`, `UNASSESSED`) is salience only—not authority, probability, applicability, acceptance or an activation command.

## When memory activates

Load PEM only when demonstrated project history can materially change the decision: substantial rework of mature D1-D4 semantics/concretization, replacement/consolidation of mature machinery, suspected recurrence, substantial optimization/scaling, migration/recovery/revert/restoration where prior choices matter, or an active workplan explicitly binding relevant memory.

A first clean local defect with no recurrence/generalization signal, ordinary documentation, trivial implementation, unrelated work, a long repository history, or the mere presence of `PROJECT-ENGINEERING-MEMORY.md` does not load memory.

## Retrieval and HAS

When triggered, use progressive disclosure:

```text
resolve accepted/base memory + explicit candidate overlay
 -> validate schema/publication state (project tooling where available)
 -> read the active summary
 -> search canonical family/notice metadata for owner/surface/mechanism/regime/applicability cues
 -> record HAS dispositions
 -> open matched family/detail rows
 -> follow raw evidence/history only where needed to decide or falsify a disposition
```

1. Resolve the **accepted/base PEM** from project integration/Git acceptance policy, never from default branch, latest, timestamp or self-declaration. Compose an explicit same-branch candidate overlay only after it validates; an overlay stays visibly candidate, cannot self-ratify, and cannot erase accepted entries by omission. Conflicting/partial composition is `REVIEW_REQUIRED`.
2. Match bounded current metadata over owner, surface, mechanism/capability, regime, project scope and task. Applicability is **not** restricted to the active summary or `HOT` entries: a `COLD`, `UNASSESSED` or summary-omitted entry may be decisive, and a prominent `HOT` entry outside the current owner/mechanism/regime is not applicable merely because it is prominent.
3. Record every materially relevant family/capability/notice surfaced or independently known, using the one canonical session-local HAS shape shared by workflow, template and validator:

```yaml
pem_basis:
  accepted_project_state: <exact accepted project state>
  accepted_pem: <exact accepted PEM publication or NONE_PROTOCOL_6.2_PRE_PEM>
  candidate_overlay_semantic_candidate: <exact candidate overlay or NONE>
has:
  - id: <family/capability/notice id>
    disposition: APPLICABLE | NOT_APPLICABLE | REVIEW_REQUIRED
    reason: <bounded rationale>
```

Do not substitute aliases such as `accepted_base` or `candidate_overlay`. Keep the HAS session-local unless the governed work explicitly needs a durable handoff/record.

4. When mature machinery is replaced, build a capability-transfer map: each demonstrated learned capability maps to its current authority binding and new mechanism, or to a justified omission/reclassification with acceptance evidence.
5. If the accepted memory basis, candidate overlay or a governing current owner materially advances before integration/closeout, inspect the changed interval/affected surface and refresh affected dispositions. A HAS derived from an obsolete basis cannot silently close current work.

**Missing memory is not absence.** Missing, malformed, unsupported, partial or stale memory—including a stale/missing derived index, stale applicability tags, an absent relation edge or an advanced `reconciled_through` watermark—cannot prove that no relevant lesson exists. For memory-triggering work on an established project, perform bounded historical intake over the affected scope or keep explicit `REVIEW_REQUIRED` uncertainty; do not turn that fallback into full-repository archaeology. Query/index/summary output is a derived view, never canonical memory. PEM is not a runtime/build single point of failure: unrelated routes stay usable.

## Using a lesson: authority binding, counterevidence, uncertainty

A `PRESERVATION_CAPABILITY` declares one binding:

- `EVIDENCE_ONLY` — demonstrated project property and replaceable design prior;
- `AUTHORITY_BOUND` — mandatory only because an exact current owner independently requires it; verify that the cited owner is still the real accepted owner for the exact claim, and treat an unhealthy/unavailable binding as `REVIEW_REQUIRED`, not as retained force;
- `PROPOSED_FOR_PROMOTION` — evidence suggests the real owner may need amendment; not mandatory until that owner accepts it.

Use a lesson at the claim strength it actually carries. `OBSERVED/WORKS` is an absolute outcome in a stated regime; `RECOMMENDED` is an eligible instinct within stated limits; `PREFERRED/DEFAULT/BEST` requires comparative evidence over viable alternatives or explicit current-owner priority. Positive guidance is usable only while the entry is `CURRENT`, adequately mature for its wording, healthily bound, and free of unresolved material contradiction in the stated regime. Keep neutral/contradicting/inconclusive evidence, unhealthy bindings and contested overlaps visible; two current patterns recommending incompatible actions need a regime/tradeoff predicate or current-owner priority, otherwise they stay contested. A memory pattern is a design prior, not an instruction to copy the old implementation.

During Review, PEM is a high-information hypothesis index, not proof: independently verify current owner, applicability, assembled candidate and evidence.

## When a durable update is justified

After an accepted material repair/rework/optimization/revert/restoration, perform the **closeout learning assessment** before declaring lifecycle closure. Ask whether a known failure family genuinely recurred after accepted repair; a success pattern gained a supporting, neutral, contradicting, inconclusive, rejected/invalid application episode; an episode is genuinely new rather than another surface/run of one coordinated intervention; a material evidence provenance cluster limits independence; a reusable discovery/capability emerged; evidence narrowed/retired/invalidated an existing lesson; maturity/comparative claim strength changed; overlapping guidance acquired a conflict/tradeoff boundary; coverage/aggregation/project scope or binding health changed; a notice expired; causal attribution changed; a PEM dependency or accepted-memory basis advanced; or schema/base/overlay reconciliation is needed.

Update PEM only when an admission threshold is met or an existing current entry materially changes; then load the schema/governance owner and publish root plus affected partitions coherently against the exact accepted-base/overlay state. Ordinary fix chronology and first-clean local defects stay in Git/native evidence. Documentation, audit or orchestration may surface candidates, but the substantive owner and admissible evidence govern the update; no specialist can self-promote a finding, declare `AUTHORITY_BOUND`, or adjudicate a material evidence conflict. When a project lesson becomes generic accepted doctrine at its real owner, retire duplicate active guidance and keep only project-specific evidence that still changes decisions.

## Scope and portability

The default discovery root is `PROJECT-ENGINEERING-MEMORY.md` at the governed project root unless project authority declares an alternative. A generic package/profile contains this doctrine, its schema owner and the template, never a live project's memory. Copying/forking memory does not manufacture local incidence; inherited entries are external/historical evidence until project governance reconciles lineage. Version-bound work under a protocol predating PEM leaves a later memory inert rather than reinterpreting it. Preserve secret/private-data boundaries when reading or updating memory.
