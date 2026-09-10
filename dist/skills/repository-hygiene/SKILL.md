---
name: repository-hygiene
description: Perform conservative post-stage repository cleanup after development is formally closed. Remove proven temporary/cache/test residue, archive completed workplans, repair directory-tree drift, and retire proven disposable branches while preserving useful records, recoverable work, and protected branches.
---

# Repository Hygiene

## Background and terminology

The **Scientific Software Development Protocol (SSDP)** organizes authority into four semantic domains: **D1** scientific/mathematical formulation, **D2** algorithm/numerical method, **D3** software architecture, and **D4** specification/implementation. A **concretization** is a lower-level expression of governing semantic authority. An **evidence realization** is one concrete execution or instantiation of an evidence specification; it is not a D1-D4 concretization.

Use this optional specialist **after a development stage is formally closed**, or when the user explicitly requests a repository-hygiene pass.

## Reference routing

Before substantive repository-hygiene reasoning, apply these explicit routes; load only the reference whose trigger is material.

- Before branch deletion or other material Git/ref operations, **MUST read** [Git and version control](references/git-and-version-control.md).
- Before archiving/closing workplans or reasoning about lifecycle closure, **MUST read** [Workflow and workplans](references/workflow-and-workplans.md).
- When cleanup can affect required regression/integration evidence, read [Testing and validation](references/testing-and-validation.md).
- When protocol/candidate compatibility or evidence invalidation is material, read [Protocol versioning and compatibility](references/protocol-versioning-and-compatibility.md).
- When broad repository inspection or context economy is material, read [Repository intake](references/repository-intake.md).
- When secrets, unsafe artifacts, or trust boundaries are material, read [Security and trust boundaries](references/security-and-trust-boundaries.md).
- When cache/checkpoint/scratch ownership or recovery value is material, read [Storage and I/O](references/storage-and-io.md).
- When tracked/generated/release artifact boundaries are material, read [Release and distribution](references/release-and-distribution.md).
- When distinguishing durable records/evidence from disposable coordination material, read [Documentation and evidence](references/documentation-and-evidence.md).
- Human-facing scientific/technical documentation -> [Scientific and technical writing](references/scientific-technical-writing.md).

It is not a lifecycle role, approval gate, design review, or substitute for implementation. It must not interrupt active engineering merely to make the tree look tidy. Its purpose is to restore a structurally sound, comprehensible repository after substantial design/implementation/test cycles while preserving useful work and history.

Repository hygiene serves long-term repository safety and comprehensibility, not cosmetic closure. Never trade recoverability, useful evidence, active authority, or durable product truth for a superficially tidy tree.

> **Inspect broadly; delete only with positive proof. When classification is uncertain, retain and report.**

## Hard invariants

1. **Never delete, rename away, force-move, or otherwise remove the `main` branch.** This is absolute.
2. Preserve the repository's configured default branch even when it is not named `main`.
3. Never use cleanup as a reason to rewrite history, force-push, bypass protections, discard uncommitted work, or erase unique commits.
4. Never delete a file, directory, branch, worktree, tag, artifact, or record merely because its name looks temporary, old, generated, deprecated, large, or unfamiliar.
5. Preserve accepted scientific/engineering evidence, benchmark closeouts, provenance needed to interpret results, durable specifications/manuals, release records, migrations still needed by supported versions, and other useful historical records.
6. Treat pre-existing user/concurrent changes as protected. A hygiene pass does not own them.
7. Product behavior, scientific semantics, public APIs, and architecture are outside this specialist's authority. If cleanup exposes a semantic/design defect, route it to `software-design`/`software-implementation` rather than silently changing the product.
8. Follow `references/git-and-version-control.md`, project `AGENTS.md`, repository policy, generated-file policy, and more specific project instructions. This specialist does not weaken their authorization boundaries.
9. Tags and releases are not ordinary hygiene targets. Do not delete or rewrite them unless the user separately and explicitly authorizes the exact tag/release operation after its retention value is reviewed.
10. A remote-hosting view is not proof of local filesystem cleanliness. Never claim that untracked, ignored, linked-worktree, or local-only residue is clean unless the local repository state was actually inspected.

## Scope and timing

Run hygiene only when at least one of these is true:

- a substantial development stage/workplan has been accepted and closed;
- a release/merge candidate needs repository-state cleanup;
- accumulated temporary diagnostics, test residue, generated scratch, or directory drift has become materially confusing;
- the user explicitly requests a cleanup audit.

Do not perform repository-wide cleanup after every local change. Active workplans, active diagnostic branches, live checkpoints, running-work outputs, and temporary files still required for unresolved debugging are not cleanup candidates.

Use the fit-for-purpose operating mode; do not take broader cleanup authority than the task needs:

- **audit** — inspect/classify only; make no destructive changes;
- **closeout** — perform authorized path cleanup, archival, and clear hierarchy repair after classification;
- **branch-prune** — separately verify and retire explicitly authorized disposable branches under the high-risk procedure below.

These are reasoning modes, not mandatory workflow gates or persistent protocol state.

## Establish a read-only baseline first

Before changing anything, resolve and record compactly:

- repository root, default branch, current branch/HEAD, remotes, upstreams;
- staged, unstaged, untracked, ignored, conflicted, and pre-existing modified paths;
- linked worktrees, nested repositories, and submodules;
- active and archived workplan locations and any repository indexes governing them;
- repository conventions for source, tests, docs, benchmarks/evidence, build outputs, generated artifacts, scratch/cache, release artifacts, large-file storage, and external data;
- local and relevant remote branches, open/merged PR relationships when available, branch tips, and hosting-platform protection/ruleset information when available;
- project-specific protected or long-lived branch classes.

Do not manufacture a clean baseline by stashing, resetting, cleaning, switching away from user work, or deleting anything.

If the available tooling can inspect only the remote repository, explicitly scope the result to tracked remote state. Remote APIs generally cannot establish local untracked/ignored files, local linked worktrees, local build caches, or unsaved working-tree changes; report those as not inspected rather than inferring they are clean.

## Classify before acting

Classify every cleanup candidate into one of five classes:

| Class | Meaning | Default action |
|---|---|---|
| persistent | current source/specification/docs/tests/fixtures or useful durable evidence/history | retain |
| archival | completed workplan, superseded but useful record, release/history material | move to canonical archive location |
| derived/rebuildable | generated product with a canonical source/build rule | regenerate, retain, or remove according to repository policy |
| disposable | positively identified cache, scratch, editor residue, temporary diagnostic/test output, or abandoned scaffolding with no durable value | remove when authorized and safe |
| ambiguous | ownership/value/reachability is not proven | retain and report |

The burden of proof is asymmetric: retention needs no proof; deletion does.

Useful evidence is not temporary merely because it originated from a test. Prefer compact durable summaries/benchmarks over massive raw scratch when the project has already accepted and summarized the result, but never remove the only evidence needed to reproduce or interpret a material conclusion.

`deprecated` is not synonymous with disposable. A deprecated API/path/data format that remains supported is persistent compatibility material until its support or migration obligation has actually ended.

## Files, caches, and test residue

Safe candidates commonly include known rebuildable caches, temporary build directories, editor/OS residue, temporary diagnostic scripts created solely for a closed investigation, abandoned scratch outputs, and generated test debris. However:

- inspect tracked versus untracked/ignored status;
- identify the owning tool and whether the artifact is reproducible;
- check references from scripts, docs, tests, manifests, CI, workplans, package/release rules, deployment configuration, and automation;
- distinguish fixtures and golden/reference data from transient test output;
- distinguish accepted benchmark/evidence records from raw temporary logs;
- distinguish lockfiles, manifests, generated source shipped by policy, and package indexes from disposable caches;
- never delete external datasets or read-only/shared inputs;
- never use broad `git clean`, wildcard deletion, or recursive deletion when a path-scoped operation suffices;
- do not delete by size alone; a large artifact may be authoritative data, an accepted fixture, an LFS-managed asset, or release material;
- do not broaden `.gitignore` merely to make residue disappear from status. New ignore rules must be narrow enough not to hide legitimate source, fixtures, evidence, or future errors, and ignoring a tracked file is not a substitute for deciding its ownership.

Treat symlinks, submodules, nested repositories, and large-file-managed paths as boundaries rather than ordinary directories:

- classify a symlink itself without recursively following it into an external or unrelated target;
- never delete or modify a symlink target merely because the link is a cleanup candidate;
- treat a submodule/nested repository as a separate repository with its own baseline and authorization; parent cleanup may alter only the gitlink/path when that exact change is justified;
- recognize Git LFS/pointer-managed content and repository large-file policy before concluding that a pointer, fetched object, or local LFS cache is disposable.

Tracked files require stronger evidence than ignored caches. If a tracked file appears obsolete but deleting it changes supported behavior, compatibility, scientific authority, package contents, or externally consumed paths, cleanup must stop at identification and route the change to the owning lifecycle role.

### Sensitive material discovered during cleanup

If logs, scratch, generated artifacts, or history appear to contain credentials, tokens, private keys, or other secrets:

- do not echo the secret into chat, reports, commits, or replacement files;
- treat credential rotation/revocation as the immediate security concern;
- remember that deleting the current working-tree file does **not** erase the secret from existing Git history, mirrors, caches, forks, CI logs, or previously published artifacts;
- do not perform history rewriting, force-pushing, or remote artifact destruction under hygiene authority alone; route any required history/security remediation through explicit operation-specific authorization and applicable security/repository policy.

A cleanup pass must never claim a leaked secret has been remediated solely because the current file was removed.

## Completed workplans

Move a workplan from `active` to `archive` only when the plan itself and accepted project state establish that it is complete. Verify that:

1. its terminal status is complete/accepted/done according to repository convention, or it is explicitly superseded by an accepted successor that owns every remaining obligation;
2. no unresolved gate, blocker, deferred acceptance requirement, or active implementation still depends on treating it as active;
3. any durable closeout result has been preserved in the plan, benchmark/history record, or other canonical owner;
4. references/indexes are updated if the repository maintains them.

Move rather than duplicate when active/archive are mutually exclusive lifecycle locations. Never archive a plan simply because work has paused. If the repository has no established archive location or archival policy, retain the plan in place and report the lifecycle inconsistency rather than inventing an archive hierarchy solely for tidiness.

## Directory-tree structural repair

Correct obvious hierarchy drift only when the canonical destination is supported by repository structure or policy. Examples include misplaced workplans, docs, fixtures, benchmarks, scripts, generated artifacts, or source modules.

Before moving a tracked path:

- establish its semantic owner and canonical directory;
- search for imports, references, links, manifests, CI paths, package-data rules, executable/permission expectations, and external/user-facing paths that may depend on the old location;
- preserve symlink/file type and other materially relevant Git metadata;
- preserve history with a normal move/rename rather than copy-and-delete where practical;
- update directly affected references and run proportionate checks.

Do not reorganize directories for aesthetic symmetry. If the correct hierarchy is genuinely ambiguous, the path is externally consumed as a compatibility contract, or a move implies architectural/module-boundary changes, report it for design/implementation review instead.

## Branch hygiene: high-risk procedure

Branch deletion is a separate high-risk cleanup action. It must follow the Git authorization policy and is never inferred merely from the existence of a hygiene task.

### Absolute protected set

Never delete:

- `main`;
- the repository default branch;
- the currently checked-out branch;
- a branch checked out in any linked worktree;
- a branch with an open PR or active workplan unless the user explicitly resolves that conflict;
- a branch containing commits not proven reachable from a **durable retained ref**;
- a branch whose purpose/status is ambiguous;
- a project-declared protected, release, stable, production, deployment, or other long-lived branch without a separate explicit retention decision.

For this purpose, another disposable scratch/test branch is not a durable retained ref. Prefer proof that needed commits are reachable from `main`, the configured default branch, a retained long-lived integration/release branch, a deliberately retained tag/release ref, or another branch whose continued retention has itself been established.

### Triple-check every candidate

For each proposed deletion, perform three independent checks:

**Check 1 — identity and lifecycle**
- exact branch name and tip SHA;
- purpose is positively identified as temporary/diagnostic/superseded;
- not in the protected set and not referenced by active work;
- inspect repository workflows, CI/deployment configuration, automation, documentation/runbooks, and project metadata for hard-coded dependence on that branch/ref where such use is plausible.

**Check 2 — reachability and integration**
- inspect comparison/merge-base/merged-PR evidence;
- prove there are no unique commits that would become unrecoverable;
- confirm the intended durable replacement/integration branch contains the needed work;
- do not treat a closed/unmerged PR, another soon-to-be-deleted branch, reflog retention, or host-side garbage-collection grace period as durable preservation.

**Check 3 — immediate pre-delete verification**
- refresh/re-read the exact branch target and tip immediately before deletion;
- re-confirm default branch, current/worktree use, open-PR state, branch protection/ruleset state where available, hard-coded operational references where material, and zero material unique work;
- require the refreshed tip SHA to equal the reviewed tip SHA; if it changed, abort deletion and re-audit that branch;
- record the tip SHA in the cleanup report before deleting so an accidental remote/UI mismatch can be diagnosed.

Delete branches **one at a time**, never through broad patterns. Never force-delete merely to bypass a failed safety check. If exact-target destructive authorization is required by repository/tool policy and has not been granted, stop after presenting the verified candidate list for approval.

Remote and local branch deletion are separate actions and require the corresponding authorization. Deleting one never implies permission to delete the other.

## Deprecated and superseded material

Separate three cases:

- **historical but useful**: archive/retain;
- **supported compatibility/deprecation path**: retain until its support/migration obligation expires;
- **truly useless residue**: remove only after proving no active references, unique information, compatibility obligation, or recovery value remains.

Do not convert a hygiene pass into a broad dead-code refactor. Obsolete product machinery that requires semantic reasoning belongs to implementation/design; this specialist may identify it as a cleanup opportunity.

## Apply cleanup conservatively

Prefer small, reviewable, path-scoped changes over one broad deletion sweep. Where practical:

1. perform moves/archive operations before irreversible deletions;
2. inspect the resulting diff/status and directly affected references;
3. remove positively proven disposable paths in coherent small batches;
4. validate tracked-tree cleanup before beginning separately authorized branch pruning.

Do not use cleanup to combine unrelated refactors, formatting changes, dependency updates, or version-control history surgery into the same change set.

## Final structural validation

After cleanup, inspect the repository again and verify proportionally:

- only intended paths changed;
- pre-existing user/concurrent changes are preserved;
- no accidental large binaries, caches, logs, checkpoints, secrets, editor files, or machine-specific paths remain among task-owned changes;
- active/archive workplan state is coherent;
- moved files have no broken directly affected imports/links/manifests/package paths;
- generated artifacts match their canonical-source policy where applicable;
- new ignore rules, if any, are narrow and do not conceal task-owned source/evidence;
- branch list still contains `main`, the default branch, all protected/long-lived branches, and every branch carrying unique or active work;
- each deleted branch had all three recorded checks and the reviewed tip matched the immediate pre-delete tip;
- repository status is actually inspected before describing it as clean.

Run the relevant tests/build/index checks required by the affected paths moved or regenerated. Minimize check cost only after required coverage is established. A hygiene pass should not rerun an expensive scientific or production qualification unless cleanup changed an input that could plausibly invalidate it.

If only remote tracked state was inspectable, say so explicitly in the completion report and do not claim local cache/untracked/worktree cleanliness.

## Completion report

Report concisely:

- retained persistent/ambiguous material that was intentionally not deleted;
- temporary/cache/test residue removed;
- workplans archived and indexes updated;
- structural moves and directly affected references repaired;
- branches deleted, with their recorded tip SHAs and evidence that they were disposable/integrated;
- verified deletion candidates intentionally left pending authorization;
- checks actually run, local-versus-remote inspection scope, and any unresolved structural ambiguity or security issue.

A successful hygiene pass leaves the repository easier to navigate and safer to continue from, without losing useful work, evidence, history, or branch recoverability and without changing the accepted engineering doctrine.
