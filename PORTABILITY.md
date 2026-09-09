# Agent portability and routing qualification

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
2. otherwise use the canonical public repository `https://github.com/hjin98/scientific-software-development-protocol` and its `source/` entrypoint plus required references;
3. preserve the workplan's protocol binding; never guess a semantic version as a Git ref or silently substitute current doctrine;
4. report truthful non-closure if no compatible source can be read.

Before mutation classify the highest potentially affected D1/D2/D3/D4 domain and direct governed side constraints. Reduced routes are normal; do not force every task through all four skills.

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
| 6.1.0 | `dec5ff2767e14fd1cda46e073757aa27f40e270c` |

The Protocol 6.1 commit is the final document-controlled/semi-automated pre-Protocol-7 rollback snapshot. It contains the qualified current source/profile and required generated artifacts plus the completed 6.1 lifecycle record. Protocol 7 fallback uses that immutable snapshot as a version rollback; it does not keep a second live canonical control plane.

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

`qualification/ssdp6/SCENARIOS.md` defines Protocol 6 authority, abstraction adequacy, D1/D2/D3/D4 routing, Serious Challenge, anti-deference/anti-stubbornness, historical compatibility, and composed-closure scenarios. Existing Protocol 5 qualification remains historical evidence for its release semantics.

Reference-routing and tool-routing sentinel qualifications remain useful for named harness configurations. Ordinary repository CI does not infer universal model compliance from static tests.