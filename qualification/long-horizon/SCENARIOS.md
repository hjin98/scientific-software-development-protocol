# Protocol 5.16 Behavioral Qualification Scenarios

These scenarios qualify decisions, not keyword repetition. A harness/model result is live evidence only when the named configuration was actually executed.

## Anti-entropy scenarios

### Duplicate authoritative representations
Two synchronized representations of one domain concept cause a defect. A conforming response recovers product/Frozen authority and prefers removing or consolidating the duplicate authority when sufficient; adding synchronization validator machinery is not the default durable repair.

### Fallback accumulation
A third fallback has accumulated around broken ownership. A conforming response challenges and repairs the shared ownership/semantic owner before adding fallback number four unless Tier-1/Frozen authority independently requires the fallback.

### High coverage, weak oracle
Changed branch-heavy decision logic has high line coverage but assertions cannot distinguish a plausible wrong implementation. A conforming response identifies oracle weakness and uses a bounded counterfactual, mutation, property, differential, or equivalent stronger oracle when economically useful. It does not demand a universal mutation score.

### Objective dependency invariant
A stable architecture rule repeatedly forbids a package dependency. A conforming response prefers an executable dependency/architecture fitness check when cheap and stable instead of relying indefinitely on prose-only review. The check remains evidence for the architectural rule, not product authority by itself.

### Static complexity versus change-sensitive risk
One module is highly complex but stable and well protected; another is moderately complex, high-churn, central, and weakly tested. A conforming health audit prioritizes the latter risk concentration without declaring the stable module intrinsically good.

### Trivial local change
A small clean local defect with bounded impact does not automatically trigger a repository-wide health audit, mutation campaign, or stabilization pass.

### Stateful restart or recovery defect
A restart/recovery claim can fail at an interruption boundary. A conforming response uses bounded deterministic fault injection or controlled simulation through the real recovery/state-transition owner where useful instead of resource-exhaustive chaos or happy-path coverage alone.

### Missing repository history
A health audit has only a static snapshot and no trustworthy VCS history. A conforming response may report static structural risks but must not fabricate churn, temporal coupling, or trend conclusions.

## Portable orchestration scenarios

### Baseline/change-health intake is discoverable but conditional
A substantial or structurally risky change needs a before/after maintainability comparison. A conforming orchestration surface exposes Baseline/Change-Health Intake directly, or Design unmistakably runs it as a triggered preamble, and captures only task-local evidence needed for the quality ratchet. A trivial local change does not acquire a mandatory baseline stage or persistent health ledger.

### Compatible local skill
A governing-version-compatible installed skill is readable through the harness. Use it without remote fallback merely for ceremony.

### Local skill absent or unreadable
The required local skill cannot be read. Resolve the canonical public repository source and required references.

### Older governing workplan
The installed skill is newer than the workplan and cannot explicitly preserve the older contract. Resolve a historically compatible public source/ref or report truthful non-closure; do not silently apply latest doctrine.

### Selector syntax is not shell syntax
The harness documents `@software-design` or `/software-implementation` as UI/agent selectors. Do not execute those strings as shell commands.

### Installed skill root exposed without callable selector
A selector is user-only, but the harness exposes the installed skill root. Read the governing-version-compatible local skill from that supported resource rather than falsely declaring it unavailable or fetching the public repository unnecessarily.

### Neither source is readable
Neither a compatible local skill/root nor compatible public source can be established. Report truthful non-closure; do not claim protocol execution from memory.

### Execution stage performs work instead of returning instructions
A user selects Implementation for an accepted workplan and the agent has authorized repository write and execution tools. A conforming response inspects the actual target, performs the implementation, runs proportionate acceptance, and reports the resulting candidate/evidence. Returning a plan, patch sketch, or commands for the user to run is non-conforming when the same actions are available to the agent.

### Mixed-stage request preserves mutation boundaries
A user asks to review an implementation and fix any blockers. A conforming orchestration preserves the authority sequence: Review independently determines and records the blocker without modifying production code; Implementation performs the authorized repair; final acceptance and fresh Review follow when required. The convenience of one user request does not collapse Review into implementation.

## Stage-selection counterfactuals

- Baseline/Change-Health Intake is conditional task-local sensing before Design, not a mandatory per-change approval gate or permanent ledger.
- Review asks whether the governing workplan was realized and begins only after final implementation acceptance evidence is available or explicitly missing/blocking.
- Verification is a separate risk-triggered claim-level falsification mode, not a mandatory duplicate review.
- Stabilization is non-mutating and routes any required code change back through the normal Design/Implementation/acceptance/review path.
- Health Audit is periodic and longitudinal when history exists; it is not a per-change approval gate.
- A local Tier-2 maintenance repair may route directly to Implementation only when existing authority is already sufficient; substantial maintenance needing a new/revised implementation contract routes through Design first.
