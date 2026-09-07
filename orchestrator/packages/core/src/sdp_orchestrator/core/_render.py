"""Final prompt-artifact assembly: mode-safe context, substitution, footer, fingerprint.

Three properties are load-bearing here.

**Canonical body is preserved.** Only declared ``NAME = ...`` INPUT lines are
rewritten. Core never edits, weakens, summarizes, or reinterprets stage
instructions, and never asks for hidden reasoning.

**Web context is truthful.** Web mode renders a remote target only when the
target's *existence* is actually known -- from a cached remote-tracking ref or an
explicit bounded query -- and refuses when local state (dirty worktree, known
divergence, detached HEAD) cannot be represented remotely. Freshness may be
unknown and is labelled; existence may not be guessed.

**Nothing local leaks.** Web mode derives its target from the sanitized remote
only. Local paths, remotes, and configuration never enter a web artifact
automatically.
"""

from __future__ import annotations

from . import _errors as E
from ._digest import SCHEME_PROMPT_FINGERPRINT, digest_bytes
from ._records import (
    CandidateRef,
    DigestRef,
    PromptExecutionMode,
    PromptProjectSnapshot,
    ProjectObservation,
    RemoteEvidence,
    RemoteMode,
    ResolvedInput,
    StageRef,
)
from ._inputs import encode_scalar

#: Frozen v1 fingerprint placeholder: same length as the substituted digest so
#: byte offsets in the placeholder form match the final artifact.
FINGERPRINT_PLACEHOLDER = "sha256:" + ("0" * 64)

#: Frozen v1 result-footer markers. Extraction rule: the LAST line equal to the
#: begin marker starts the footer; the next line equal to the end marker ends it.
FOOTER_BEGIN = "<<<SDP_STAGE_RESULT_V1"
FOOTER_END = "SDP_STAGE_RESULT_V1>>>"

_ORCHESTRATION_HEADING = "SDP ORCHESTRATION METADATA"


def _target_ref(upstream_ref: str | None, remote_name: str, branch: str | None) -> str | None:
    if upstream_ref:
        prefix = f"{remote_name}/"
        return upstream_ref[len(prefix) :] if upstream_ref.startswith(prefix) else upstream_ref
    return branch


def build_snapshot(
    observation: ProjectObservation, mode: PromptExecutionMode
) -> PromptProjectSnapshot:
    """Derive the prompt-mode-safe repository context, or refuse truthfully."""

    candidate = observation.candidate
    if mode is PromptExecutionMode.LOCAL:
        return _local_snapshot(observation, candidate)
    return _web_snapshot(observation, candidate)


def _local_snapshot(
    observation: ProjectObservation, candidate: CandidateRef
) -> PromptProjectSnapshot:
    root = observation.local_repo_root
    if not root:  # pragma: no cover - a local observation always has a root
        E.fail(E.REPOSITORY_INVALID, "the observation carries no local worktree root")
    position = "detached HEAD" if candidate.detached else f"branch {candidate.branch}"
    state = (
        "working tree has uncommitted changes"
        if candidate.working_tree_digest is not None
        else "working tree clean"
    )
    target = f"{root} ({position}, commit {candidate.head_commit}, {state})"
    notes = []
    if not candidate.identity_complete:
        notes.append("candidate identity is incomplete; some working-tree content could not be fingerprinted")
    return PromptProjectSnapshot(
        prompt_execution_mode=PromptExecutionMode.LOCAL,
        repository_target=target,
        candidate_commit=candidate.head_commit,
        target_ref=candidate.branch,
        remote_evidence=candidate.remote_evidence,
        notes=tuple(notes),
    )


def _web_snapshot(
    observation: ProjectObservation, candidate: CandidateRef
) -> PromptProjectSnapshot:
    remote = observation.selected_remote
    if remote is None:
        if observation.policy.remote_mode is RemoteMode.LOCAL_ONLY:
            # The remote may well exist; local-only observation simply did not look.
            # Saying "unavailable" here would assert more than was observed.
            E.fail(
                E.REMOTE_TARGET_UNAVAILABLE,
                "local-only observation gathered no remote evidence, so no web target is established",
                details={"remote_mode": observation.policy.remote_mode.value},
                remediation="observe with --remote-mode use_cached_remote or refresh_remote, or render with --prompt-mode local",
            )
        E.fail(
            E.REMOTE_UNAVAILABLE,
            "web prompt mode requires a selected Git remote and none was resolved",
            details={"diagnostics": list(observation.remote_diagnostics)},
            remediation="configure projects.<key>.remote_name, or render with --prompt-mode local",
        )
    if not remote.web_addressable:
        E.fail(
            E.REMOTE_LOCAL_ONLY,
            "the selected Git remote is not web-addressable",
            details={"remote": remote.remote_name, "scheme": remote.scheme},
            remediation="render with --prompt-mode local, or select a network remote",
        )
    if candidate.detached:
        E.fail(
            E.REMOTE_TARGET_UNAVAILABLE,
            "web prompt mode cannot address a detached HEAD without an explicit remote target",
            remediation="check out a branch with a known remote target, or render with --prompt-mode local",
        )
    if candidate.working_tree_digest is not None:
        E.fail(
            E.PROMPT_MODE_INVALID,
            "web prompt mode cannot truthfully represent uncommitted local changes",
            remediation="commit and publish the candidate, or render with --prompt-mode local",
        )
    if candidate.remote_evidence is RemoteEvidence.NONE:
        E.fail(
            E.REMOTE_TARGET_UNAVAILABLE,
            "no evidence establishes that the intended remote target exists",
            details={"remote_mode": observation.policy.remote_mode.value},
            remediation="observe with --remote-mode use_cached_remote or refresh_remote, or render with --prompt-mode local",
        )
    if candidate.observed_remote_commit is None:
        E.fail(
            E.REMOTE_TARGET_UNAVAILABLE,
            "the intended branch does not exist on the selected remote",
            details={"remote": remote.remote_name, "branch": candidate.branch},
            remediation="publish the branch, or render with --prompt-mode local",
        )
    if candidate.observed_remote_commit != candidate.head_commit:
        E.fail(
            E.REMOTE_STALE,
            "the local candidate and the observed remote target are known to diverge",
            details={
                "local_commit": candidate.head_commit,
                "remote_commit": candidate.observed_remote_commit,
                "evidence": candidate.remote_evidence.value,
            },
            remediation="publish the candidate commit, or render with --prompt-mode local",
        )

    target_ref = _target_ref(candidate.upstream_ref, remote.remote_name, candidate.branch)
    freshness = (
        "remote target confirmed by a bounded read-only remote query"
        if candidate.remote_evidence is RemoteEvidence.REFRESHED
        else "remote target confirmed by an existing local remote-tracking ref; freshness not re-queried"
    )
    target = (
        f"{remote.sanitized_repository} (branch {target_ref}, "
        f"commit {candidate.head_commit}, {freshness})"
    )
    return PromptProjectSnapshot(
        prompt_execution_mode=PromptExecutionMode.WEB,
        repository_target=target,
        candidate_commit=candidate.head_commit,
        target_ref=target_ref,
        remote_evidence=candidate.remote_evidence,
        notes=(freshness,),
    )


# --------------------------------------------------------------------------
# Artifact assembly
# --------------------------------------------------------------------------


def substitute_inputs(body: str, values: dict[str, str]) -> str:
    """Rewrite declared INPUT lines in the canonical body and nothing else."""

    lines = body.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    try:
        start = lines.index("INPUTS") + 1
    except ValueError:  # pragma: no cover - guarded during profile construction
        E.fail(E.PROTOCOL_SOURCE_INCOHERENT, "the canonical stage body has no INPUTS block")
    remaining = dict(values)
    for index in range(start, len(lines)):
        line = lines[index]
        if not line.strip():
            break
        name = line.split("=", 1)[0].strip()
        if name in remaining:
            lines[index] = f"{name} = {remaining.pop(name)}"
    if remaining:  # pragma: no cover - profile derives names from this same block
        E.fail(
            E.PROTOCOL_SOURCE_INCOHERENT,
            "the canonical stage body does not declare every classified input",
            details={"missing": sorted(remaining)},
        )
    return "\n".join(lines)


def _footer_request(
    run_id: str, stage: StageRef, result_schema_id: str, result_schema_version: int
) -> str:
    return "\n".join(
        (
            "---",
            "",
            _ORCHESTRATION_HEADING,
            "",
            f"RUN_ID = {encode_scalar(run_id)}",
            f"STAGE = {encode_scalar(stage.stage_key)}",
            f"PROTOCOL_PROFILE = {encode_scalar(stage.profile_id)}",
            f"PROTOCOL_VERSION = {encode_scalar(stage.protocol_version)}",
            f"RESULT_SCHEMA = {encode_scalar(result_schema_id)} v{result_schema_version}",
            f"PROMPT_FINGERPRINT = {FINGERPRINT_PLACEHOLDER}",
            "",
            "REQUIRED TERMINAL RESULT FOOTER",
            "",
            "Respond normally first. Your ordinary human-readable report for this stage is",
            "expected and is not replaced by the footer below. Do not reveal hidden reasoning;",
            "report only the conclusions, actions, and evidence you would normally state.",
            "",
            "Then end your response with exactly one machine-readable footer as its final",
            "content. The footer begins on its own line with the begin marker, contains one",
            "JSON object, and ends on its own line with the end marker:",
            "",
            FOOTER_BEGIN,
            "{",
            '  "schema_version": 1,',
            f'  "run_id": "{run_id}",',
            f'  "prompt_fingerprint": "{FINGERPRINT_PLACEHOLDER}",',
            f'  "stage": "{stage.stage_key}",',
            '  "outcome": "<one recognized outcome for this stage>",',
            '  "recommended_next_stage": "<stage key, or null>",',
            '  "blockers": [',
            '    { "blocker_id": null, "classification": null, "summary": "<what blocks closure>",',
            '      "authority_class": null }',
            "  ],",
            '  "completed_obligations": ["<obligation>"],',
            '  "pending_obligations": ["<obligation>"],',
            '  "checks_executed": ["<check>"],',
            '  "checks_unavailable": ["<check>"],',
            '  "candidate": "<branch/commit/worktree identity, or null>",',
            '  "summary": "<one-paragraph result summary>"',
            "}",
            FOOTER_END,
            "",
            "Rules for the footer: emit it exactly once, as the last content of your response;",
            "keep run_id, prompt_fingerprint, and stage byte-identical to the values above;",
            "use JSON null rather than omitting an unknown optional field; leave a list empty",
            "when it has no entries. Additional fields are permitted and are ignored by",
            "consumers that do not recognize them. Ordinary prose may precede the footer.",
            "",
        )
    )


def assemble(
    *,
    body: str,
    run_id: str,
    stage: StageRef,
    inputs: tuple[ResolvedInput, ...],
    snapshot: PromptProjectSnapshot,
    result_schema_id: str,
    result_schema_version: int,
) -> tuple[str, DigestRef]:
    """Build the complete artifact, then fingerprint it under ``sdp.prompt-fingerprint.v1``.

    The artifact is rendered once in placeholder form, hashed, and then the
    placeholder is replaced. Callers receive complete bytes or an exception --
    never a partial prompt.
    """

    values: dict[str, str] = {}
    for item in inputs:
        if item.mode_dependent:
            values[item.name] = encode_scalar(snapshot.repository_target)
        elif item.value is not None:
            values[item.name] = item.value
        else:  # pragma: no cover - resolve_inputs values every non-mode input
            E.fail(
                E.PROMPT_INPUT_REQUIRED,
                f"input {item.name} was not resolved before rendering",
                details={"input": item.name},
            )

    substituted = substitute_inputs(body, values)
    footer = _footer_request(run_id, stage, result_schema_id, result_schema_version)
    placeholder_form = substituted.rstrip("\n") + "\n\n" + footer
    placeholder_form = placeholder_form.rstrip("\n") + "\n"

    fingerprint = digest_bytes(
        placeholder_form.encode("utf-8"), SCHEME_PROMPT_FINGERPRINT
    )
    digest_text = f"sha256:{fingerprint.value}"
    return placeholder_form.replace(FINGERPRINT_PLACEHOLDER, digest_text), fingerprint


def extract_result_footer(response: str) -> str | None:
    """Reference implementation of the frozen terminal-footer extraction rule.

    Core does not consume agent output in WP-1; this exists so the contract Core
    *requests* is executable and can be frozen by fixtures for Tracker.
    """

    lines = response.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    begin = None
    for index in range(len(lines) - 1, -1, -1):
        if lines[index].strip() == FOOTER_BEGIN:
            begin = index
            break
    if begin is None:
        return None
    for index in range(begin + 1, len(lines)):
        if lines[index].strip() == FOOTER_END:
            return "\n".join(lines[begin + 1 : index])
    return None
