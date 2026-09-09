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
