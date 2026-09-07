# Git and Version-Control Policy

## Purpose and precedence

Use this policy for work inside a Git repository. It protects repository history, concurrent work, and data boundaries without assuming every task needs a new branch, worktree, commit, or remote action.

Before acting, read the repository-root `AGENTS.md` and every applicable nearer `AGENTS.md` for the files in scope. Recheck instructions when work crosses into another directory tree. Project instructions may define branch names, worktree use, generated-file ownership, required checks, commit conventions, or stricter authorization rules. Follow the most specific applicable project rule. Project instructions do not override the user's scope, platform safety requirements, or the need for explicit authorization for consequential external or history-changing actions. If instructions conflict or would endanger unrelated work, stop and report the conflict.

### Permanent branch invariant

The branch named `main` is permanently protected by this protocol. **Never delete `main`, rename it away as a cleanup action, or force-move it in a way that discards its reachable history.** Normal authorized commits, merges, and fast-forward updates to `main` remain ordinary development operations. Also preserve the repository's configured default branch when it is not named `main` unless a separately authorized default-branch migration has first established and verified its durable replacement; such a migration still does not authorize deleting `main`.

## Establish the baseline

Perform read-only reconnaissance before editing tracked files or changing Git state:

1. Resolve the repository root and confirm the intended target is inside it. Detect nested repositories, submodules, and linked worktrees rather than assuming the nearest parent is the only repository.
2. Inspect the current branch or detached-HEAD state, HEAD commit, upstream/tracking relationship, and configured remotes relevant to the task. Do not fetch merely to make remote state current unless network access and that external read are within scope.
3. Inspect staged, unstaged, untracked, ignored, and conflicted paths. Use a machine-readable or unambiguous status form when available. Inspect existing diffs for files that may overlap the requested change.
4. Inspect linked worktrees and determine whether the intended branch is already checked out elsewhere before switching, creating, deleting, or reusing a branch/worktree.
5. Read enough recent history, blame, or adjacent commits to understand local conventions only when it materially informs the change. History is evidence, not authority over current code, tests, specifications, or `AGENTS.md`.
6. Record a compact baseline: repository root, branch/detached state, HEAD, relevant upstream, pre-existing modified/untracked/conflicted paths, and any worktree or submodule constraints.

Treat a dirty worktree as normal evidence, not a condition to "fix." Distinguish pre-existing state from changes made during the task so the completion report can account for both.

## Protect user and concurrent work

- Never delete, overwrite, revert, reformat, stage, or commit unrelated changes. Do not assume a change is disposable because it is untracked, ignored, generated-looking, or failing tests.
- Inspect overlapping edits before modifying a dirty file. Preserve them and make a minimal compatible change. If safe separation is not possible, stop and ask rather than choosing which work survives.
- Do not use `git stash` to hide user or concurrent changes unless the user explicitly authorizes the exact operation. A stash changes shared repository state and can be lost, conflicted, or mistaken for task-owned work.
- Do not switch branches in a worktree when doing so would disturb uncommitted work, running processes, or another agent. Do not edit, relocate, lock, unlock, prune, or remove a worktree you did not create for the current task without explicit authorization.
- Treat submodules as separate repositories. Do not update a submodule checkout or parent gitlink incidentally; each change requires the same state inspection and scope discipline as any other repository change.
- Do not make broad formatting, dependency-lock, generated-file, or line-ending changes solely to obtain a clean diff.

When unrelated changes prevent verification, run safe path-limited checks where meaningful and report the limitation. Do not manufacture a clean tree by modifying the user's state.

## Branches and worktrees

Use the current branch/worktree when it is safe, project instructions allow it, and isolation would not materially reduce risk. Consider an isolated branch or linked worktree for nontrivial or concurrent work, especially when the current tree is dirty, but do not create one reflexively.

Before creating or switching:

- honor project naming, base-branch, and worktree-location rules;
- confirm the chosen base commit and whether remote freshness matters;
- ensure the branch is not already checked out in another worktree;
- choose a location that will not nest one repository inside another or place generated/build output into a tracked tree;
- state whether uncommitted changes will remain in the original worktree.

Creating, switching, renaming, deleting, or force-updating a branch/worktree is a repository-state mutation. Do it only when requested, required by applicable project workflow, or clearly necessary to complete the authorized task without disturbing existing work. Report any branch or worktree created. Do not delete task-created isolation at completion if it contains unmerged or otherwise unrecoverable work; removal must be safe, scoped, and authorized. The permanent `main` invariant above always applies and cannot be bypassed by a general cleanup request.

## Destructive and history-changing operations

Do not run commands that can discard work or rewrite history without explicit, operation-specific user authorization after resolving the exact targets and explaining the effect. This includes, but is not limited to:

- hard or destructive reset;
- `git clean` or deletion of untracked/ignored files;
- checkout/restore of paths that would discard content;
- forced branch switching, deletion, or ref movement;
- commit amendment, interactive or non-interactive rebase, history filtering, reflog expiration, or aggressive pruning;
- force push or deletion/overwrite of remote refs, tags, or branches.

Prefer a non-destructive alternative such as a new corrective commit, a patch, a new branch, or preserving a recoverable copy. Explicit authorization for one target or operation does not authorize adjacent cleanup, other branches/worktrees, or later repetitions. Never use a destructive Git command merely to simplify the task or make tests pass. No authorization can make deletion of `main` a valid cleanup action under this protocol.

## Authorization boundaries

Local inspection, scoped edits, and validation do not imply permission to publish, integrate, or rewrite history.

- Do not push, merge, rebase, create/delete/move tags, open/update/close a pull request, or otherwise change remote repository state unless the user explicitly requests that specific class of action.
- Do not infer authorization from credentials being present, a remote being configured, project automation being available, or a request to "finish" an implementation.
- Do not bypass branch protections, required reviews, signing rules, hooks, CI, or policy checks. If a required control cannot run, report it as blocked or not run.
- Create a local commit only when the user requested commits or an applicable project workflow clearly requires one. Do not amend, squash, sign on another person's behalf, or alter authorship without explicit authorization.
- Fetching is read-only with respect to the remote but changes local refs and uses the network. Perform it only when current remote state is relevant and network access is authorized. Pulling is an integration action; do not use it as a substitute for an explicitly considered fetch plus merge/rebase decision.

If an authorized remote action would include commits or files outside the task, stop and show the scope before proceeding.

## Diff, staging, and commit hygiene

Review the repository state throughout the task and before completion:

1. Compare the final state with the recorded baseline. Inspect both unstaged and staged diffs, including summaries and changed-file lists.
2. Review each changed path for task relevance, accidental generated artifacts, secrets, credentials, private data, large binaries, caches, logs, checkpoints, build output, editor state, machine-specific paths, permission changes, and unintended line-ending churn.
3. Run whitespace/error checks and project-required formatting or validation where appropriate, without applying unrelated mass rewrites.
4. Stage only explicit task-owned paths or hunks. Avoid broad staging commands in a dirty worktree. Reinspect the staged diff before committing.
5. Keep each requested commit coherent: one explainable change with its tests and required documentation. Use the project's message convention; do not mix unrelated cleanup or transient evidence.
6. Do not skip hooks or checks unless the user explicitly authorizes the bypass and the completion report identifies what was skipped and why.

At handoff, report the branch/worktree used, commits created (if any), task-owned modified paths, pre-existing changes still present, and any untracked or staged state relevant to the user. Never describe the repository as clean without checking.

## Version and documentation state in Git

Treat version files, current specifications, architecture manuals, implementation workplans, history/changelog entries, and generated permanent-document PDFs as one review surface when a workplan/release changes documented behavior.

- Identify the authoritative package/release version source and do not create divergent duplicates.
- Stage the code change together with required current-specification updates, any actual current-architecture update, workplan/evidence state, history/version record, tests, and generated permanent-document PDF(s) when repository policy tracks generated docs.
- Inspect generated PDFs and other binaries for unexpected size growth before staging.
- If the repository deliberately excludes generated PDFs from Git, still build/verify them and report them as release artifacts; do not add ignored binaries merely to satisfy this protocol.
- Do not use a version bump to hide unrelated changes or collapse multiple incomplete workplan gates into a misleading release record.

## External and read-only data directories

Treat data outside the repository—mounted datasets, shared corpora, user-provided archives, model weights, production snapshots, and other external directories—as external inputs unless the user and project policy explicitly say otherwise.

- Do not initialize Git in an external data directory, add it as a worktree, move it into the repository, or modify/delete its contents as part of source control cleanup.
- Treat directories identified as read-only by mounts, permissions, task context, `AGENTS.md`, or project documentation as immutable even if a command could technically write to them.
- Do not stage external data through symlinks, submodules, large-file tooling, generated manifests, or copied snapshots. `.gitignore` prevents ordinary tracking; it does not grant permission to write, transform, or delete data.
- Keep temporary outputs, indexes, caches, and derived evidence in a project-sanctioned scratch/output location. Do not place them beside read-only source data.
- Copy only the smallest necessary, non-sensitive, license-compatible fixture into the repository when the task explicitly requires a tracked test artifact and project policy permits it. Record its origin and transformation when provenance matters.
- Use path-scoped Git commands from the verified repository root so similarly named external paths cannot become accidental targets.

If repository behavior depends on unavailable or immutable external data, validate with an approved fixture or report the relevant check as blocked; do not alter the data boundary to force completion.
