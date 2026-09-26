set -x
M="python3 run_matrix.py --layer trajectory --variant v65=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/7af2808c-6809-44ab-a122-a702353fc44c/scratchpad/variants/v65/dist/skills --variant v66=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/7af2808c-6809-44ab-a122-a702353fc44c/scratchpad/variants/v66/dist/skills --out results/rework/live-r1r2 --parallel 4"
$M --reps 4 --only T6-version-bound-stage-continuation-holdout
$M --reps 3 --only T1-first-clean-local-repair --only T7-unversioned-workplan-implementation
$M --reps 2 --only T5-version-bound-workplan-holdout --only T4-version-bound-workplan --only T2-tolerance-within-envelope --only T3-d2-owned-default
