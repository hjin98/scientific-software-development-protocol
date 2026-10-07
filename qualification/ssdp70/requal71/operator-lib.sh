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

_launcher() {  # _launcher <commands.json> <key> <detach 0|1> : run one printed command; the launcher records its own PID and exit
  # Detached mode forks and calls setsid() inside Python so the run leaves the caller's process group and session;
  # the shell's $! is never used because a forking setsid/nohup makes it name an already-exited parent.
  "$PY" - "$1" "$2" "$WORK/launch/$2" "$3" > "$WORK/launch/$2.log" 2>&1 <<'PYEOF'
import json, os, subprocess, sys, traceback
plan, key, base, detach = sys.argv[1:5]
if detach == "1":
    if os.fork():
        os._exit(0)
    os.setsid()
with open(base + ".pid", "w") as f:
    f.write(f"{os.getpid()}\n")
try:
    cmds = [c for c in json.load(open(plan))["commands"] if c["key"] == key]
    rc = subprocess.call(cmds[0]["argv"]) if len(cmds) == 1 else 97
except Exception:
    traceback.print_exc(); rc = 98
with open(base + ".exit", "w") as f:
    f.write(f"{rc}\n")
PYEOF
}

_launch_begin() {  # _launch_begin <key> : refuse a relaunch, then mark the start
  mkdir -p "$WORK/launch"
  if [ -e "$WORK/launch/$1.started" ]; then echo "STOP: $1 was already launched; never relaunch"; return 1; fi
  date -u +%FT%TZ > "$WORK/launch/$1.started"
}

launch() {  # launch <commands.json> <key> : start one printed harness command, detached, exactly as printed
  local plan="$1" key="$2" i
  _launch_begin "$key" || return 1
  _launcher "$plan" "$key" 1
  for i in $(seq 50); do [ -s "$WORK/launch/$key.pid" ] && break; sleep 0.2; done
  if [ "$(launch_status "$key")" = RUNNING ] || [ -e "$WORK/launch/$key.exit" ]; then
    echo "launched $key (PID $(cat "$WORK/launch/$key.pid")); poll with: launch_status $key"
  else
    echo "STOP: $key launcher is not alive ($(launch_status "$key"))"; return 1
  fi
}

launch_fg() {  # launch_fg <commands.json> <key> : same, in the foreground; ONLY when the analyst's work order says so
  _launch_begin "$2" || return 1
  _launcher "$1" "$2" 0
  echo "$2: $(launch_status "$2")"
}

launch_status() {  # launch_status <key> : NOT-LAUNCHED, RUNNING, EXIT <rc>, or CRASHED (started, no exit, launcher gone)
  local b="$WORK/launch/$1" pid
  if [ ! -e "$b.started" ]; then echo "NOT-LAUNCHED"; return; fi
  if [ -e "$b.exit" ]; then echo "EXIT $(cat "$b.exit")"; return; fi
  pid=$(cat "$b.pid" 2>/dev/null)
  # The launcher's command line carries $b, so a recycled PID is not mistaken for it.
  if [ -n "$pid" ] && tr '\0' ' ' 2>/dev/null < "/proc/$pid/cmdline" | grep -qF -- " $b "; then echo "RUNNING"; else echo "CRASHED"; fi
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
    [ -e "$WORK/launch/$id.started" ] && echo "- launch status: $(launch_status "$id")"
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
