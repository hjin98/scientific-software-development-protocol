# Repository agent instructions

`source/` is canonical protocol source. Do not hand-edit generated `dist/` or orchestrator protocol snapshots when canonical generation exists.

Act as an engineering steward of the stakeholder's durable product. Workplans, tests, gates, metrics, reviews and reports are constraints/evidence, not objectives. Follow explicit user/task authority first; use a named governing workplan under its declared protocol version rather than assuming every active-plan file governs every task.

For D1/D2/D3/D4 work enter the corresponding `source/roles/*/SKILL.md`; for documentation, maintenance audit, or repository hygiene use the matching specialist when triggered. The role/specialist entrypoint owns root routing. Read `source/shared/references/abstraction-and-concretization.md` plus the owning domain/concern, then activate further references only when their explicit decision predicate fires. Ordinary hyperlinks, semantic-dependency edges and package membership do not imply active reads. Reuse already-established material only while its protocol/source/workplan/candidate/regime/scope remains applicable.

Apply the Protocol 6.2 Lossless Representation Rule to plans, handoffs, reports and agent communication: preserve complete governed meaning first; use one detailed generic owner; prefer local delta + resolvable route; make Serious Challenge/blockers/current decisions/material uncertainty prominent; keep history/raw/specialized detail cold but discoverable; never drop a lower-salience mandatory closure condition for brevity.

When acceptance requires a real production semantic owner/consumer, do not replace or bypass that owner and claim its behavior accepted. Required unexecuted checks are blocking. If accepted authority itself may be materially false, contradictory, ambiguous, inadequate or unrealizable, surface `SERIOUS CHALLENGE` and route the earliest affected owner instead of patching around it.

Before Protocol 6.2 completion run the repository acceptance workflow documented in `README.md`/CI, including tests, package build/independent validation, committed-distribution parity, whitespace checks, and Orchestrator Core snapshot/tests when affected. Protocol 6.1 remains accepted-current/rollback until the 6.2 lifecycle explicitly closes.
