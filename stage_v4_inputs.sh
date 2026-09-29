#!/usr/bin/env bash
# Stages the safe live-probe evidence for the implementer. Deliberately omits N01 (contains custody canary strings) and N04 (contains ~/.gitconfig).
set -uo pipefail
cd /home/samjin/agent-skills/scientific-software-development-protocol
D=qualification/ssdp70/stage-f-runner-admission-v4-inputs-2026-09-29
W=$HOME/ssdp70-checker-run
mkdir -p "$D"
for r in run-ping/CHK-PING-p70-r0 run-turn/CHK-TURN-p70-r0 \
  narrow/N02-cat-custody-file-Bash/N02-cat-custody-file-Bash-p70-r0 \
  narrow/N05-list-host-home/N05-list-host-home-p70-r0 \
  narrow/N06-write-tmp-python/N06-write-tmp-python-p70-r0 \
  narrow/N07-write-tmp-Write-tool/N07-write-tmp-Write-tool-p70-r0 \
  narrow/N08-write-outside-project-relative/N08-write-outside-project-relative-p70-r0 \
  narrow/N20-ordinary-control-ls/N20-ordinary-control-ls-p70-r0 \
  narrow/N21-grep-no-path/N21-grep-no-path-p70-r0 \
  narrow/N22-glob-no-path/N22-glob-no-path-p70-r0 \
  narrow/N18-mcp-issue-create/N18-mcp-issue-create-p70-r0 \
  narrow/N19-mcp-delegate/N19-mcp-delegate-p70-r0; do
  n=$(basename "$r"); mkdir -p "$D/$n"
  for f in trace.jsonl summary.json normalization-map.json events.normalized.jsonl containment-realization.json; do
    cp "$W/$r/$f" "$D/$n/" 2>/dev/null || echo "missing $r/$f"
  done
  ls "$W/$r/final-tree" > "$D/$n/final-tree-listing.txt"
done
echo "staged $(ls "$D" | wc -l) directories in $D (expect 12)"
ls "$D"
if grep -rlq "CANARY-" "$D" 2>/dev/null; then echo "WARNING: canary strings present in staged files - do not hand over"; else echo "canary check: none found"; fi
if grep -rlq "hjin98\|noreply.github.com" "$D" 2>/dev/null; then echo "WARNING: personal git identity present in staged files"; else echo "identity check: none found"; fi
rm -f /tmp/qualification_probe_a.txt /tmp/qualification_probe_b.txt && echo "removed /tmp probe residue"
