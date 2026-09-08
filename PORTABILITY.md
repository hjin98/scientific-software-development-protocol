# Agent portability and routing qualification

Protocol 6 preserves the portable Agent Skill contract while adding first-class D1/D2 roles and a dual-version orchestration profile.

## Installation contract

The runtime unit is the self-contained directory `dist/skills/<skill-name>/`; the top-level ZIP contains identical files under one enclosing skill directory. Install each skill as a direct child of the harness-supported skill root so `<skills-root>/<skill-name>/SKILL.md` exists. `source/` is canonical development source, not the runtime bundle.

Current authority-bearing skills:

- `scientific-formulation`
- `numerical-algorithm-design`
- `software-design`
- `software-implementation`

Optional specialists: `software-documentation`, `software-maintenance-audit`, `repository-hygiene`.

## Human-facing orchestration

`source/shared/references/development-workflow-prompts.md` is the canonical prompt source. With `AUTO_LOCAL_FIRST`:

1. use a governing-version-compatible installed skill/ exposed skill root through the harness-native mechanism;
2. otherwise use the canonical public repository `https://github.com/hjin98/software-development-protocol` and its `source/` entrypoint plus required references;
3. preserve the workplan's protocol binding; never guess a semantic version as a Git ref or silently substitute current doctrine;
4. report truthful non-closure if no compatible source can be read.

Before mutation classify the highest potentially affected D1/D2/D3/D4 domain and direct governed side constraints. Reduced routes are normal; do not force every task through all four skills.

## Orchestrator profile compatibility

The Core supports independent version-bound profiles:

| Profile | Protocol | Profile schema | Purpose |
| --- | --- | ---: | --- |
| `sdp-protocol-5.16` | 5.16.0 | 1 | frozen historical compatibility |
| `ssdp-protocol-6.0` | 6.0.0 | 2 | current domain-aware workflow |

Historical 5.16 prompt/profile bytes remain immutable. A workplan's declared `protocol_version` selects its compatible profile before stage semantics are interpreted. Project profile configuration is a default, not authority to override an explicit workplan version.

Protocol 6 profile stages include authority intake, D1, D2, D3, D4, Review/Challenge, Verification, Stabilization, Alignment, Health Audit, and Closeout. Serious Challenge/human-pending outcomes stop automatic normal routing; the orchestrator records/routes state but never decides scientific truth.

## Other deterministic routing dimensions

Language/runtime routing remains under `references/language-profiles.md`; material Python/C++ surfaces load the matching profile(s). Engineering-relation routing selects Serena/Semgrep/Hypothesis/CodeQL or other capabilities only when their relation matches the claim. External development tools are optional environment capabilities unless project/task authority explicitly requires them.

Static package validation proves structural reachability and byte/source parity; it does not prove that a named live harness/model actually follows the route. Live harness/tool/model claims require executed qualification for that exact configuration.

## Behavioral qualification

`qualification/ssdp6/SCENARIOS.md` defines Protocol 6 authority, abstraction adequacy, D1/D2/D3/D4 routing, Serious Challenge, anti-deference/anti-stubbornness, historical compatibility, and composed-closure scenarios. Existing Protocol 5 qualification remains historical evidence for its release semantics.

Reference-routing and tool-routing sentinel qualifications remain useful for named harness configurations. Ordinary repository CI does not infer universal model compliance from static tests.
