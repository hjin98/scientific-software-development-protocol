# Operator helpers for the Protocol 7.1 requalification runbook. Source AFTER campaign-parameters.env.
# Analyst-owned and pinned in tool-pins.sha256. The operator never edits this file.

need() {  # need VAR... : refuse unless every parameter is decided
  local v val
  for v in "$@"; do
    val="${!v-}"
    if [ -z "$val" ] || [ "${val#UNDECIDED}" != "$val" ]; then
      echo "STOP: parameter $v is not decided (analyst/stakeholder must set it)"; return 1
    fi
  done
}

gate() {  # gate <step-id> <command...> : run once, keep the JSON verdict, return the command's exit code
  local id="$1"; shift
  mkdir -p "$WORK/gates"
  if [ -e "$WORK/gates/$id.exit" ]; then
    echo "STOP: step $id already ran (exit $(cat "$WORK/gates/$id.exit")); steps are never repeated"; return 1
  fi
  "$@" > "$WORK/gates/$id.json" 2> "$WORK/gates/$id.stderr"
  local rc=$?
  echo "$rc" > "$WORK/gates/$id.exit"
  echo "step $id exit $rc  (verdict: $WORK/gates/$id.json)"
  return $rc
}

launch() {  # launch <commands.json> <key> : start one printed harness command in the background, exactly as printed
  local plan="$1" key="$2"
  mkdir -p "$WORK/launch"
  if [ -e "$WORK/launch/$key.started" ]; then echo "STOP: $key was already launched; never relaunch"; return 1; fi
  date -u +%FT%TZ > "$WORK/launch/$key.started"
  nohup "$PY" - "$plan" "$key" "$WORK/launch/$key.exit" > "$WORK/launch/$key.log" 2>&1 <<'PYEOF' &
import json, subprocess, sys
plan, key, exit_path = sys.argv[1:4]
cmds = [c for c in json.load(open(plan))["commands"] if c["key"] == key]
if len(cmds) != 1:
    open(exit_path, "w").write("97\n"); sys.exit(97)
rc = subprocess.call(cmds[0]["argv"])
open(exit_path, "w").write(f"{rc}\n")
PYEOF
  echo "launched $key; poll with: launch_status $key"
}

launch_status() {  # launch_status <key> : RUNNING, or the exit code once finished
  if [ ! -e "$WORK/launch/$1.started" ]; then echo "NOT-LAUNCHED"; elif [ -e "$WORK/launch/$1.exit" ]; then echo "EXIT $(cat "$WORK/launch/$1.exit")"; else echo "RUNNING"; fi
}

log_access() {  # log_access <role> <paths> <reason> : append one line to the custody access log (append-only)
  printf -- '- %s role=%s paths=%s reason: %s (recorded by operator)\n' "$(date -u +%FT%TZ)" "$1" "$2" "$3" >> "$CUSTODY/ACCESS-LOG.md"
}

escalate() {  # escalate <step-id> <one-line description> : write the packet, then STOP working
  local id="$1"; shift
  mkdir -p "$WORK/escalations"
  local f="$WORK/escalations/$(date -u +%Y%m%dT%H%M%SZ)-$id.md"
  {
    echo "# Escalation: step $id"
    echo "- time: $(date -u +%FT%TZ)"
    echo "- operator note (facts only): $*"
    echo "- exit code: $(cat "$WORK/gates/$id.exit" 2>/dev/null || cat "$WORK/launch/$id.exit" 2>/dev/null || echo n/a)"
    echo; echo '## Verdict JSON (verbatim)'; echo '```json'; cat "$WORK/gates/$id.json" 2>/dev/null; echo '```'
    echo; echo '## stderr / log tail'; echo '```'; tail -n 60 "$WORK/gates/$id.stderr" "$WORK/launch/$id.log" 2>/dev/null; echo '```'
    echo; echo "The operator has stopped and will not continue until the analyst replies."
  } > "$f"
  echo "ESCALATED: $f -- now STOP."
}

freeze_check() {  # freeze_check : verify the custody store against its own frozen digests (prints a verdict JSON)
  if ( cd "$CUSTODY" && sha256sum -c --quiet FREEZE.sha256 >/dev/null 2>&1 \
       && [ "$(sha256sum FREEZE.sha256 | cut -d' ' -f1)" = "$(cut -d' ' -f1 FREEZE.sha256.digest)" ] ); then
    echo '{"command": "freeze-check", "verdict": "PASS"}'
  else
    echo '{"command": "freeze-check", "verdict": "STOP"}'; return 1
  fi
}
