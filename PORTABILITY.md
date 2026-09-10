# Agent portability and routing qualification

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** is distributed as portable **Agent Skills**: self-contained skill directories whose `SKILL.md` entrypoint routes the references needed for a role or specialist. SSDP uses **D1** scientific/mathematical, **D2** algorithm/numerical, **D3** software-architecture, and **D4** specification/implementation authority. An **orchestration profile** is a version-bound machine-readable representation of the human-facing workflow prompts used by the optional Orchestrator Core.

Protocol 6.1 preserves the portable Agent Skill contract while adding first-class D1/D2 roles and a dual-version orchestration profile.

## Installation contract

The runtime unit is the self-contained directory `dist/skills/<skill-name>/`; the top-level ZIP contains identical files under one enclosing skill directory. Install each skill as a direct child of the harness-supported skill root so `<skills-root>/<skill-name>/SKILL.md` exists. `source/` is canonical development source, not the runtime bundle.

This direct-directory installation contract remains the portability baseline. ZIPs are transport artifacts; extract the enclosing `<skill-name>/` directory before placing it under a runtime skill root. A shared/symlinked installation is a separate harness capability and must be qualified on that harness.

Current authority-bearing skills:

- `scientific-formulation`
- `numerical-algorithm-design`
- `software-design`
- `software-implementation`

Optional specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`.

## Human-facing orchestration

`source/shared/references/development-workflow-prompts.md` is the canonical prompt source. With `AUTO_LOCAL_FIRST`:

1. use a governing-version-compatible installed skill/exposed skill root through the harness-native mechanism;
2. otherwise use the canonical public repository `https://github.com/hjin98/scientific-software-development-protocol` at immutable current-6.1 public-source bootstrap `47e9155632c44493644b0b02fa1fa625703cf480` and load its `source/` entrypoint plus required references; never use repository-default bytes as a substitute for the declared protocol version;
3. preserve the workplan's protocol binding; never guess a semantic version as a Git ref or silently substitute current doctrine;
4. report truthful non-closure if no compatible source can be read.

Before mutation classify the highest potentially affected D1/D2/D3/D4 domain and direct governed side constraints. Reduced routes are normal; do not force every task through all four skills.

Current Protocol 6.1 immutable public-source bootstrap: `47e9155632c44493644b0b02fa1fa625703cf480`. This source identity is usable before default-branch cutover and remains distinct from accepted replacement rollback recovery snapshot `802e75af261efb4f70d71284d860613a2197b639`.

## Orchestrator profile compatibility

The Core supports independent version-bound profiles:

| Profile | Protocol | Profile schema | Purpose |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen historical compatibility |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | frozen pre-6.1 compatibility |
| `ssdp-protocol-6.1` | 6.1.0 | 2 | current evidence/evolution-aware document-controlled workflow |

Historical 5.16 and 6.0 prompt/profile bytes remain immutable. A workplan's declared `protocol_version` selects its compatible profile before stage semantics are interpreted. Project profile configuration is a default, not authority to override an explicit workplan version.

Protocol 6 profile stages include authority intake, D1, D2, D3, D4, Review/Challenge, Verification, Stabilization, Alignment, Health Audit, and Closeout. Serious Challenge/human-pending outcomes stop automatic normal routing; the orchestrator records/routes state but never decides scientific truth.

## Immutable recovery identities

Version-bound recovery uses immutable repository commits rather than `main`/latest:

| Protocol | Immutable recovery commit |
| --- | --- |
| 5.16.0 | `e151daaf5c8eebb351a85cfed86170fda80fb5e3` |
| 6.0.0 | `21d5188f5bd9a0270d7a2ebf93d41a6b7842ccd2` |
| 6.1.0 | `802e75af261efb4f70d71284d860613a2197b639` |

Protocol 6.1 semantic candidate `be7d05827f52a3029c294c38edf5ede1afb1f9b4` passed fresh 95/95 behavioral qualification and fresh independent D3 Review with no Serious Challenge and zero open blockers. Recovery snapshot `802e75af261efb4f70d71284d860613a2197b639` contains that candidate through ancestry together with the fresh qualification and Review records needed to interpret rollback. The earlier Protocol 6.1 closeout snapshots `dec5ff2767e14fd1cda46e073757aa27f40e270c` and `0c90fda19bf6ed9cb0c4511beb3da80ace6584ed` remain immutable historical evidence but are superseded for current release/recovery authority.

## Deterministic routing dimensions

Protocol 6 keeps three independent routing concerns:

1. **Workflow/domain routing:** classify the earliest affected D1-D4 owner, then use reduced or full concretization paths as required.
2. **Language/runtime routing:** material executable Python/C++ work routes through `references/language-profiles.md` and the matching language profile(s).
3. **Engineering-relation/tool routing:** semantic, structural, property/generative, interprocedural, runtime-state, memory/UB, race, performance, test-effectiveness, architecture-fitness, longitudinal-risk, and failure/recovery questions route to capabilities that directly model the relation.

Static validation proves that referenced files are packaged, directly linked, and structurally reachable. It **cannot prove** that a real harness/model follows the route or invokes an external capability, so live qualification remains a separate evidence class.

## Optional external development capabilities

Serena, Semgrep, Hypothesis, CodeQL, mutation engines, architecture/dependency checkers, complexity/hotspot analyzers, compiler-native analyzers, sanitizers, debuggers, profilers, fuzzers, and similar tools are **optional environment capabilities**. They are **not part of generic Agent Skill validity**, the **direct-directory installation contract**, or reference-routing package validity unless project/task authority explicitly requires one.

Generic bundles do not embed executable paths, credentials, analyzer databases, compiler/toolchain installations, hosted-service configuration, or project-specific query/rule settings. Language/backend/build/runtime support varies independently of skill packaging.

A claim that a particular harness actually exposes or invokes an external capability requires evidence for that **named harness/tool configuration**. Static package validation or reference-routing success does not establish those external-tool claims.

## Bounded reference-routing qualification

Use `qualification/reference-routing/protocol-routing-sentinel/` as a tiny independent Agent Skill. The required answer token exists only in its bundled reference; `SKILL.md` deliberately does not contain the token.

For each harness/model/install mode being claimed, install the sentinel, start a fresh session, request the routing sentinel, verify the reference-backed token, and distinguish discovery, activation, resource-access/path-canonicalization, route-selection, and model-compliance failures.

A simulated parser/local loader cannot establish a real-harness claim. This is **bounded reference-routing qualification**.

## Language-profile routing qualification

When claiming live language routing, use a representative material executable prompt whose language/runtime surface is unambiguous. Static tests may establish protocol-level route/package completeness; they do not establish universal model compliance.

## Bounded live tool-routing qualification

Reference reachability and tool selection are different claims. Use `qualification/tool-routing/SCENARIOS.md` for a **bounded live tool-routing qualification** of each actually available harness/model/tool combination.

Verify the direct relevant reference read where traces are exposed, then verify either specialized invocation or a concrete permitted fallback. Silent preference for built-in search/read/shell/tests after a specialized trigger is not automatically a valid fallback. Record only the combination actually exercised; **do not infer another harness/model/tool** from static tests or a different run.

If no suitable live harness/tool environment exists, static/counterfactual/package tests may establish deterministic protocol-level routing semantics but **must not claim empirical universal model compliance** or an unexecuted harness/tool pass.

## Behavioral qualification

`qualification/ssdp6/SCENARIOS.md` defines Protocol 6 authority, abstraction adequacy, D1/D2/D3/D4 routing, Serious Challenge, anti-deference/anti-stubbornness, historical compatibility, and composed-closure scenarios. `qualification/ssdp6/SCENARIOS-6.1-ADDITIONS.md` extends the Protocol 6.1 set through scenario 95, including the reopened terminology, canonical-navigation, and immutable public-fallback counterexamples. The current second-reopen result is `qualification/ssdp6/RESULTS-GPT-5.6-SOL-2026-09-10-PROTOCOL-6.1-SECOND-REOPENED-95.md`: 95/95 PASS for semantic candidate `be7d05827f52a3029c294c38edf5ede1afb1f9b4`, with no Serious Challenge. The earlier 94/94 and prior Protocol 6.1/Protocol 5 records remain historical evidence for their evaluated candidate/release semantics.

Reference-routing and tool-routing sentinel qualifications remain useful for named harness configurations. Ordinary repository CI does not infer universal model compliance from static tests.