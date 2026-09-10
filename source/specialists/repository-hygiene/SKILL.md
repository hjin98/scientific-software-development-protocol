---
name: repository-hygiene
description: Perform conservative post-stage repository cleanup under Protocol 6.2: classify residue, archive genuinely completed workplans, repair clear structural drift, and retire proven disposable branches/artifacts while preserving recoverable work, evidence, compatibility, history, and protected refs.
---

# Repository Hygiene

Optional post-stage cleanup specialist. Use after formal development closure or when explicitly requested; do not interrupt active engineering merely to make a tree look tidy. Repository safety/recoverability outrank cosmetic cleanliness.

> **Inspect broadly; delete only with positive proof. When classification is uncertain, retain and report.**

## Routing

Before substantive reasoning read [Abstraction, concretization, authority, challenge, and representation](references/abstraction-and-concretization.md). Load only triggered concern owners:

- branch/ref deletion or material Git operations -> [Git and version control](references/git-and-version-control.md);
- workplan archive/lifecycle closure -> [Workflow and workplans](references/workflow-and-workplans.md);
- broad inspection/context economy -> [Repository intake](references/repository-intake.md);
- cleanup affecting executable evidence -> [Testing and validation](references/testing-and-validation.md);
- protocol/candidate compatibility -> [Protocol versioning](references/protocol-versioning-and-compatibility.md);
- secrets/trust -> [Security and trust boundaries](references/security-and-trust-boundaries.md);
- cache/checkpoint/scratch ownership -> [Storage and I/O](references/storage-and-io.md);
- tracked/generated/release artifacts -> [Release and distribution](references/release-and-distribution.md);
- durable record vs disposable coordination material -> [Documentation and evidence](references/documentation-and-evidence.md).

Ordinary hyperlinks/package membership are not activation commands.

## Hard boundaries

Never delete/force-move `main`, the configured default branch, current/worktree branches, protected/long-lived refs, unique work, active authority/evidence, required compatibility/migrations, or pre-existing user/concurrent changes. Never use hygiene to rewrite history, force-push, bypass protections, discard uncommitted work, change product/scientific semantics, or infer local cleanliness from a remote-only view. Tags/releases require separate explicit operation-specific authorization.

If a sensitive credential may exist, do not echo it. Removing a working-tree file does not erase Git/history/cache/publication exposure; route rotation/history remediation through the applicable security/Git authority rather than claiming cleanup solved it.

## Classification and action

Establish a read-only baseline first: repository/ref/worktree state available to the tool, active/archive workplans/indexes, source/test/doc/evidence/generated conventions, and relevant protections. Do not manufacture cleanliness by reset/stash/clean/switch/delete.

Classify candidates:

| Class | Default |
| --- | --- |
| persistent current source/spec/docs/tests/fixtures/evidence | retain |
| archival completed/superseded useful record | move only to established archive location |
| derived/rebuildable | follow canonical generation/release policy |
| disposable proven cache/scratch/editor/test residue | remove when authorized and safe |
| ambiguous | retain and report |

`deprecated` is not `disposable`; supported compatibility remains persistent. Symlinks, submodules/nested repositories, LFS/external data, generated source, fixtures/goldens, benchmarks/evidence and package/release material require owner-aware classification rather than name/size heuristics.

Archive a workplan only when current authority/state proves it complete or an accepted successor owns every remaining obligation; update maintained indexes. A paused plan is not complete.

Move tracked paths only when the canonical destination is established and imports/links/manifests/CI/package/public compatibility are reconciled. Do not reorganize for aesthetic symmetry.

Branch deletion is high-risk: use the exact Git-owner procedure, prove lifecycle identity and no active reference, prove all needed commits reachable from a durable retained ref, refresh the exact tip/protection/worktree/PR state immediately before deletion, require the reviewed tip to match, and delete only the individually authorized target. Local and remote deletion are separate actions.

Prefer small path-scoped cleanup over wildcard/recursive sweeps. Do not broaden `.gitignore` merely to hide unresolved ownership.

## Final validation and report

After cleanup verify only intended paths/refs changed, active/archive state and directly affected routes remain coherent, generated outputs still follow canonical-source policy, protected/unique work remains, and affected tests/build/index checks execute when required. If only remote tracked state was inspectable, say so explicitly.

Report concisely what was retained because persistent/ambiguous, removed as proven disposable, archived/moved with affected references, branch operations with exact tips and proof/authorization, checks actually executed, and unresolved structural/security ambiguity. Apply the Lossless Representation Rule: preserve decisions/evidence needed to continue safely without replaying routine inspection history.
