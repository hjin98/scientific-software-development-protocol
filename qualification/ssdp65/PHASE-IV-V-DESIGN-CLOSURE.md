---
kind: ssdp65-phase-iv-v-design-closure
investigation: SSDP-6.5-FRONTIER-MODEL-RE-EVALUATION
protocol_version: 6.4.0
target_protocol_version: 6.5.0
subject_baseline: 55c085261eb827e3047637d045a8e6917ea6b962
diagnostic_commit: 81375d8142a8130b80cd82f2304d3e16bc3fc390
adjudication: qualification/ssdp65/CROSS-MODEL-ADJUDICATION-2026-09-24.md
status: design-pass
phase_iv: complete
phase_v: complete
phase_vi: authorized
active_serious_challenge: none
created: 2026-09-24
---

# Protocol 6.5 Phase IV-V Design Closure

## 1. Disposition

**DESIGN PASS. Phase IV principle extraction and Phase V candidate design are complete. Phase VI implementation is authorized.**

The design closes the four adjudicated defect families through six principles, without reopening the accepted D1-D4 scientific/software authority model and without introducing a universal semantic parser, ontology, registry, or second control plane.

The principal D3 decision is to create **one small project-level mutable release-state owner outside versioned `source/`**. This is justified new machinery because every existing alternative either preserves duplicated lifecycle truth or makes mutable state part of immutable version semantics. The new owner replaces value copies; it is not another mirror.

## 2. Governing parents and protected capabilities

The candidate must preserve:

- D1-D4 as the only semantic authority domains;
- abstraction adequacy distinct from concretization fidelity;
- accepted Protocol 6.4 formal-definition/source-availability/well-definedness/parameterization/warrant/typed-dependency doctrine;
- evidence specification -> realization -> observation -> assessment;
- stale-evidence, proxy-proof, and real-owner evidence rules;
- Serious Challenge as the route for defective accepted authority;
- PEM as optional-to-activate, evidence-backed, project-local and non-authoritative;
- one semantic owner per current material claim;
- progressive disclosure and Lossless Representation;
- bounded impact closure and preservation of unaffected siblings/evidence;
- exact immutable historical source/profile/bootstrap/recovery identities;
- public-source fallback and recovery as distinct identities;
- Protocol 7 D3 architecture unchanged.

The design changes SSDP self-governance, release state, qualification semantics and representation architecture only.

## 3. Architecture alternatives considered

### 3.1 Mutable release-state owner

Four alternatives were considered.

| Alternative | Result | Reason |
| --- | --- | --- |
| Keep release truth in `protocol-versioning-and-compatibility.md` | rejected | versioned source/fallback is immutable; mutable current state becomes stale by construction |
| Make `SSDP-6.1-7.0-WORKPLAN-AUTHORITY-INDEX.md` the owner | rejected | workplan routing/index has a different lifecycle and audience; machine parsing human workplan prose would preserve hidden coupling |
| Make root `README.md` / `AGENTS.md` the owner | rejected | human navigation/instruction surfaces should route to authority, not become a mutable release database |
| Add one root `PROTOCOL-RELEASE-STATE.yaml` | **selected** | one bounded machine/human owner replaces many hand-copied values and can be validated without contaminating immutable protocol semantics |

The selected artifact is project-level state, not packaged protocol doctrine. A copy of it in an old immutable commit is historical snapshot state, not current release authority.

### 3.2 Semantic qualification

| Alternative | Result |
| --- | --- |
| Expand QF64 synthetic dictionaries/string assertions until more prose mutants fail | rejected: optimizes proxy/wording rather than the real semantic subject |
| Build a general semantic parser/theorem prover | rejected: new parallel authority and unjustified complexity |
| Separate structural executable qualification from assembled-candidate semantic Review | **selected** |

### 3.3 PEM validator reconciliation

| Alternative | Result |
| --- | --- |
| Treat executable validator behavior as de facto schema | rejected |
| Remove all sophisticated validator semantics | rejected: several concretize accepted 6.3 evidence/maturity/recurrence doctrine |
| Reconcile canonical schema/template with justified validator semantics and remove redundant executable-only knobs | **selected** |

## 4. P65-1 — Self-application

### Definition

SSDP development/release is itself a governed SSDP project. Current accepted ownership, evidence, Challenge, convergence, representation and impact rules apply to SSDP's own artifacts unless the versioning owner defines a **bounded bootstrap exception** that is technically unavoidable and explicitly scoped.

Self-application does not recursively require an infinite proof of itself. It means that when SSDP creates a workplan, qualification, release mapping, generated artifact, project memory, or Review, those artifacts are judged by the same owner/evidence/representation rules applicable to downstream projects.

### Coverage

Covers A-01, A-02, A-05, A-06, A-10, A-11 and A-12 at their shared root.

### Old rules subsumed

- one current semantic owner;
- derived-view subordination;
- evidence must discriminate its real owner;
- convergence after recurrence;
- one detailed owner per generic rule;
- no amendment replay;
- workplans/tests/reviews are means, not objectives.

### Counterexamples excluded

- lifecycle values copied into many current surfaces;
- test suite becoming a second semantic owner through exact prose pins;
- validator silently acquiring schema semantics;
- repeated Review rounds optimizing an author matrix without challenging the matrix.

### Newly permitted behavior

No new downstream behavior. The rule permits deleting SSDP-specific compensating machinery when the generic owner rule already governs the case.

### Compatibility

Backward-compatible strengthening; frozen historical artifacts remain historical truth.

### Owners

Kernel owns the self-application invariant. Workflow/testing/versioning/PEM owners state only local consequences.

### Qualification

A final Review must identify any Protocol-6.5-only exception to ordinary SSDP rules and show why it is bounded/necessary. Absence of unjustified exceptions is a semantic Review claim, not a phrase count.

### Ablation

Without P65-1, reproduce A-02/A-11: allow a self-testing qualification proxy to satisfy local release obligations while failing to discriminate canonical semantic mutation.

**Closure: PASS.**

## 5. P65-2 — State/semantics separation

### Definition

Let (S_v) denote version-intrinsic semantics of protocol version (v), and (L_t) the repository/project release state at time/project state (t).

[
S_v 
eq L_t.
]

An immutable source snapshot for (v) may define the semantics of release-state concepts, but it must not be the current owner of mutable facts such as which version is accepted-current, whether a candidate has passed Review, or which recovery identity was later published.

### Selected release-state owner

Add root:

`PROTOCOL-RELEASE-STATE.yaml`

with schema 1:

```yaml
schema_version: 1
project: hjin98/scientific-software-development-protocol
accepted_current:
  version: "6.4.0"
  public_source_ref: <immutable SHA>
  recovery_ref: <immutable SHA>
historical:
  "<version>":
    public_source_ref: <immutable SHA or NONE>
    recovery_ref: <immutable SHA or NONE>
candidate:
  version: "6.5.0"
  semantic_ref: UNFROZEN | <immutable SHA>
  review:
    state: NOT_RUN | NO_PASS | PASS
    evidence_ref: NONE | <immutable repository evidence route>
  ratification:
    state: NOT_REQUESTED | PENDING | RATIFIED | REJECTED
    evidence_ref: NONE | <immutable repository evidence route>
  public_source_ref: UNAVAILABLE | <immutable SHA>
  recovery_ref: UNAVAILABLE | <immutable SHA>
```

The implementation may normalize key names/format, but may not add a second release-state representation with independent semantics.

### State rules

1. Exactly one `accepted_current.version`.
2. Every non-sentinel public/recovery ref resolves to an immutable commit whose `source/PROTOCOL_VERSION` matches the mapped version.
3. Candidate `semantic_ref` remains UNFROZEN until the semantic candidate exists.
4. Review PASS binds exact `semantic_ref`.
5. Ratification may be RATIFIED only from explicit stakeholder evidence for that reviewed semantic ref.
6. Public-source fallback remains UNAVAILABLE until Review PASS + stakeholder ratification.
7. Public-source ref is the exact reviewed/ratified semantic source candidate; publication is from a later descendant because the candidate cannot self-name.
8. Recovery remains distinct and later; recovery ref is published from a descendant after the recovery commit exists.
9. `accepted_current` changes only after recovery/publication/current-state acceptance completes.
10. Historical mappings are immutable facts once superseded unless an explicit correction invalidates the mapping.

### Current versus historical copies

The current authority is the release-state file on the repository's designated integration publication state. The same path in an older immutable commit is historical evidence only. Branch position/default/newest commit is not itself release authority; the file's exact mappings and lifecycle evidence are.

For this repository, `main` is the designated integration publication line. Merge/publication to `main` makes the ratified state discoverable; **the merge does not create the acceptance decision**. Stakeholder ratification does.

### Consequences for versioned source

- `source/README.md`: version-intrinsic navigation only; no "candidate", "accepted-current", "recovery pending" current claims.
- `development-workflow-prompts.md`: may state its own protocol version, but removes current accepted-version/public-ref/recovery value copies; cold remote fallback resolves exact ref from an explicitly supplied mapping or the project release-state owner.
- role/specialist descriptions: no hard-coded predecessor/current protocol version.
- versioning owner: owns semantics/classes/lifecycle rules, not current exact mutable values.
- generated profile/prompts: version intrinsic; do not embed mutable repository lifecycle truth.
- root README/AGENTS/current indexes: route to `PROTOCOL-RELEASE-STATE.yaml` rather than restate mutable values except where a workplan deliberately freezes a value as a cycle input.

### Coverage

A-01, A-03, A-09, A-12 and FF-001 recurrence.

### Counterexamples excluded

Accepted 6.5 package saying 6.4 is accepted-current; immutable fallback saying its own fallback is unavailable; current index disagreeing with versioning owner.

### Compatibility

Historical 5.16-6.4 source/profile bytes are untouched. Exact accepted mappings are preserved in the new state owner and history.

### Ablation

Embed candidate/current lifecycle text back into the immutable 6.5 prompt source and show that a later cutover makes that text stale while source/package parity remains green.

**Closure: PASS.**

## 6. P65-3 — Evidence-claim congruence

### Definition

For a qualification claim (q), the evidence record must make recoverable:

[
q = (	ext{subject}, 	ext{property}, 	ext{oracle/method}, 	ext{result}, 	ext{limitations}).
]

Evidence may support only the property of the exact subject that the oracle/method can discriminate.

### Three evidence classes

1. **Structural/executable consistency** — schemas, exact refs, generated parity, package structure, state transitions, forbidden dependency structure, frozen bytes.
2. **Semantic adequacy/conformance** — interpretation of the assembled normative owners and their consequences.
3. **Engineering-outcome improvement** — whether protocol-guided development produces better outcomes/cost on representative tasks.

No class substitutes for another.

### QF64 disposition

The 6.4 QF synthetic fixture machinery is not automatically deleted wholesale. During implementation classify each current assertion:

- retain/strengthen if it exercises a real executable parser/state/schema/routing predicate;
- rewrite if it can test the real semantic owner structurally;
- retire/move to historical qualification if it only proves an author-created dictionary predicate or exact prose wording;
- keep exact strings only when that exact syntax/token is itself the governed interface.

Passing a fixture matrix must not be described as qualification of prose semantics.

### Qualification records

Protocol qualification records must state their claim scope. No new mandatory machine-readable report schema is required; concise front matter/table fields are sufficient if unambiguous.

### Coverage

A-02, A-04, A-11.

### Counterexamples excluded

- 12/15 canonical semantic inversions passing while a synthetic oracle remains green;
- lossless paraphrase failing because tests own wording;
- scenario conformance being presented as proof that a new protocol improves engineering outcomes.

### Compatibility

Existing mechanical regression remains useful for the properties it actually tests. No requirement for machine semantic understanding is added.

### Ablation

Restore a QF-style self-contained predicate and claim it qualifies corresponding canonical prose; mutate only the prose and show the proxy remains green.

**Closure: PASS.**

## 7. P65-4 — Review abstraction adequacy

### Definition

A substantial independent Review must test both:

1. **candidate fidelity** to reconstructed governing authority; and
2. **review/plan abstraction adequacy** — whether the author's decomposition, workplan and qualification could all be satisfied while a material upstream/global invariant still fails.

### Mandatory protocol-Review pass

For protocol releases, a fresh reviewer must perform an **out-of-matrix pass**:

```text
reconstruct global invariants from current owners
-> inspect the assembled candidate
-> ignore the author's obligation matrix temporarily
-> construct at least one plausible local-compliance/global-failure trajectory or record that none survived
-> challenge the adequacy of the qualification method itself
```

The reviewer is not required to invent a defect. It is required to attempt the falsification independently.

### Independence

Review independence is authorship/conclusion independence, not model-family identity:

- reviewer/context did not author the candidate being reviewed;
- reviewer reconstructs authority/evidence rather than inheriting author conclusions;
- prior findings may be evidence after independent reconstruction;
- different model family/human evidence is stronger corroboration but not a prerequisite for ordinary independence.

### Coverage

A-02, A-04, A-08, A-11 and the historical B64-R4..R9 local-repair cycle.

### Compatibility

Strengthens existing "review assembled candidate, not summary" doctrine without requiring a second frontier family for every Review.

### Ablation

Give the reviewer only the author obligation matrix and known repair findings; verify that lifecycle/qualification defects outside the matrix can remain invisible.

**Closure: PASS.**

## 8. P65-5 — Minimal meta-governance

High-leverage control predicates receive one canonical definition at their natural owner.

### 8.1 Materiality — kernel owner

For governed decision (d), a difference/claim/risk (x) is **material** when there is a plausible path within the governed scope, grounded by current authority, dependency, evidence, or a concrete counterexample, by which changing/omitting (x) can change one or more of:

- governed interpretation;
- admissible concretization;
- evidence applicability or required evidence;
- acceptance/reopen/Challenge disposition;
- protected risk;
- protected stakeholder/product/scientific outcome.

Pure wording difference and remote ungrounded possibility are not material merely because they can be imagined.

This formalizes the already implicit semantic-object/materiality logic; it does not create a numerical threshold.

### 8.2 Serious Challenge — kernel owner

Raise Serious Challenge only with a **credible basis** that accepted authority may itself be materially defective: a concrete contradiction/counterexample, materially consequential ambiguity, mutually incompatible applicable constraints, unrealizability, or admissible evidence of inadequacy. Mere possibility or reviewer discomfort is insufficient.

The Challenge record identifies owner, basis, consequence, assumptions and discriminating resolution evidence.

### 8.3 Challenge resolution — kernel/workflow consequence

The owning authority resolves the challenged semantics through its normal acceptance route. A "clarification" that materially narrows or changes the admissible interpretation/concretization set is a semantic mutation for impact/evidence/version purposes. Representation-only wording changes are those that preserve the admissible semantic set.

### 8.4 Review/falsification independence — workflow owner

Defined by authorship/conclusion separation as in P65-4. Evidence-route independence remains separately owned by the evidence owner.

### 8.5 Protocol-version acceptance — versioning owner

[
	ext{independent Review PASS}
Rightarrow
	ext{technically eligible}
]

[
	ext{explicit stakeholder ratification of that exact reviewed semantic ref}
Rightarrow
	ext{accepted decision}
]

Publication/cutover then represents and distributes the accepted decision. Automation cannot self-ratify.

Ratification must be explicit; an agent must not infer it from silence, Review PASS, CI, branch merge, or its own commit.

### 8.6 Accepted PEM base — Git/workflow owner

Generic projects must declare an integration policy for selecting accepted/base PEM. For the SSDP repository:

- `main` is the designated integrated project line for PEM publication;
- a candidate branch uses the exact integrated base from which its governed work started, unless explicitly rebound to a newer accepted integration state;
- same-branch PEM is an overlay until integration;
- an active workplan records the exact accepted base/overlay used.

This is project-memory policy only; it does not make `main` a protocol-version semantic oracle.

### Coverage

A-05, A-07, A-08, A-09.

### Ablation

- allow "may be wrong" without credible basis and observe false-positive Challenge blocking;
- allow author context to call itself independent;
- allow Review PASS to transition release state to accepted without ratification.

**Closure: PASS.**

## 9. P65-6 — Integrated current representation

### Definition

Current doctrine is written as current doctrine. Release-labelled amendment replay belongs in semantic history once integrated. Secondary surfaces route to one owner and state only their local consequence.

### Mandatory integration set

The implementation must inspect and integrate the existing 6.4-labelled additions in these current owners rather than simply rename their headings to 6.5:

- `abstraction-and-concretization.md`;
- `scientific-formulation.md`;
- `numerical-algorithm-design.md`;
- `architecture-and-design.md`;
- `specification-and-implementation.md`;
- `evidence-evolution-and-dependencies.md`;
- `testing-and-validation.md`;
- `workflow-and-workplans.md`;
- `documentation-and-evidence.md`;
- `documentation-maintenance.md`;
- `scientific-technical-writing.md`;
- `security-and-trust-boundaries.md`;
- `protocol-versioning-and-compatibility.md`.

The behavior is preserved in equal-or-stronger owner sections; detailed 6.4 chronology remains in history/archived workplan.

### Stale current labels

At minimum repair:

- all four role and three specialist frontmatter descriptions saying "under Protocol 6.3" — remove hard-coded protocol number unless version identity is semantically required;
- D1/D2 paper templates self-labelled Protocol 6.1 — make templates current/generic and add any accepted 6.4 definition/import slots actually needed;
- `language-profiles.md` "Current Protocol 6.2" wording;
- current repository-intake/semantic-dependency/navigation statements retaining candidate/older-version claims;
- `source/README.md` candidate/current lifecycle prose;
- workflow prompts embedding current accepted version/public-ref/recovery values.

### Versioning-owner compression

The current versioning owner keeps:

- version-class semantics;
- compatibility/adoption rules;
- generic public-fallback/recovery semantics;
- generic self-reference-safe publication;
- candidate/evidence applicability rules;
- route to current project release-state owner.

Detailed version-by-version bootstrap/recovery chronology and long exact-SHA narratives move to semantic history/current release-state mapping as appropriate. Frozen historical sources remain unchanged.

### PEM schema reconciliation

The canonical PEM owner/template must explicitly represent the accepted semantics already enforced by D4 where they are genuine schema requirements:

- structured `recurrence_basis`, including prior occurrence, repair identity, repair-acceptance evidence, later event identity, independence basis and non-Git chronology evidence where applicable;
- `maturity_basis` obligations for PROVEN claims;
- typed `comparative_basis` and owner-backed `comparative_authority`;
- evidence-bound `temperature_override`;
- bounded `counterevidence_search`;
- authority/binding-health fields and assessment supersession already described by doctrine.

Specific D4 decisions:

- remove the redundant top-level `provenance_independence_required` compatibility knob; claim-relative `maturity_basis` owns independence requirements;
- `alias_of` may remain only if documented as optional recurrence metadata; it is not a required field and cannot be a hidden semantic requirement;
- Git `patch-id --stable` remains a replaceable validator heuristic for the already-owned "copied/rebased/cherry-picked episodes are not independent recurrence" rule; it does not become protocol schema authority;
- fix the current PEM template front-matter/example structure so copied examples are syntactically valid YAML;
- do not remove temperature/maturity semantics based only on the SSDP repository's low usage.

### Context/duplication target

P0 kernel baseline is approximately 2,636 words and increased materially from 6.2. P1 must not increase always-loaded kernel words. Added meta-definitions/self-application must be offset by integrating/removing duplicate/amendment text. Prefer net reduction.

### Coverage

A-05, A-06, A-10, A-12; A-13 explicitly deferred.

### Ablation

Restore a version-labelled appendix/value-copy or executable-only PEM field and demonstrate reintroduced duplicate ownership/staleness.

**Closure: PASS.**

## 10. Concrete canonical-owner map

| Concern | Canonical owner after 6.5 | D4/local consequences |
| --- | --- | --- |
| universal self-application/materiality/Challenge threshold | kernel | roles route only |
| mutable SSDP release state | root `PROTOCOL-RELEASE-STATE.yaml` | tests validate schema/refs; current docs route |
| version classes/fallback/recovery/ratification semantics | versioning owner | state file contains current values |
| Review independence/out-of-matrix Review | workflow owner | role prompts invoke |
| qualification/oracle scope | testing owner | tests implement only decidable properties |
| evidence subject/applicability | evidence owner | qualification records bind exact subjects |
| simplification/review saturation | convergence owner | Review uses family/simplification trigger |
| PEM schema meaning | PEM owner + canonical template | validator concretizes |
| PEM accepted-base integration policy | Git/workflow owner + project-local AGENTS policy | workplan/HAS exact basis |
| protocol-version stakeholder ratification | versioning owner | release state references ratification evidence |
| historical release chronology | semantic history / archived workplans | not hot owner |

No other release-state registry or schema owner is permitted.

## 11. Publication transaction

The 6.5 release sequence is frozen as:

1. implement canonical P1 without public-fallback/recovery claims;
2. execute implementation acceptance;
3. freeze immutable semantic candidate;
4. bind exact candidate in a descendant handoff if needed;
5. independent assembled-candidate Review;
6. explicit stakeholder ratification of that exact reviewed semantic candidate;
7. later descendant publishes the semantic candidate SHA as 6.5 public-source fallback in the release-state owner;
8. verify exact-ref remote/fallback/package/profile behavior;
9. select a distinct immutable recovery target containing candidate + Review + ratification + required publication evidence;
10. later descendant publishes recovery mapping;
11. regenerate/reconcile any mapping-dependent current project surfaces;
12. rerun release-state/package/profile/Core acceptance;
13. update accepted-current in release-state owner and publish the integrated state;
14. update Protocol 7 inheritance identity only;
15. reconcile PEM/history and close/archive.

A semantic mutation after step 5 invalidates Review/ratification for the modified candidate and returns to step 2/3 as applicable.

## 12. D4 delegated space

Implementation may choose:

- YAML parsing helper location and function names;
- exact test module split;
- precise prose organization after removing amendment headings;
- generator refactors needed to stop embedding mutable state;
- local schema helper/data classes;
- exact current-release-state negative fixtures;
- exact compression edits.

It may not:

- introduce a second release-state file/registry;
- keep mutable lifecycle values in versioned prompts "for convenience";
- replace semantic Review with exact-string tests;
- alter D1-D4 authority semantics;
- merge bootstrap and recovery identities;
- self-create stakeholder ratification;
- mutate frozen 5.16-6.4 resources;
- remove PEM maturity/temperature semantics without new authority/evidence.

## 13. Preservation/supersession-map contract

Before P1 freeze, produce `qualification/ssdp65/PROTOCOL-6.4-TO-6.5-PRESERVATION-MAP.md`.

The map must cover:

1. every invariant in the 6.4 consolidated workplan §1;
2. every substantive 6.4 formal-definition/traceability section and its current owner;
3. P64-A..P64-O and any accepted QF/F64 capability that remains valid after qualification-method narrowing;
4. inherited Protocol 6.3 preservation census capabilities;
5. frozen profile/public-fallback/recovery behavior.

Each item is classified:

`PRESERVED | CLARIFIED | GENERALIZED | COMPRESSED | RELOCATED | SUPERSEDED | INTENTIONALLY_REMOVED`

with exact 6.5 owner and evidence obligation. "Removed because tests changed" is not sufficient.

## 14. Phase-V Challenge pass

### Could the new release-state file become another duplicate authority?

Yes, if current docs continue to hand-copy values. The design forbids that. Its acceptance includes a census showing secondary surfaces route/reference rather than independently state mutable values.

### Could moving semantic validation to Review weaken evidence?

Yes, if executable structural properties are also moved out of tests. The design forbids that. Machine-decidable state/schema/generated/package properties remain executable and receive stronger real-owner tests.

### Could human ratification become procedural bureaucracy?

For ordinary downstream releases, this design adds no generic human gate. It applies explicit stakeholder ratification to SSDP protocol-version acceptance itself, where the protocol defines the authority governing future agent behavior.

### Could compression lose 6.4 doctrine?

The preservation map, frozen-profile checks and semantic Review are explicit blockers. Compression is not accepted on line-count evidence alone.

### Serious Challenge

None. The design is compatible with accepted 6.4 D1-D4 doctrine and is implementable.

## 15. Phase IV-V verdict

```text
P65-1 SELF-APPLICATION:               CLOSED
P65-2 STATE/SEMANTICS SEPARATION:     CLOSED
P65-3 EVIDENCE-CLAIM CONGRUENCE:      CLOSED
P65-4 REVIEW ABSTRACTION ADEQUACY:    CLOSED
P65-5 MINIMAL META-GOVERNANCE:        CLOSED
P65-6 INTEGRATED REPRESENTATION:      CLOSED
D3 OWNER CONFLICT:                    NONE
SERIOUS CHALLENGE:                    NONE
PHASE VI IMPLEMENTATION:              AUTHORIZED
```
