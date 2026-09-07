# Agent portability and routing qualification

Protocol 5.9 established the portable skill-routing/distribution contract. Protocol 5.13 made optional-tool routing deterministic per material relation. Protocol 5.15 added deterministic language-profile routing. Protocol 5.16 preserves those contracts and adds a human-facing stage-orchestration entrypoint with compatible-local-first/public-repository-fallback skill resolution.

The runtime installation unit remains the self-contained directory under `dist/skills/<skill-name>/`; the top-level ZIP with the same skill name contains identical files under one enclosing skill directory.

## Installation contract

Install each skill as a direct child of a harness skill root so the entrypoint is exactly `<skills-root>/<skill-name>/SKILL.md`. Do not install `source/roles/...` or `source/specialists/...` directly as a runtime bundle: canonical source references become self-contained only in generated bundles.

Use a harness-supported shared `.agents/skills` root when available or the harness-native root when required. Harness-specific paths are integration guidance, not protocol doctrine; verify them against the harness version being qualified.

ZIPs are transport artifacts: extract the enclosing `<skill-name>/` directory before placing it under a runtime skill root. A symlinked/shared installation is a separate harness capability and must be qualified on that harness; the **direct-directory installation contract** is the portability baseline.

## Human-facing workflow orchestration

The canonical prompt entrypoint is `source/shared/references/development-workflow-prompts.md`. Each stage defines task inputs once and resolves its required skill using `AUTO_LOCAL_FIRST` by default.

1. Inspect the current harness skill/plugin/command registry or documented exposed installed-skill root.
2. Use a readable local skill when it can preserve the protocol contract governing the task. Harness selectors such as `@software-design` or `/software-implementation` are examples of native selectors, **not shell commands**.
3. If local resolution fails, use the public canonical repository `https://github.com/hjin98/software-development-protocol` and read the appropriate `source/roles/<skill>/SKILL.md` or `source/specialists/<skill>/SKILL.md` plus required references.
4. Preserve version binding. A newer installed skill does not silently reinterpret an older workplan. Resolve a historically compatible source/ref from evidence; do not guess that a semantic version string is a Git ref.
5. If neither source is readable, report the limitation rather than claiming skill execution from memory.

This orchestration surface routes into the protocol; it is not a parallel source of product or architectural authority.

## Deterministic routing dimensions

Protocol 5.16 has three independent routing concerns:

1. **Workflow-stage routing:** Design, Implementation, Review, risk-triggered Verification, Stabilization, Alignment, Health Audit, and Closeout activate their appropriate role/specialist mode.
2. **Language/runtime routing:** material executable Python/C++ work routes through `references/language-profiles.md` and the matching language profiles.
3. **Engineering-relation/tool routing:** semantic, structural, property/generative, interprocedural, runtime-state, memory/UB, race, performance, test-effectiveness, architecture-fitness, longitudinal-risk, and failure/recovery questions route to capabilities that directly model the relation.

Static validation proves that referenced files are packaged, directly linked, and structurally reachable. It cannot prove that a real harness/model follows the route or invokes an external capability, so live qualification remains a separate evidence class.

## Optional external development capabilities

Serena, Semgrep, Hypothesis, CodeQL, mutation engines, architecture/dependency checkers, complexity/hotspot analyzers, compiler-native analyzers, sanitizers, debuggers, profilers, fuzzers, and similar tools are **optional environment capabilities**. They are **not part of generic Agent Skill validity**, the **direct-directory installation contract**, or reference-routing package validity unless project/task authority explicitly requires one.

Generic bundles do not embed executable paths, credentials, analyzer databases, compiler/toolchain installations, hosted-service configuration, or project-specific query/rule settings. Language/backend/build/runtime support varies independently of skill packaging.

A claim that a particular harness actually exposes or invokes an external capability requires evidence for that **named harness/tool configuration**. Static package validation or reference-routing success does not establish those external-tool claims.

## Bounded reference-routing qualification

Use `qualification/reference-routing/protocol-routing-sentinel/` as a tiny independent Agent Skill. The required answer token exists only in its bundled reference; `SKILL.md` deliberately does not contain the token.

For each harness/model/install mode being claimed, install the sentinel, start a fresh session, request the routing sentinel, verify the reference-backed token, and distinguish discovery, activation, resource-access/path-canonicalization, route-selection, and model-compliance failures.

A simulated parser/local loader cannot establish a real-harness claim. This is **bounded reference-routing qualification**.

## Language-profile routing qualification

When claiming live language routing, use a representative material executable prompt whose language/runtime surface is unambiguous. Expected trace when observable:

```text
lifecycle SKILL.md
-> references/language-profiles.md
-> matching Python or C++ profile
-> shared domain references/tools only as triggered by the engineering question
```

Static tests may establish protocol-level route/package completeness; they do not establish universal model compliance.

## Bounded live tool-routing qualification

Reference reachability and tool selection are different claims. Use `qualification/tool-routing/SCENARIOS.md` for a **bounded live tool-routing qualification** of each actually available harness/model/tool combination.

Verify the direct relevant reference read where traces are exposed, then verify either specialized invocation or a concrete permitted fallback. Silent preference for built-in search/read/shell/tests after a specialized trigger is not automatically a valid fallback. Record only the combination actually exercised; **do not infer another harness/model/tool** from static tests or a different run.

If no suitable live harness/tool environment exists, static/counterfactual/package tests may establish deterministic protocol-level routing semantics but **must not claim empirical universal model compliance** or an unexecuted harness/tool pass.

## Protocol 5.16 behavioral and orchestration qualification

`qualification/long-horizon/SCENARIOS.md` defines bounded semantic scenarios for anti-entropy decisions, oracle strength, architecture fitness, change-sensitive risk, bounded fault injection, missing-history behavior, stage selection, and local-first/public-fallback routing.

Static tests can prove that these scenarios and routes exist. A claim that a named model/harness actually makes the intended decision requires an executed run of that **named harness/tool configuration** or named harness/model configuration. Never generalize one live result to another configuration.

## Compatibility matrix

Record actual qualification results in release/PR closeout when relevant. Do not infer a pass from static validation.

| Harness | Direct-directory/reference routing | Workflow skill resolution | Language-profile routing | Tool routing | 5.16 behavioral scenarios | Notes |
| --- | --- | --- | --- | --- | --- | --- |
| Codex/OpenAI | unqualified | unqualified | unqualified | unqualified | unqualified | Qualify the actual installed model/tool configuration. |
| Claude Code | unqualified | unqualified | unqualified | unqualified | unqualified | Qualify only installed/exposed capabilities actually exercised. |
| Pi | unqualified | unqualified | unqualified | unqualified | unqualified | Qualify only installed/exposed capabilities actually exercised. |
| Gemini CLI / Antigravity | unqualified | unqualified | unqualified | unqualified | unqualified | Qualify only installed/exposed capabilities actually exercised. |
| GitHub Copilot | unqualified | unqualified | unqualified | unqualified | unqualified | Qualify only installed/exposed capabilities actually exercised. |
| DeepSeek Harness | unqualified | unqualified | unqualified | unqualified | unqualified | Qualify only installed/exposed capabilities actually exercised. |

Ordinary repository CI intentionally does not call external agents. Live qualification may enter CI only if credentials, harness/model/tool versions, cost, and stochastic behavior become stable enough to make it a reliable release signal.
