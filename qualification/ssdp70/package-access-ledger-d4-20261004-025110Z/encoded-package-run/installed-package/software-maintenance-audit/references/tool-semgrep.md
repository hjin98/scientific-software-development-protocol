# Semgrep: Structural Analysis and Variant Evidence

Use Semgrep for AST-aware structural queries, static checks, and variant analysis when its rule/language/engine model matches the material claim.

## Selection boundary

Prefer Semgrep when the relation under the claim is structural: repeated unsafe or nonconforming constructs, API misuse, diagnosed bug variants, security-sensitive patterns, forbidden/legacy paths, ownership/structure invariants, structural absence/uniqueness, or independent-review structural checks.

Do not route a purely literal lookup through Semgrep merely because a rule could be written. Do not use Semgrep as a substitute for interprocedural/data-flow analysis when the claim materially depends on those relations.

When a Semgrep-class question is triggered, read this method before relying solely on textual search. If Semgrep availability/engine capability is unknown, use a cheap non-mutating capability probe when practical. When available/supported and its structural model directly fits the claim, presumptively use it; otherwise take a concrete fallback without weakening the claim.

## Portable baseline and capability boundaries

Generic protocol guidance assumes **local Semgrep Community Edition-compatible scanning**. Paid or proprietary cross-file/interfile analysis, managed scanning, cloud triage, and AI/managed workflows are optional capabilities, not generic skill requirements.

If a richer engine or edition is available, use advanced analysis only when that capability is actually active. State negative or completeness claims no more broadly than the selected engine, language, rule, and dataflow model support.

## Rule quality and interpretation

Prefer focused rules tied to the current concern when broad scanning would mainly produce noise. A finding is evidence requiring repository-context triage; it is not automatically a defect, requirement, or blocker.

For an acceptance-critical custom rule, validate the rule itself against representative **known-positive and known-negative** examples or equivalent rule tests before trusting its positive or zero-finding result. The rule must demonstrate that it can match a construct that should match and remain quiet on one that should not.

When a rule encodes a durable project invariant, version the rule, tests, or configuration when ongoing enforcement justifies the maintenance cost. A one-off inspection need not become permanent rule infrastructure; preserving the exact rule/command is sufficient when that adequately establishes the claim.

Broad community or automatic rulesets may be useful for exploratory discovery. Their findings enter normal affected-surface/scope reasoning rather than mechanically becoming required work.

## Negative evidence and scan scope

A `0 findings` result is **meaningful only relative to the actual scan contract**. For an acceptance-critical negative claim, account for material dimensions that could hide matches:

- exact rule/configuration and active Semgrep engine/edition;
- **target paths and languages actually scanned**;
- `.gitignore`, `.semgrepignore`, default exclusions, explicit include/exclude flags, generated/vendor exclusions, or managed targeting that can remove files;
- inline suppressions such as `nosemgrep` and relevant project/platform triage or ignore state;
- **rule and analysis limitations that can create false negatives**.

The command/configuration plus relevant source and scan output is normally enough evidence; do not create a permanent report merely to restate it.

## External services and generated fixes

Acceptance-critical rules should not depend solely on a **volatile network-fetched ruleset** when exact rule identity materially affects the claim. Pin, version, or otherwise govern that identity proportionately.

Do not silently upload private source/findings or invoke managed/cloud workflows. Any external service that receives source, findings, or credentials crosses a trust boundary and requires explicit project/user authorization and applicable security policy.

Autofix, rule `fix`, AI remediation, or another generated patch is **ordinary implementation output**. Review the resulting source/diff and apply the **same conformance and functional acceptance** as for manually written changes. Semgrep never replaces real-owner execution, affected regression, integration, runtime security testing, or another project-required analyzer when those claims are material.

## Family and review use

For a recurring material family, turn a diagnosed unsafe/nonconforming construct into a focused structural variant scan when structure provides a useful bounded census. Preserve known-positive/known-negative validation and honest scan-scope/false-negative accounting before relying on zero findings. Use semantic/runtime/configuration cross-checks when structural matching cannot see material members.
