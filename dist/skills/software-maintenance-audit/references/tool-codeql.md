# CodeQL: Interprocedural/Data-Flow Analysis and Code-Scanning Evidence

Use CodeQL when the material claim depends on supported interprocedural program relations such as data flow, taint propagation, source-to-sink reachability, or another relationship that ordinary inspection or lighter structural analysis cannot establish with adequate confidence.

CodeQL is an optional specialist analyzer, not a generic security gate. Generic protocol validity does not require local CodeQL, GitHub, hosted code scanning, network access, or a commercial entitlement unless project/task authority independently requires one of them.

## Selection boundary

High-value local/external uses include:

- interprocedural data-flow or taint-flow questions;
- source-to-sink reachability across functions/modules;
- security-sensitive flows whose risk depends on propagation rather than the mere presence of a syntax pattern;
- project-governed custom queries/query suites that encode durable analysis policy;
- independent review of a material data-flow/security claim using a distinct analysis model.

Do not route a purely structural pattern to CodeQL merely because a CodeQL query could express it when a focused Semgrep rule or direct inspection is sufficiently reliable and cheaper. A security task is not automatically a CodeQL task.

When a CodeQL-class question is triggered, read this method before relying solely on lower-information defaults. If availability is unknown, use a cheap read-only/non-mutating capability probe when practical. When CodeQL is available, supports the relevant language/build/extraction surface, and directly models the claim, presumptively use it. Fall back for a concrete reason such as unsupported language, unavailable CLI/query packs, extraction/build infeasibility, analyzer-model mismatch, or disproportionate database setup for a trivially bounded claim.

## Three distinct evidence concepts

Keep provenance explicit:

1. **Local/external CodeQL execution** — a CLI database/query analysis run against a candidate, optionally producing SARIF.
2. **GitHub-managed CodeQL execution** — CodeQL analysis executed under GitHub default/advanced code-scanning configuration or equivalent repository CI configuration.
3. **GitHub code-scanning result/alert surface** — repository-hosted findings/results that may originate from GitHub-managed CodeQL, externally uploaded CodeQL SARIF, or another analyzer.

A GitHub code-scanning alert is not automatically independent execution evidence. Uploading SARIF from the same local CodeQL run does not create a second analyzer execution merely because the result is displayed by GitHub. Only a separately executed GitHub-managed/CI analysis is an independent run relative to a local execution.

When project policy requires a particular hosted CodeQL/code-scanning check, that exact required check must execute on the intended candidate/configuration. A local run does not silently substitute for a required GitHub-managed check, and a hosted result does not silently substitute for a task-required local/custom analysis.

## Database creation, identity, and invalidation

A CodeQL database is derived analysis state for a particular source/extraction/build environment. Database creation success is not product correctness evidence.

For a material claim, retain enough identity to interpret the result:

- candidate/source identity and relevant generated-source state;
- supported language(s) and extractor version/capability when material;
- build mode/build command and material build configuration/dependency conditions when extraction depends on them;
- database creation/extraction success and material exclusions or extraction warnings;
- query/query-suite/pack identity and configuration sufficient to interpret the finding or zero-result claim.

Invalidate/rebuild or otherwise re-establish the database when changed source, generated code, build configuration, dependency resolution, extractor-relevant environment, or another changed dimension can plausibly alter the analyzed relation. Do not reuse stale database results merely because the database still opens successfully.

Choose build mode according to the actual language/project and current CodeQL capability. Do not hard-code a universal no-build/autobuild/manual-build rule into protocol doctrine.

For compiled/project builds, CodeQL extraction can execute the repository's build system, compilers, package/build hooks, and dependency tooling. Treat this as privileged execution under existing trust, supply-chain, resource, and subprocess rules. Bound CPU/RAM/disk/wall time and avoid executing untrusted build hooks without an appropriate trust decision.

## Query choice and result interpretation

Run the narrowest suitable built-in or project-governed query/query suite first; broaden only when the material claim warrants it. A finding is evidence requiring repository-context triage, not an automatic defect, requirement, or blocker.

For an acceptance-critical custom query, provide proportionate **known-positive and known-negative** validation or another convincing query test before trusting its positive or zero result. A custom query that has never demonstrated detection of a representative positive cannot establish absence.

If exact query identity materially affects an acceptance claim, pin/version/govern the query or query-pack identity proportionately. Do not base a durable acceptance-critical claim solely on a moving network-fetched query pack whose semantics can change invisibly.

A `0 results` or `0 alerts` outcome is meaningful only relative to the actual database and query contract. Bound negative/completeness claims by:

- language support and successful extraction/build;
- source/generated code actually included in the database;
- query/query-suite/pack and configuration identity;
- source/sink/model coverage for the analyzed relation;
- framework/library models and known analyzer limitations;
- runtime/dynamic/plugin/external-consumer behavior outside the database model.

Zero findings are not proof of absence outside that contract.

## Local state, SARIF, and hosted analysis

CodeQL databases, caches, downloaded packs, logs, and SARIF are derived analysis state by default. Do not commit large transient databases/caches/results unless project policy deliberately governs a compact configuration/result artifact for a real engineering reason. Bound analysis disk footprint and clean up run-owned transient state safely.

Do not upload source, SARIF, findings, or credentials to GitHub or another hosted service without project/user authorization and applicable trust-boundary policy. Local analysis is the portability baseline.

Generic protocol packages should document methodology, not embed CodeQL binaries, query packs, credentials, machine-specific paths, workflow action versions, or volatile GitHub UI/setup paths.

## Acceptance boundary

CodeQL complements but never substitutes for runtime security testing, focused behavior tests, affected regression, real-owner integration, or another project-required analyzer when those claims are material. Re-derive the final affected surface from the assembled candidate. If project policy requires GitHub-managed CodeQL/code scanning, an unavailable or unexecuted required check is not a pass under ordinary testing doctrine.
