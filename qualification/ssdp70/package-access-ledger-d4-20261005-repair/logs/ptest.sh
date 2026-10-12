#!/bin/bash
# usage: ptest.sh <module> <jobs> <outdir>
# One process per test id, at most <jobs> at a time, each with its own short scratch HOME
# (own run directories; the immutable runtime closures are exposed through a symlink).
module=$1; jobs=$2; out=$3
mkdir -p "$out"; : > "$out/results.txt"
cd /home/samjin/agent-skills/scientific-software-development-protocol/qualification/ssdp70/eval || exit 2
export PYTHONDONTWRITEBYTECODE=1 SSDP70_OMP_EXE=$HOME/.local/bin/omp REAL_HOME=$HOME OUT="$out"
python3 - "$module" > "$out/ids.txt" <<'PY'
import sys, unittest
def walk(s):
    for t in s:
        if isinstance(t, unittest.TestSuite):
            yield from walk(t)
        else:
            yield t.id()
for i in walk(unittest.defaultTestLoader.loadTestsFromName(sys.argv[1])):
    print(i)
PY
xargs -a "$out/ids.txt" -P "$jobs" -I{} bash -c '
  id="$1"; h=$(mktemp -d /tmp/s70p.XXXXXX); mkdir -p $h/ssdp70-omp-stagef
  ln -sfn $REAL_HOME/ssdp70-omp-stagef/runtime-closures $h/ssdp70-omp-stagef/runtime-closures
  HOME=$h python3 -m unittest "$id" > "$OUT/$id.log" 2>&1; echo "$? $id" >> "$OUT/results.txt"; rm -rf $h' _ {}
echo "DONE tests=$(grep -c . "$out/ids.txt") nonzero=$(grep -vc '^0 ' "$out/results.txt")" >> "$out/results.txt"
