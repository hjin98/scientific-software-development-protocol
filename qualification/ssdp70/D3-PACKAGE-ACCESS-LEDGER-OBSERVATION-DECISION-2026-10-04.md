# D3 decision: supervisor-owned package-access ledger for exact resource observation

Governing protocol: SSDP **6.6.0** (workplan `protocol_version` unchanged). Protocol 7.0 remains **NON-QUALIFIED**. This is a **cycle-scoped D3 clarification of the Stage F OMP slice, pending fresh independent D3 acceptance**. It is not an acceptance of its own bytes, admits no runner/profile/transform, and changes no contract threshold, floor or fixture.

Parents: consolidated workplan "Trusted runtime-observation contract" and "Root-selection evidence contract" (T1/T7/T8 "exact consumed SSDP resources/active material"; otherwise claim-scoped inadmissible); evaluation contract rev8 §1 items 4–5, §4 (active-byte metric), §6. Authorized by the stakeholder as the bounded D3 repair of the process/file-access observation gap.

## Gap (classified: D3, not D4)

Native `read` events and observer-captured tool-result text do not bound which package files an arbitrary subject process (`bash`, and native `grep`/`glob`) read. A real OMP model obtained the T7 owner via `bash cat`; the harness reported no owner read and root-only bytes yet `COMPLETE_ADMISSIBLE` (`OMP-STANDIN-20261004T171724Z-…/run`). The D4 guard that now makes such runs `INADMISSIBLE` (`OMP-STANDIN-20261004T172146Z-…/run`) prevents a false claim but cannot supply the exact observation the burden metric needs. The accepted graph does not say which principal observes subject-process package access, so a D4 choice would silently decide an architecture question.

## Decision

1. **Owner.** The *qualification supervisor principal* observes access to the installed protocol package. The package tree is already a supervisor-owned immutable input that the subject receives read-only (`/opt/ssdp/skills`). Observation is a supervisor evidence-capture duty ("run identity/evidence capture").
2. **Mechanism class (D4 may substitute an equivalent).** A kernel-maintained per-inode access record taken on the supervisor's own host-side package directories (Linux inotify marks on the installed tree: open, access, close, mutation, overflow, unmount). It records accesses by *any* process that reaches those inodes through any path or mount, with no cooperation from, or channel to, the subject.
3. **Topology.** No new principal, process, socket, proxy, credential carrier or cross-principal communication edge. The subject gains no capability; the supervisor receives information only from the kernel about its own files. The subject cannot read, write or influence the ledger; a failure to observe is itself recorded. Unchanged: provider-control observer scope, mediator ownership, MCP bridge, subject authority.
4. **Ledger = upper bound; supply = content.** The ledger bounds *which package regular files were opened*. A file counts as *consumed* only when model-visible tool-result text (hash-linked request bodies, via the existing observer chain) contains its content (existing `consumption` rule for native `read`; a contiguous-content rule for process output). An opened file whose content cannot be shown to have reached the model is **unexplained**. Unexplained access, ledger loss (overflow, lost mark, unmount, mutation, mark not established, missing artifact) or an observed-content/ledger contradiction makes resource observation **not exact**, and a not-exact observation makes T1/T7/T8 burden and owner-read claims `INADMISSIBLE` (never a lower-bound PASS). Files never opened are *exactly* not consumed.
5. **Phase split by request 0.** Opens before the hash-linked request-0 record are runtime-initiated (the model cannot act before it has a response). They are explained only when they are `<root>/SKILL.md` entries (catalog/activation); any other pre-request open is unexplained. Model-driven reads cannot precede the response, so opens at or after request 0 must be explained by supply. Clock skew can only move an event into the stricter class.
6. **Counting.** Active SSDP bytes remain the contract metric: the root `SKILL.md` delivered/read plus each package file whose content reached the model, each counted once at full installed size. Owner-read sequences derive from the events that supplied the owner file. Native `read` behavior is unchanged.
7. **Adapter scope.** The ledger is an adapter-produced supervisor artifact bound into the evidence-integrity chain. An adapter that produces no ledger keeps the previous behavior: process execution makes burden/owner claims `INADMISSIBLE`.

## Considered and rejected

- Remove `bash`/native process tools: contradicts the preserved 6.6 allow classes for T1/T7/T8.
- Observation via a FUSE or proxy filesystem serving the package: a new service and cross-principal edge; reopens D3.
- Content-matching alone: cannot prove absence of reads (a model can transform output); retained only as supply evidence.
- Conservative claim-scoped inadmissibility only: remains the fail-closed fallback, but forfeits a feasible exact observation inside the accepted graph.

## Residuals and non-claims

- Execution of arbitrary subject processes remains unauditable by pid; attribution is by content supply, not process identity.
- A read whose output is transformed (hash, base64, count) is *unexplained*, so the run is conservatively inadmissible for burden claims; this is intended, not a defect.
- Whether other adapters/runtimes can realize an equivalent observation is unresolved; no claim is made for them. Package root layout `/opt/ssdp/skills/<root>/...` is assumed only for this OMP profile.
- The mechanism depends on host kernel inotify semantics; exactness is claimed only for ledgers that report established, complete, non-overflowed marks.

## Reopen triggers

Reopen D3 if realization needs any new principal/channel/edge, if the subject gains the ability to influence or suppress marks, or if the contract metric changes from consumed-bytes to something the ledger plus supply cannot decide.

## D4 acceptance boundary

Real OMP → trusted observer → harness/core → scorer path: (a) `bash cat` owner yields exact bytes and an owner-read sequence; (b) accesses whose content cannot be shown supplied (count/hash/grep/transform/`wc -c`) yield `INADMISSIBLE` for burden claims with the file named; (c) non-read mutation, ledger overflow, missing ledger and ledger/native contradiction are rejected; (d) pre-request opens other than `SKILL.md` are rejected; (e) previous guard behavior for ledger-less adapters is preserved; (f) retained failed and earlier realizations stay append-only.

## D4 realization facts observed (development evidence, not admission)

Exact OMP 18.0.11 (`6054460b…cd26`) through the real observer/harness/scorer with the local provider stand-in only:

- Before request 0 the runtime opens exactly the seven roots' `SKILL.md` files (catalog scan) and nothing else in the package; the pre-request rule therefore needs no exception beyond `<root>/SKILL.md`. This is an observation of this build, not a contract constant; any other pre-request open is classified unexplained.
- Original counterexample re-realized (`bash cat` of the T7 owner): `COMPLETE_ADMISSIBLE`, resource observation exact, active bytes 14 454 (root) + 45 958 (owner) = 60 412, owner-read sequence recorded. The earlier false state (root-only 14 454, no owner read) is retired by observation, not by guard.
- Content that cannot be shown supplied (`wc -l`, `base64 | head`, native `grep` over the package) yields `INADMISSIBLE` for burden/owner claims, names the opened files, and leaves `active_ssdp_bytes`/`owner_read_sequences` null.
- The kernel mechanism distinguishes `open`+`access` (read) from `open` only (`wc -c`); the accounting treats both as access that must be explained.
- `package_ledger.py` is supervisor code bound into the execution-profile identity with the adapter, core and harness digests.

Retained: the guard-only realizations (`…T171724Z…`, `…T172146Z…`) remain append-only evidence of the defect and its interim guard.
