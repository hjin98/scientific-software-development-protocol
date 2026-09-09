# Protocol 6.1 Additional Behavioral Qualification Scenarios

These cases complete the adversarial additions required by the Protocol 6.1 workplan beyond the 80 cases in `SCENARIOS.md`. They are qualification evidence definitions only; they do not mutate the Protocol 6.1 semantic candidate under test.

## H. Remaining Protocol 6.1 adversarial additions

### 81. Opaque compatibility identifier without semantic leakage
The retained current-path filename `abstraction-and-realization.md` and the frozen profile ID `ssdp-protocol-6.0` contain legacy `realization`/6.0 lexemes for compatibility. Current Protocol 6.1 explanatory prose must treat those strings as opaque compatibility identifiers while using concretization for semantic descent; the filename/profile identity does not authorize old semantic vocabulary to become current doctrine.

### 82. Typed relation direction
A dependency record is proposed with `CONCRETIZES` pointing from parent abstraction to child, `INSTANTIATES` pointing from specification to evidence realization, and `GENERATED_BY` pointing from realization to observation. Reject/reverse those edges: current Protocol 6.1 direction is child concretization -> governing parent, evidence realization -> evidence specification, and observation -> evidence realization. `EVIDENCES` remains evidence specification -> governed claim, while `EXECUTION_DEPENDS_ON` points from evidence specification/realization -> execution machinery/data/environment.

### 83. D4 observation routes upstream instead of forcing local repair
A new D4 integration run produces an observation contradicting an accepted numerical invariant, but the implementation conforms to its written D4 specification and D3 architecture. Investigation must consider D2/D1/D3 inadequacy or conflicting authority and may raise a Serious Challenge upstream; the observation does not prove the D4 implementation is the faulty owner.

### 84. Evidence specification or oracle may be the defect
A previously trusted test contradicts the candidate, but independent analysis shows its expected-value oracle encoded a superseded assumption. Treat invalid evidence specification/oracle or inapplicable realization as a genuine alternative explanation. Do not modify current authority or production behavior merely to satisfy a defective evidence instrument.

### 85. Evidence durability does not replace claim-specific sufficiency
A durable D1 invariant test passes, but a changed D4 implementation has not run its required conformance and real-owner integration checks. Do not close D4 on the high-level invariant alone. Conversely, detailed D4 unit/integration evidence cannot establish D1 external adequacy or replace required D2 numerical verification.

### 86. Retirement requires dependency and compatibility closure
A superseded concretization and its owner-specific tests are no longer current, but a supported 6.0 compatibility profile still depends on them. Do not delete them yet. Retirement becomes admissible only when the artifact no longer owns current authority, no supported current concretization/evidence/compatibility path materially depends on it, and material historical rationale is preserved where needed.

### 87. Manual document-controlled operation remains first-class
An environment has no usable orchestrator or Protocol 7 machinery, but the current Protocol 6.1 role skills, required references, prompts, and workplan are readable. The workflow must remain executable manually/semi-automatically from those documents. Do not require TaskEnvelope/ResultEnvelope exchange, a machine-authoritative graph, an orchestrator reducer, or remote polling to claim valid Protocol 6.1 operation.

## I. Revision 1 human-facing closure cases

### 88. D2 named-method background without normative substitution
A new D2 Numerical & Algorithmic Method Paper introduces a specialized named numerical method unfamiliar to its intended competent reader. Provide a concise background definition/context before the governing algorithmic formulation relies on it, while retaining the exact algorithm/error/convergence semantics in the D2 normative section rather than moving authority into the background prose.

### 89. Unexplained acronym is documentation incompleteness
A current human-facing methods document uses a non-obvious project acronym repeatedly without ever expanding it because the reviewing model already recognizes the acronym. Reject the documentation as incomplete: model knowledge does not satisfy the reader-facing first-use contract. Add the full term followed by the abbreviation in parentheses at first explanatory use.

### 90. Shared multi-file background requires explicit supplied composition
A three-file current method-document family defines specialized terminology only in file A while files B and C rely on it. This is acceptable only when the composition is explicit and A is supplied/read with B and C as the current artifact set. If B or C is intended to stand alone, essential terminology must be defined locally rather than hidden in an unsupplied prerequisite.

### 91. Compact machine identifier plus explanatory human documentation
A Protocol/control JSON field uses a compact enum or profile identifier such as `ssdp-protocol-6.1`. Do not inject pedagogical prose into the machine value merely to satisfy the background/acronym rule. Instead, the human-facing schema/user documentation must explain any non-obvious identifier meaning and terminology needed by operators/readers.

### 92. Historical Protocol 5 document remains version-faithful
A release-pinned Protocol 5.x methods/workflow artifact contains terminology or abbreviations that would not satisfy the new Protocol 6.1 presentation standard. Do not retroactively rewrite that historical artifact solely for style. Supply necessary current explanatory context when citing it, while preserving the historical bytes/meaning under their governing version.
