"""The ``sdp`` command line -- Core owns the composition root and this entry point.

Two output rules are contractual:

* A prompt command writes **only** the prompt to stdout, and writes it only after
  the complete artifact exists. Any failure produces zero prompt bytes.
* Diagnostics go to stderr, redacted, with a nonzero exit status.

Every stage alias and ``sdp prompt <stage>`` share one prepare/render path; the
aliases are convenience spellings, not duplicated semantics.
"""

from __future__ import annotations

import json
import sys
from typing import Optional

import typer

from . import errors as E
from . import profile as P
from . import protocol_source as PS
from .application import create_application
from .canonical import CANONICAL_STAGES
from .records import (
    ActivationPolicy,
    ApplicationRequest,
    ObservationPolicy,
    ProjectKey,
    PromptExecutionMode,
    PromptPreparationRequest,
    PromptRenderRequest,
    RemoteMode,
    StageSelector,
    WorkplanQuery,
)
from .redaction import redact_text

EXIT_OK = 0
EXIT_INTERNAL = 1
EXIT_PROBLEM = 2

app = typer.Typer(
    name="sdp",
    help="Software Development Protocol orchestrator: render stage-correct Protocol prompts.",
    add_completion=False,
    no_args_is_help=True,
)

# Typer needs its command surface at import time, before any configuration or
# profile is loaded, so the alias *names* come from the frozen canonical stage
# list. This is not a second semantic authority: `build_profile` requires the
# profile's stage set to match this list exactly, and every command resolves its
# stage through the compatible profile at run time.
_STAGE_KEYS = tuple(key for _, key, _ in CANONICAL_STAGES)

# --- shared option declarations -------------------------------------------

_project_opt = typer.Option(None, "--project", help="configured project key")
_workplan_opt = typer.Option(
    None, "--workplan", help="exact workplan_id or exact repository-relative path"
)
_mode_opt = typer.Option(
    None, "--prompt-mode", help="where the prompt will be consumed: local or web"
)
_config_opt = typer.Option(None, "--config", help="explicit configuration file path")
_remote_opt = typer.Option(
    None, "--remote-mode", help="local_only, use_cached_remote (default), or refresh_remote"
)
_task_opt = typer.Option(None, "--task", help="Design-stage task description")
_input_opt = typer.Option(
    None, "--input", help="declared profile INPUT as NAME=VALUE (repeatable)"
)
_copy_opt = typer.Option(False, "--copy", help="additionally copy the prompt to the clipboard")


def _parse_inputs(values: Optional[list[str]]) -> tuple[tuple[str, str], ...]:
    pairs: list[tuple[str, str]] = []
    for item in values or []:
        if "=" not in item:
            E.fail(
                E.PROMPT_INPUT_INVALID,
                "--input expects NAME=VALUE",
                details={"argument": item[:120]},
            )
        name, value = item.split("=", 1)
        pairs.append((name.strip(), value))
    return tuple(pairs)


def _prompt_mode(explicit: str) -> PromptExecutionMode:
    """explicit -> project default -> core default -> built-in web.

    Core never silently falls back from web to local: an infeasible web target is
    reported, not quietly downgraded.
    """

    try:
        return PromptExecutionMode(explicit)
    except ValueError:
        E.fail(
            E.PROMPT_MODE_INVALID,
            "--prompt-mode must be 'local' or 'web'",
            details={"supplied": explicit},
        )


def _remote_mode(explicit: str | None) -> RemoteMode:
    if explicit is None:
        # CLI default: read existing local remote-tracking evidence. No network,
        # no mutation, and enough to tell whether a web target actually exists.
        return RemoteMode.USE_CACHED_REMOTE
    try:
        return RemoteMode(explicit)
    except ValueError:
        E.fail(
            E.CONFIG_INVALID,
            "--remote-mode must be local_only, use_cached_remote, or refresh_remote",
            details={"supplied": explicit},
        )


def _emit_problem(problem: E.Problem) -> None:
    typer.echo(json.dumps(problem.to_dict(), indent=2, sort_keys=True), err=True)


def _copy_to_clipboard(text: str) -> None:
    try:
        import pyperclip  # noqa: PLC0415 - optional extra
    except ImportError:
        typer.echo(
            json.dumps(
                E.Problem(
                    E.CLIPBOARD_UNAVAILABLE,
                    "clipboard support is not installed",
                    remediation="install sdp-orchestrator-core[clipboard]",
                ).to_dict(),
                indent=2,
                sort_keys=True,
            ),
            err=True,
        )
        return
    try:
        pyperclip.copy(text)
    except Exception as exc:  # noqa: BLE001 - clipboard is strictly additive
        typer.echo(
            json.dumps(
                E.Problem(
                    E.CLIPBOARD_UNAVAILABLE,
                    f"clipboard copy failed: {type(exc).__name__}",
                ).to_dict(),
                indent=2,
                sort_keys=True,
            ),
            err=True,
        )


def _render_stage(
    stage: str,
    *,
    project: str | None,
    workplan: str | None,
    prompt_mode: str | None,
    config: str | None,
    remote_mode: str | None,
    task: str | None,
    inputs: Optional[list[str]],
    copy: bool,
) -> None:
    """The single prepare/render path shared by every stage command."""

    application = create_application(
        ApplicationRequest(config_path=config, activation_policy=ActivationPolicy.NORMAL)
    )
    core = application.core()
    project_key = core.resolve_project_key(project)
    section = application.config().project(str(project_key))

    if prompt_mode:
        mode = _prompt_mode(prompt_mode)
    elif section.default_prompt_mode is not None:
        mode = section.default_prompt_mode
    elif application.config().core.default_prompt_mode is not None:
        mode = application.config().core.default_prompt_mode
    else:
        mode = PromptExecutionMode.WEB

    prepared = core.prepare(
        PromptPreparationRequest(
            project=ProjectKey(str(project_key)),
            stage=StageSelector(stage),
            workplan_selector=workplan,
            first_task=task,
            input_overrides=_parse_inputs(inputs),
            policy=ObservationPolicy(remote_mode=_remote_mode(remote_mode)),
        )
    )
    rendered = core.render(
        PromptRenderRequest(prepared=prepared, prompt_execution_mode=mode)
    )

    # The artifact is complete before a single byte reaches stdout.
    sys.stdout.write(rendered.prompt_text)
    sys.stdout.flush()
    if copy:
        _copy_to_clipboard(rendered.prompt_text)
    for failure in application.events().failures:
        typer.echo(f"event sink failure (primary render unaffected): {failure}", err=True)


def _register_stage_command(stage_key: str) -> None:
    @app.command(stage_key, help=f"Render the {stage_key} stage prompt.")
    def _command(  # noqa: D401 - Typer command
        project: Optional[str] = _project_opt,
        workplan: Optional[str] = _workplan_opt,
        prompt_mode: Optional[str] = _mode_opt,
        config: Optional[str] = _config_opt,
        remote_mode: Optional[str] = _remote_opt,
        task: Optional[str] = _task_opt,
        inputs: Optional[list[str]] = _input_opt,
        copy: bool = _copy_opt,
    ) -> None:
        _render_stage(
            stage_key,
            project=project,
            workplan=workplan,
            prompt_mode=prompt_mode,
            config=config,
            remote_mode=remote_mode,
            task=task,
            inputs=inputs,
            copy=copy,
        )

    _command.__name__ = f"stage_{stage_key.replace('-', '_')}"


for _key in _STAGE_KEYS:
    _register_stage_command(_key)


@app.command("prompt", help="Render any stage prompt by profile stage key or alias.")
def prompt_command(
    stage: str = typer.Argument(..., help="stage key or profile alias"),
    project: Optional[str] = _project_opt,
    workplan: Optional[str] = _workplan_opt,
    prompt_mode: Optional[str] = _mode_opt,
    config: Optional[str] = _config_opt,
    remote_mode: Optional[str] = _remote_opt,
    task: Optional[str] = _task_opt,
    inputs: Optional[list[str]] = _input_opt,
    copy: bool = _copy_opt,
) -> None:
    _render_stage(
        stage,
        project=project,
        workplan=workplan,
        prompt_mode=prompt_mode,
        config=config,
        remote_mode=remote_mode,
        task=task,
        inputs=inputs,
        copy=copy,
    )


@app.command("projects", help="List configured projects and their observable workplans.")
def projects_command(
    config: Optional[str] = _config_opt,
    workplans: bool = typer.Option(False, "--workplans", help="include the workplan catalog"),
) -> None:
    application = create_application(ApplicationRequest(config_path=config))
    core = application.core()
    payload = []
    for descriptor in core.projects().items:
        entry = descriptor.model_dump(mode="json")
        if workplans:
            try:
                page = core.workplans(WorkplanQuery(project=descriptor.project_key))
                entry["workplans"] = [item.model_dump(mode="json") for item in page.items]
            except E.OrchestratorError as exc:
                entry["workplans_problem"] = exc.problem.to_dict()
        payload.append(entry)
    typer.echo(json.dumps(payload, indent=2, sort_keys=True))


@app.command("capabilities", help="Report capability status (metadata-only discovery by default).")
def capabilities_command(
    config: Optional[str] = _config_opt,
    load_extensions: bool = typer.Option(
        False,
        "--load-extensions",
        help="import and activate installed providers instead of reading metadata only",
    ),
) -> None:
    policy = ActivationPolicy.NORMAL if load_extensions else ActivationPolicy.DISCOVERY_ONLY
    application = create_application(
        ApplicationRequest(config_path=config, activation_policy=policy)
    )
    typer.echo(
        json.dumps(
            {
                "activation_policy": policy.value,
                "capabilities": [
                    status.model_dump(mode="json") for status in application.capabilities()
                ],
                "extensions": [
                    status.model_dump(mode="json") for status in application.extensions()
                ],
            },
            indent=2,
            sort_keys=True,
        )
    )


@app.command("doctor", help="Report Core readiness without hidden loading, network, or mutation.")
def doctor_command(config: Optional[str] = _config_opt) -> None:
    application = create_application(
        ApplicationRequest(config_path=config, activation_policy=ActivationPolicy.DISCOVERY_ONLY)
    )
    core_config = application.config()
    report: dict[str, object] = {
        "activation_policy": ActivationPolicy.DISCOVERY_ONLY.value,
        "config_path": str(core_config.path) if core_config.path else None,
        "configuration_identity": core_config.identity.model_dump(mode="json"),
        "projects": sorted(core_config.projects),
        "protocol_sources": sorted(core_config.protocol_sources),
        "inactive_extension_config_namespaces": sorted(core_config.extension_namespaces),
        "core_capabilities": [
            status.model_dump(mode="json") for status in application.capabilities()
        ],
        "discovered_extensions": [
            status.model_dump(mode="json") for status in application.extensions()
        ],
        "notes": [
            "extension providers were not imported; their capabilities and health are unobserved",
            "no repository was mutated and no network request was made by this command",
        ],
    }
    try:
        descriptor = PS.resolve_packaged(P.PROFILE_ID).snapshot.descriptor
        report["packaged_profile"] = {
            "profile_id": descriptor.profile.profile_id,
            "protocol_version": descriptor.profile.protocol_version,
            "stages": [stage.stage.stage_key for stage in descriptor.stages],
            "result_schema": f"{descriptor.result_schema_id} v{descriptor.result_schema_version}",
        }
    except E.OrchestratorError as exc:
        report["packaged_profile_problem"] = exc.problem.to_dict()
    typer.echo(json.dumps(report, indent=2, sort_keys=True))


def main() -> int:
    """Console entry point.

    Usage errors are rendered by Typer itself. Structured Core problems are
    emitted as redacted JSON on stderr with exit status 2; an unexpected failure
    exits 1 without printing a traceback as the product surface.
    """

    try:
        app()
    except E.OrchestratorError as exc:
        _emit_problem(exc.problem)
        return EXIT_PROBLEM
    except SystemExit as exc:
        return int(exc.code or 0)
    except Exception as exc:  # noqa: BLE001 - never leak a traceback as the product surface
        typer.echo(
            f"internal error: {type(exc).__name__}: {redact_text(str(exc))}", err=True
        )
        return EXIT_INTERNAL
    return EXIT_OK


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
