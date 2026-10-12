#!/usr/bin/env bash
# S4 launcher (analyst-authorized steps only). Usage: launch.sh WORK start|status
#   start  : runs every command in WORK/commands.json detached (own session), writing WORK/launch/<key>.{pid,started,log,exit}
#   status : NOT-LAUNCHED | RUNNING | EXIT <rc> | CRASHED per key, plus run directories completed so far
# Needs SSDP70_OMP_PROVIDER_CREDENTIAL in the environment (the DeepInfra key; it is only checked for presence, never printed).
set -u
WORK=${1:?work dir}; ACTION=${2:?start|status}
mkdir -p "$WORK/launch"
keys() { python3 -c "import json,sys;print(' '.join(c['key'] for c in json.load(open(sys.argv[1]))['commands']))" "$WORK/commands.json"; }
shellof() { python3 -c "import json,sys;print(next(c['shell'] for c in json.load(open(sys.argv[1]))['commands'] if c['key']==sys.argv[2]))" "$WORK/commands.json" "$1"; }
state() {  # state <key>
  local k=$1 f="$WORK/launch/$1"
  if [ -f "$f.exit" ]; then echo "EXIT $(cat "$f.exit")"
  elif [ -f "$f.pid" ] && kill -0 "$(cat "$f.pid")" 2>/dev/null; then echo RUNNING
  elif [ -f "$f.started" ]; then echo CRASHED
  else echo NOT-LAUNCHED; fi
}
case "$ACTION" in
  start)
    [ -n "${SSDP70_OMP_PROVIDER_CREDENTIAL:-}" ] || { echo "SSDP70_OMP_PROVIDER_CREDENTIAL is not set" >&2; exit 2; }
    for k in $(keys); do
      [ "$(state "$k")" = NOT-LAUNCHED ] || { echo "$k already launched: $(state "$k")" >&2; exit 2; }
    done
    for k in $(keys); do
      date -u +%FT%TZ > "$WORK/launch/$k.started"
      setsid nohup bash -c "$(shellof "$k"); echo \$? > '$WORK/launch/$k.exit'" > "$WORK/launch/$k.log" 2>&1 < /dev/null &
      echo $! > "$WORK/launch/$k.pid"
      echo "started $k (pid $!)"
    done;;
  status)
    for k in $(keys); do
      echo "$k: $(state "$k")  runs started: $(ls -d "$WORK/runs/$k"/*-r0 2>/dev/null | wc -l)  summaries: $(ls "$WORK/runs/$k"/*-r0/summary.json 2>/dev/null | wc -l)  errors: $(ls "$WORK/runs/$k"/*.error.txt 2>/dev/null | wc -l)"
    done;;
esac
