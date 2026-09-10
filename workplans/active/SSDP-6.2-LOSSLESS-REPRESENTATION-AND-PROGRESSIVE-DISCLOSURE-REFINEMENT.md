---
kind: abstraction-concretization-change-plan
workplan_id: SSDP-6.2-LOSSLESS-REPRESENTATION-AND-PROGRESSIVE-DISCLOSURE-REFINEMENT
protocol_version: 6.1.0
target_protocol_version: 6.2.0
status: proposed
created_date: 2026-09-10
active_serious_challenge: none
parent_semantic_baseline: cec29671b9db59d20124a6e2ce99725ed60b8f0a
parent_protocol_61_recovery: 802e75af261efb4f70d71284d860613a2197b639
---

# SSDP 6.2 Lossless Representation and Progressive-Disclosure Refinement

## Background and terminology

The Scientific Software Development Protocol (SSDP) is intentionally thorough: it preserves scientific, numerical, architectural, implementation, evidence, challenge, validation, maintenance, and historical semantics across D1-D4. Protocol 6.2 addresses a different problem: a semantically complete protocol can still become harder for an agent or human to execute correctly when the same ideas are repeatedly restated, routing paths become deep or combinatorial, historical revisions remain on the active reasoning path, or low-importance material competes for attention with governing decisions.

For this plan:

- **representation** means any human- or agent-facing form used to communicate, preserve, route, summarize, or hand off governed information, including skills, reference documents, prompts, workplans, handoffs, specifications, method papers, architecture manuals, evidence/review/qualification records, semantic-dependency/evolution records, guides, runbooks, and compact resumable state;
- **lossless representation** means a representation from which every material semantic element required for its intended scope remains recoverable and correctly interpretable, including governing invariants, constraints, authority state, uncertainty, evidence qualification, exceptions, dependencies, non-goals, and reopen conditions;
- **representation hot path** means the information normally loaded or presented to make the current decision; **cold path** means recoverable detail such as historical lineage or supporting rationale that remains available but is not loaded unless materially relevant;
- **progressive disclosure** means loading or presenting additional doctrine only when the current semantic question triggers it;
- **activation dependency** means a reference that must be read to make a named decision correctly; an ordinary explanatory cross-reference, semantic dependency, or package-transport dependency is not automatically an activation dependency;
- **attention balance** means allocating prominence and active context in proportion to consequence, uncertainty, risk, and immediate decision relevance rather than giving every fact equal cognitive weight.

The target is not minimum character count. Extreme abbreviation, excessive indirection, fragmented prose, hidden prerequisites, or over-compression can increase cognitive strain. The target is the minimum complete, precise, readily interpretable representation.

## 1. Target outcome and authority

### Problem / stakeholder outcome

Protocol 6.1 is semantically coherent and passed its accepted behavioral qualification, but accumulated representation and routing complexity can impose unnecessary context cost and maintenance synchronization debt. A representative substantial D3 Review currently routes through `software-design/SKILL.md` plus the abstraction/concretization kernel, workflow, evidence/dependency, architecture, testing, versioning, and long-horizon references before task-specific language/tool/domain material. Those files total roughly 112 kB of Markdown before the workplan, code, tests, repository evidence, or user request are considered. The equivalent Protocol 6.0 core was roughly 80 kB. Physical distribution size is not itself a defect; the concern is active-context load, repeated doctrine, salience dilution, deep routing, and long-term drift.

Protocol 6.2 SHALL preserve the full semantic sophistication of Protocol 6.1 and all still-valid historical improvements while making their representation terser, more precise, more importance-weighted, easier to digest, shallower to route, and cheaper in active context.

### Governing parent authority

- accepted Protocol 6.1 closeout baseline: `cec29671b9db59d20124a6e2ce99725ed60b8f0a`;
- accepted Protocol 6.1 recovery: `802e75af261efb4f70d71284d860613a2197b639`;
- immutable Protocol 6.0 recovery: `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2`;
- immutable Protocol 5.16 recovery: `e151daaf5c8eebb351a85cfed86170fda80fb5e3`;
- current 95-scenario Protocol 6.1 qualification and current static/package/orchestrator regression evidence;
- `history/SEMANTIC_EVOLUTION.md` and accepted archived workplans as historical rationale, not parallel current authority.

The new rule is a backward-compatible strengthening of how governing information is represented and routed. It does not weaken D1-D4 authority, evidence requirements, Serious Challenge semantics, human ratification, testing, active simplicity, or any other accepted Protocol 6.1 capability.

### Highest affected authority / implementation surfaces

This is a protocol-wide representation-doctrine refinement with D3/D4 consequences for documentation/routing/package/profile structure. It does not reopen scientific D1 or numerical D2 meaning merely because D1/D2 artifacts must obey the new representation rule.

### Non-goals

- reducing ZIP or repository size for its own sake;
- weakening or deleting a doctrine because it is verbose;
- replacing precise domain terminology with vague summaries;
- introducing a universal knowledge graph, routing database, context manager, or new approval role merely to enforce compactness;
- forcing exact token/paragraph quotas independent of semantic need;
- rewriting frozen Protocol 5.16, 6.0, or 6.1 historical artifacts;
- implementing Protocol 7 control-plane machinery.

## 2. Governing invariants and the Protocol 6.2 representation rule

### 2.1 No-loss prerequisite

Information completeness is a hard admissibility condition, not an optimization objective.

A representation `R` of governed information `S` is admissible only when a competent intended reader/agent can recover every material semantic element of `S` required for the artifact's declared scope and interpret it correctly without hidden chat, unavailable history, or unstated prerequisites.

No compaction may remove a distinct accepted capability, invariant, constraint, uncertainty, exception, evidence qualification, authority-state distinction, compatibility obligation, or reopen condition. A historical improvement may disappear as separate prose only when its behavior is demonstrably preserved by an equal or stronger generalized current rule and the historical reason remains recoverable where material.

### 2.2 Representation optimization order

Among lossless admissible representations, prefer in order:

```text
semantic correctness and completeness
> semantic precision and unambiguity
> importance-weighted attention
> cognitive digestibility
> context and routing efficiency
> representational compactness
```

Compactness may never trade against completeness. Conversely, once completeness is secured, avoidable verbosity, repeated generic doctrine, unnecessary history replay, gratuitous routing depth, and equal prominence for unequal concerns are representation defects.

### 2.3 Lossless Representation Rule

For every governed communication surface:

1. **Say each generic rule fully once at its canonical owner.** Secondary artifacts route to that owner and state only their local/domain-specific consequence unless a short local restatement materially improves standalone interpretation.
2. **Generalize rather than accumulate.** When a later improvement strengthens an earlier rule, rewrite the current rule into the strongest coherent general form instead of preserving amendment-style layers in the hot path. Preserve material supersession rationale in semantic history.
3. **Prefer local delta over repeated doctrine.** A role, handoff, workplan, report, or guide should carry what is specific to its decision plus the minimum context required to interpret it; generic protocol doctrine should be referenced, not recopied.
4. **Use progressive disclosure.** Load or present doctrine when a material semantic question triggers it. Being potentially relevant to the broad task class is insufficient by itself for unconditional loading.
5. **Keep routing shallow and typed by purpose.** Distinguish activation dependencies from ordinary explanatory cross-links, semantic dependencies, evidence execution dependencies, and package transport closure. A Markdown link does not by itself create a runtime reading obligation.
6. **Reuse established context.** Do not repeatedly reload unchanged governing material in one task merely to restate it; re-read exact authority when a new question depends on precise wording or evidence may have invalidated the prior interpretation.
7. **Balance attention by consequence.** Serious Challenges, safety/governing constraints, current authority, blockers, uncertain high-impact claims, and required next decisions receive greater prominence than routine mechanics, supporting provenance, or historical narrative.
8. **Separate current truth from historical explanation.** Current artifacts must explain the accepted present coherently. Detailed chronology and supersession rationale remain recoverable off the normal execution path unless history is itself material to the task.
9. **Minimize inferential burden, not merely text.** Do not replace a clear local statement with a long chain of references when a concise restatement costs less total attention. Do not fragment one coherent concept across many files solely to reduce file length.
10. **Preserve evidence visibility.** Compression may summarize large evidence, logs, or review material, but it must not hide warnings, failures, uncertainty, contradictory admissible evidence, unavailable required checks, or the provenance needed to interpret a material claim.

The rule applies to skills, prompts, workplans/handoffs, records, current normative documents, documentation, reviews, qualification outputs, and agent-generated communication. Machine data and immutable raw evidence need not be rewritten for prose compactness; human/agent representations of their meaning must follow the rule.

## 3. Baseline scan and refinement targets

The Protocol 6.1 scan found no Serious Challenge to the core semantic model. It did find representation overlap and routing load that Protocol 6.2 should normalize.

### 3.1 Governing kernel

Current `source/shared/references/abstraction-and-realization.md` is already the strongest candidate for the universal semantic kernel. Its current filename, however, retains obsolete current terminology solely as a 6.0 compatibility path while Protocol 6.1 prose uses abstraction/concretization.

Protocol 6.2 SHALL rename the current canonical reference to:

`source/shared/references/abstraction-and-concretization.md`

Update all current 6.2 links, package routes, dependency views, tests, documentation, prompts, and generated 6.2 resources accordingly. Do not rewrite frozen 5.16/6.0/6.1 artifacts. Do not add a current alias/wrapper merely to preserve the old path unless an actual supported current consumer contract requires it. Historical releases already preserve the prior filename.

Also audit other current filenames that retain `realization` where they mean semantic concretization, including `abstraction_realization_change_plan_template.md`. Rename current 6.2 identifiers when no supported current compatibility contract requires the legacy spelling; preserve frozen historical paths rather than carrying obsolete terminology forward as new compatibility machinery.

Add the Lossless Representation Rule to the renamed semantic kernel so it becomes a protocol-wide invariant without adding another mandatory reference file.

### 3.2 Skills as decision routers

Current role/specialist `SKILL.md` files contain both routing and sizeable restatements of evidence, convergence, challenge, authority, and documentation doctrine. Refactor each entrypoint toward:

```text
ownership / activation boundary
+ minimal standalone background
+ always-required semantic kernel
+ direct conditional routing table
+ role-specific method/delta
+ role-specific completion contract
```

A skill should not independently reteach complete generic evidence, convergence, testing, versioning, or Challenge doctrine when a canonical owner exists. Preserve short local consequences where they prevent incorrect inference.

Review every `MUST read` edge. Retain unconditional reads only when the named role cannot make its ordinary substantive decision safely without that document. Convert broad potentially-relevant reads into decision-triggered conditional routes. Avoid transitive activation: secondary reference links do not automatically require another read unless the current question explicitly triggers it.

### 3.3 Canonical reference-owner normalization

Preserve one complete detailed owner for each generic concern. Current intended ownership includes at least:

```text
universal abstraction/concretization/authority/challenge/representation
  -> abstraction-and-concretization.md
workflow/handoff/stage semantics
  -> workflow-and-workplans.md
evidence lifecycle/applicability/evolution/dependencies
  -> evidence-evolution-and-dependencies.md
testing/validation/oracle methodology
  -> testing-and-validation.md
D3 architecture
  -> architecture-and-design.md
recurrence/simplification/development-cycle economy
  -> convergence-and-cycle-economy.md
longitudinal maintenance/stabilization/health sensing
  -> long-horizon-code-health.md
version selection/recovery/current compatibility
  -> protocol-versioning-and-compatibility.md
human/scientific technical writing
  -> scientific-technical-writing.md
document authority/current-vs-history/source-chain maintenance
  -> documentation-maintenance.md
repository inspection/context economy
  -> repository-intake.md
```

Refactor secondary documents to reference the owner plus their local consequence. In particular:

- remove repeated full evidence-lifecycle/applicability doctrine from testing, workflow, D1-D4 skills, and documentation where a concise consequence plus evidence-owner route is sufficient;
- keep testing-specific oracle, proxy-proof, regression, integration, failure-path, and qualification semantics in `testing-and-validation.md`;
- keep recurrence/family/simplification doctrine in `convergence-and-cycle-economy.md`; reduce repeated generic restatements in workflow, architecture, D3/D4 skills, and long-horizon health to local consequences;
- keep the complete Serious Challenge model in the universal kernel; secondary artifacts state only the threshold/routing consequence they need;
- separate long-horizon sensing/stabilization semantics from generic recurrence/simplification so the two owners do not maintain parallel versions of the same rule;
- ensure documentation-and-evidence, documentation-maintenance, and scientific-technical-writing have non-overlapping primary responsibilities and inherit the universal representation rule rather than independently restating it.

Do not mechanically deduplicate text. Similar wording may encode different domain consequences; preserve distinct semantics. Conversely, textually different paragraphs that carry the same generic rule should not survive merely because they use different wording.

### 3.4 Workplans, handoffs, records, and resumable state

A snapshot-complete handoff remains mandatory, but snapshot completeness does not require copying generic protocol doctrine. Refactor templates and guidance so a handoff carries:

- task-specific governing invariants and side constraints;
- cycle-scoped accepted decisions;
- delegated space/non-goals;
- material evidence/dependency/uncertainty state;
- blockers/Serious Challenges/human-pending state;
- acceptance/reopen conditions;
- direct references to generic protocol owners where necessary.

Chronology, superseded attempts, closed findings, and raw evidence detail stay out of the active handoff unless they materially constrain the next decision. Preserve material historical rationale in semantic evolution/history and evidence in its native artifact.

Review/qualification/audit records should lead with current disposition and decision-critical findings, then supporting evidence, then historical/provenance detail. A concise summary must remain lossless for the claimed decision scope; supporting detail may remain linked rather than repeated.

### 3.5 Human-facing technical documents

Keep `scientific-technical-writing.md` as the human/scientific writing specialization. Extend it only with consequences of the universal representation rule that are specific to technical exposition: information hierarchy, concise background, definitions near use, coherent section structure, elimination of amendment-style prose, and importance-weighted presentation.

Do not duplicate the universal rule in full. Existing background/terminology and first-use abbreviation requirements remain fully binding.

### 3.6 Repository intake and active context

`repository-intake.md` already contains strong progressive-inspection and context-economy principles. Generalize those principles through the kernel while keeping repository-specific inspection mechanics local.

Add a task-context rule: once a governing fact has been established from a current source, retain it as working context until a material question requires exact reread or later evidence plausibly invalidates it. Prefer targeted sections/ranges and discriminating evidence over repeated whole-document loading.

### 3.7 Workflow prompts

`development-workflow-prompts.md` already demonstrates useful deduplication by defining public-source resolution once for all stages. Apply the same architecture to other cross-stage contracts:

- keep one shared execution/authority/evidence/representation contract;
- make stage blocks primarily stage-specific inputs, ownership, actions, outputs, and stop/routing conditions;
- remove repeated generic explanations that are already guaranteed by the shared contract or canonical owner;
- preserve each stage as independently executable once the shared preamble is supplied;
- ensure human-facing prompt entrypoints make high-impact state and required inputs more salient than boilerplate.

### 3.8 Versioning and history

Keep current version-selection/recovery behavior compact and operational. Detailed Protocol 5.x/6.0/6.1 lineage must remain recoverable but should not be forced into ordinary current-version execution context unless historical compatibility, migration, or archaeology is relevant.

Prefer a current operational versioning section plus clearly separated historical lineage/cold-path material. Do not remove immutable recovery identities or the semantic mapping needed to interpret historical work.

### 3.9 Semantic-dependency and package topology

`source/SEMANTIC_DEPENDENCIES.md` should distinguish at least conceptually among:

- semantic authority/dependency relationships;
- activation/read prerequisites;
- evidence target/execution dependency relationships;
- generated/source-chain relationships;
- package transport closure.

Do not infer one relationship from another merely because both are expressed by Markdown links.

The self-contained package contract may retain bounded transitive Markdown transport closure if that remains the simplest reliable packaging solution; physical duplication is not the target of this work. Runtime activation and context loading, however, must remain controlled by explicit role/task routes rather than package membership or transitive hyperlinks.

Avoid inventing a graph/database/schema unless existing Markdown structure and tests cannot express the required distinctions reliably.

## 4. Preservation contract: losslessness before compaction

### 4.1 Semantic capability inventory

Before substantive refactoring, construct a bounded implementation-time preservation inventory from:

- every current Protocol 6.1 canonical owner and role/specialist obligation;
- the 95 accepted Protocol 6.1 behavioral scenarios;
- current static route/package/language/tool/orchestrator tests;
- `history/SEMANTIC_EVOLUTION.md` for material historical capabilities and supersession rationale;
- immutable 5.16, 6.0, and 6.1 recovery/version mappings;
- accepted archived workplans where current doctrine explicitly inherits a subtle historical guarantee.

This inventory is an implementation/review aid, not automatically a new permanent protocol database. Reuse existing qualification/tests/history as the primary preservation oracle.

### 4.2 Compression proof obligation

For every material removal, merge, relocation, or generalization of current doctrine, Implementation/Review must be able to identify where the semantic content now lives and why the old capability remains recoverable.

Acceptable forms include:

- identical semantic rule moved to its canonical owner;
- several narrower rules replaced by a demonstrably stronger general rule;
- generic rule removed from a secondary document while a direct route plus local consequence preserves correct behavior;
- historical amendment prose removed from the hot path while current generalized doctrine plus semantic history preserves both current behavior and historical rationale.

Unacceptable forms include:

- deleting a rule because current tests happen not to exercise it;
- replacing a precise exception/constraint with a vague principle;
- assuming a model will infer an omitted obligation from common sense;
- preserving only terminology while losing behavioral capability;
- passing a shorter document that changes an edge case, authority boundary, evidence threshold, or failure/closure condition.

### 4.3 Historical version isolation

Frozen Protocol 5.16, 6.0, and 6.1 source/profile/publication semantics remain immutable. Protocol 6.2 should express its current doctrine directly and cleanly rather than retaining obsolete current paths/terms solely because an earlier release used them.

The filename migration from `abstraction-and-realization.md` to `abstraction-and-concretization.md` is therefore a current 6.2 migration, not permission to rewrite frozen historical snapshots.

## 5. Routing and attention design

### 5.1 Desired routing shape

Prefer:

```text
SKILL.md
  -> universal kernel
  -> owning domain reference
  -> direct conditional concern owner(s)
  -> conditional language/tool owner(s)
```

Avoid:

```text
SKILL -> A -> B -> C -> repeated A-derived doctrine
```

A reference may contain explanatory links without creating transitive activation. When a secondary reference genuinely requires another owner to interpret a decision, say so explicitly and conditionally.

### 5.2 Attention hierarchy

Agent/human-facing outputs should normally order material as:

```text
active Serious Challenge / safety-critical conflict
-> current decision or disposition
-> governing invariants / blockers / required action
-> material uncertainty and evidence applicability
-> supporting rationale/evidence
-> routine implementation detail
-> historical/provenance detail
```

This is a semantic priority order, not a mandatory document template. Use the ordering only where those categories exist.

### 5.3 Representative hot-path evaluation

Measure the current 6.1 and candidate 6.2 protocol-context surface for representative tasks, including at least:

- local D4 repair under sufficient authority;
- substantial D3->D4 workplan creation;
- independent D4 implementation Review;
- D2 numerical-method work;
- D1 scientific formulation work;
- documentation-only reconciliation;
- maintenance audit;
- release/package work;
- historical-version recovery/migration;
- closeout.

For each, identify which protocol files are actually required before/while making the decision, why each activation edge exists, whether the same doctrine was already supplied, and whether history/secondary concerns can remain cold until triggered.

Token/byte/document counts are sensors, not governing thresholds. Acceptance requires a materially cleaner route with every retained mandatory load justified and no semantic capability loss. Do not optimize a numerical context metric by hiding necessary information.

## 6. Implementation sequence

### Stage A — Baseline and semantic preservation map

1. Freeze `cec29671...` as the Protocol 6.1 parent candidate for this work.
2. Inventory current 6.1 canonical owners, direct `MUST read` routes, conditional routes, cross-reference topology, and representative hot-path context surfaces.
3. Map all 95 qualified behaviors plus material historical Protocol 5.x/6.0 improvements to their current 6.1 owners.
4. Identify duplicate generic doctrine, near-duplicate doctrine, amendment-style history in current hot paths, and route chains that load the same concept repeatedly.
5. Produce a bounded change map; do not create a permanent universal graph unless evidence demonstrates it is necessary.

Stage A is non-mutating with respect to protocol semantics. It establishes the losslessness oracle.

### Stage B — Kernel and terminology normalization

1. Rename current `abstraction-and-realization.md` to `abstraction-and-concretization.md` and update current 6.2 references.
2. Add the protocol-wide Lossless Representation Rule to that kernel.
3. Reconcile current uses of `realization` so semantic concretization and evidence realization remain unambiguous.
4. Audit related current filenames/templates for obsolete realization terminology and rename when no supported current compatibility contract requires retention.
5. Keep frozen historical releases untouched.

### Stage C — Canonical-owner and document compaction

1. Refactor generic doctrine to one detailed current owner per concern.
2. Replace repeated generic sections in secondary references/skills with concise local consequences and direct owner routes.
3. Preserve standalone comprehension where local repetition actually reduces total cognitive cost.
4. Move detailed chronology/superseded amendment narrative off current execution paths while preserving semantic-evolution rationale.
5. Reconcile `source/SEMANTIC_DEPENDENCIES.md` with the new owner/routing structure.

### Stage D — Skill and prompt progressive-disclosure refactor

1. Refactor all role/specialist `SKILL.md` files into compact ownership + routing + local-method entrypoints.
2. Reclassify every mandatory read as truly universal/role-critical or decision-conditional.
3. Ensure ordinary hyperlinks/transitive package dependencies do not become implicit activation dependencies.
4. Refactor workflow prompts to one shared cross-stage contract plus concise stage deltas.
5. Update templates/handoff guidance and documentation specialist behavior to inherit the representation rule.

### Stage E — Version/profile/package integration

1. Set current canonical protocol version to `6.2.0` only after the semantic source is internally coherent.
2. Add a separate `ssdp-protocol-6.2` current profile/snapshot; preserve 5.16/6.0/6.1 frozen profiles unchanged.
3. Rebuild all generated distributions from canonical source and validate source-to-dist parity.
4. Update public/current documentation, semantic-dependency view, and versioning/recovery guidance.
5. Keep package transport self-containment correct after the filename/routing refactor.
6. Do not treat package membership as proof that a resource should be loaded into active context.

Profile schema v2 should remain unless this work changes an actual machine profile contract. Do not bump schema merely because prose/routing became cleaner.

### Stage F — Behavioral qualification and independent Review

1. Run all repository/package/orchestrator regression required by affected surfaces.
2. Construct Protocol 6.2 qualification by preserving the semantic capability of all 95 Protocol 6.1 cases. Version-specific cases must be interpreted correctly: frozen 6.1 continues to use its historical identifiers, while current 6.2 uses the renamed current kernel.
3. Add focused 6.2 scenarios for the new representation rule, including:
   - lossless compression versus omitted constraint;
   - generalized rule versus accumulated historical amendment prose;
   - single canonical owner plus local consequence;
   - ordinary hyperlink that must not trigger unrelated activation;
   - a genuinely required conditional dependency that must activate;
   - reuse of already-established governing context rather than repeated reload;
   - importance-weighted reporting that surfaces a blocker/Serious Challenge ahead of routine detail;
   - historical lineage remaining recoverable while absent from the normal hot path;
   - standalone handoff remaining complete without copying generic protocol doctrine;
   - current `abstraction-and-concretization.md` routing with frozen 6.1 historical compatibility preserved.
4. Perform an independent D3 Review of semantic preservation, routing topology, hot-path efficiency, and owner cleanliness.
5. No PASS if any material historical/current capability is missing, if a compact form becomes materially ambiguous, or if routing efficiency improves only by making required information unavailable.

### Stage G — Closeout and Protocol 7 impact reconciliation

1. Record material 6.2 semantic evolution and accepted recovery identity after qualification/Review.
2. Archive the completed 6.2 workplan only after current canonical owners contain every accepted rule.
3. Reconcile the active Protocol 7 handoff explicitly. Because Protocol 7 is not yet authorized for D4 implementation, it should inherit accepted Protocol 6.2 representation doctrine if 6.2 completes first unless Protocol 7 deliberately supersedes a rule.
4. Do not silently rewrite accepted Protocol 7 design semantics merely to adopt 6.2 wording. If the impact is representation-only, update routing/index/cutover references without minting an unnecessary Protocol 7 semantic revision; if a Protocol 7 architecture contract must materially change, route that through its existing deliberate D3 reopen.
5. Until 6.2 is accepted and has an immutable recovery mapping, Protocol 6.1 remains the current accepted rollback baseline.

## 7. Acceptance and falsification

### Mandatory semantic-preservation gates

Protocol 6.2 is No-Pass if any of the following occurs:

- an accepted Protocol 6.1 doctrine or still-valid historical improvement can no longer be recovered or executed correctly;
- a 5.16/6.0/6.1 frozen artifact/profile is rewritten for current terminology or style;
- semantic compaction changes an authority boundary, acceptance threshold, evidence applicability rule, uncertainty meaning, compatibility obligation, or Serious Challenge behavior without an explicit accepted semantic revision;
- removal of duplicated prose leaves a secondary artifact dependent on hidden/unsupplied context;
- a current runtime route relies on an incidental Markdown/package edge instead of an explicit decision trigger;
- historical detail is removed from the hot path without remaining recoverable where it can materially affect compatibility or recurrence reasoning;
- representation becomes shorter but materially harder to interpret or increases inferential burden.

### Representation-quality acceptance

After semantic preservation passes, independent Review should establish that:

- every generic protocol rule has one identifiable detailed current owner;
- secondary artifacts contain only justified local restatement/delta;
- normal role routes are progressive, shallow, and decision-triggered;
- representative hot paths show material reduction in unnecessary protocol context/repeated doctrine relative to 6.1 without arbitrary numerical gaming;
- current-state documents read as coherent present doctrine rather than patch history;
- high-consequence information is more salient than routine/historical detail;
- workplans/handoffs/reports remain snapshot-complete for their declared scope while avoiding generic doctrine duplication;
- package/distribution correctness remains independent from runtime context-loading policy;
- current terminology consistently uses abstraction/concretization and reserves realization for evidence execution except inside frozen historical identifiers/content.

### Challenge Pass

Actively attempt to falsify the central premise: determine whether the proposed compaction removes nuance that appears repetitive but actually encodes a distinct edge case, scope qualification, authority boundary, historical compatibility condition, or evidentiary requirement. Treat any such loss as a blocker and restore the distinct semantic content at the correct owner rather than preserving duplication blindly.

Also challenge the opposite failure mode: a purportedly lossless refactor that keeps every paragraph but merely rearranges links does not satisfy this workplan if normal routing/context remains unnecessarily dense.

SERIOUS CHALLENGE is reserved for evidence that the accepted Protocol 6.1 semantic authority itself is materially false, contradictory, inadequate, or impossible to preserve coherently. No such challenge is currently identified.

## 8. Required handoff state

Implementation handoff is ready only when the accepted 6.1 baseline, preservation oracle, canonical-owner targets, filename migration, routing principles, representation rule, affected surfaces, version/profile constraints, and qualification strategy above are treated as one composed contract.

The intended end state is:

```text
thorough and sophisticated semantics
+ zero material information loss
+ one detailed owner per generic rule
+ terse precise local representations
+ shallow relevance-driven routing
+ importance-weighted attention
+ history available without dominating current context
+ minimum justified cognitive/context cost
```

Protocol 6.2 succeeds only if it makes the same or stronger SSDP easier for an agent or human to understand and execute correctly, not merely shorter.