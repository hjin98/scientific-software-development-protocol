---
kind: abstraction-concretization-change-plan-consolidated-staging
workplan_id: SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED-FIFTH-REVIEW-STAGING
protocol_version: 6.3.0
target_protocol_version: 6.4.0
status: staging-non-authoritative
created_date: 2026-09-15
reviewed_date: 2026-09-15
design_review_state: fifth-review-gap-closure-staging
implementation_handoff: not-authorized-from-this-file
active_serious_challenge: none
branch: ssdp-6.4-axiomatic-definition-traceability
reviewed_composed_head: f94723215dc0ed9eeadf0bc298e4cce579fab810
---

# Protocol 6.4 fifth-review staging notes

This temporary non-authoritative file records the fifth-review corrections while the single active consolidated workplan is rewritten. It MUST be deleted from the final branch state and MUST NOT be used as a composed implementation handoff.

## Gaps found

1. The live workplan uses specialized core terms (`semantic object`, `canonical definition`, `substantive use`, material direct prerequisite) without defining them, violating its own self-hosting rule.
2. `available(x)` conflates source/document semantic availability with agent-runtime loaded-context availability.
3. `USES_DEFINITION` is definition-to-definition only and therefore misses theorem statements, assumptions, algorithms, contracts, and other governed semantic units that use a definition without themselves being definitions.
4. Primitive roots have declarations rather than definitions, so the relation endpoint wording is incomplete.
5. Direct-prerequisite materiality lacks a falsifiable criterion, allowing omission by author discretion.
6. Circular warrant can still be hidden across different typed relations even though pure `DERIVED_FROM` cycles are rejected.
7. Definition laundering is prohibited, but definitional conservativity over prior vocabulary is not stated explicitly.
8. Literature/data support and externally binding contract/standard/regulatory authority remain insufficiently separated.
9. Imported empirical data may be transformed/filtered/preprocessed without a required source-to-local transformation lineage.
10. Necessary/sufficient/biconditional direction is not called out explicitly even though implication direction is semantic.
11. Material semantic endpoints lack an explicit durable-locator rule for cross-document traceability.
12. The doctrine lacks an explicit rule for cases where full formalization is impractical but material ambiguity remains.
13. The current workplan itself uses non-obvious abbreviations such as IID and SCC without first-use expansion.
14. Supported Markdown/LaTeX/link/render integrity is not an explicit qualification surface even though broken rendering can make a formal definition unavailable to the intended reader.

## Required closure model

The rewritten single consolidated workplan must define:

- `source_available_D(x)`: `x` is reconstructible from one version-coherent authority composition `D` through the bounded foundational envelope, exact external import, project declaration/definition, or a valid local binder;
- `context_available_C(x)`: the exact canonical meaning needed for an inference is actually supplied/loaded in runtime context `C`;
- authoring invariant: `use_D(x) -> source_available_D(x)`;
- runtime invariant: `infer_C(x) -> context_available_C(x) -> source_available_D(x)`;
- a governed **semantic object/unit** as a term, symbol, quantity, operator, relation, state, proposition, algorithmic object, or contract whose meaning/conditions can alter governed interpretation, admissible concretization, evidence applicability, or acceptance;
- **substantive semantic use** as an occurrence whose meaning participates in a definition/declaration, premise, inference, constraint, contract, acceptance, or interpretation rather than a harmless forward name;
- `USES_DEFINITION` as `subject -> exact semantic object whose canonical declaration/definition/semantic statement is directly required to interpret the subject's own canonical semantic statement`, not merely definition-to-definition use;
- a direct material prerequisite criterion: varying the prerequisite's admissible meaning can change the subject's denotation, admissible domain, validity, governed contract, or accepted interpretation;
- bounded typed **warrant closure** for established claims, terminating in admissible roots without self-supporting cycles across mixed relation types;
- definitional conservativity: an explicit definition cannot add a new proposition about prior vocabulary; existence, uniqueness, admissibility, empirical, causal, comparative, safety, convergence, and normative assertions are separately classified/warranted;
- external semantic support separately from external normative force; an applicable contract/standard/regulation can be governing because the actual external/project authority makes it binding, not because it is merely cited;
- transformation lineage for imported data/reference values when filtering, preprocessing, unit conversion, calibration, aggregation, or other transformations affect meaning;
- explicit necessary/sufficient/biconditional direction where material;
- durable owner + logical locator + version/snapshot identity for material cross-document endpoints, without mandating global IDs;
- `REVIEW_REQUIRED`/Challenge when the strongest practical formal representation still leaves material ambiguity;
- first-use expansion and source/render integrity as self-hosting acceptance obligations.

This staging file is evidence only and is not a new current authority surface.