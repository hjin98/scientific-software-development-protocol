set -x
# Candidate v66f: dist/skills at 22f4bdba53795da3a6f13f162529f3a843fc37ae; basis v66b: 47dc85d; baseline v65: 2b8ce17 (6.5.0).
# Rule and routing map frozen at 9b65f8d (scenarios.yaml final, routing-preservation-map.yaml) before the candidate existed.
V65="--variant v65=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/bfa3776f-3d60-46bc-8519-f7598ac655d4/scratchpad/variants/v65/dist/skills"
V66B="--variant v66b=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/bfa3776f-3d60-46bc-8519-f7598ac655d4/scratchpad/variants/v66b/dist/skills"
V66F="--variant v66f=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/bfa3776f-3d60-46bc-8519-f7598ac655d4/scratchpad/variants/v66f/dist/skills"
M="python3 run_matrix.py --parallel 4"
$M --layer route --out results/final/routes --reps 2 $V66B $V66F
$M --layer selection --out results/final/selection --reps 2 $V66B $V66F
$M --layer trajectory --out results/final/trajectory --reps 3 $V65 $V66F --only T1-first-clean-local-repair --only T7-unversioned-workplan-implementation --only T8-ordinary-feature-with-docs
$M --layer trajectory --out results/final/trajectory --reps 4 $V66B $V66F --only T6-version-bound-stage-continuation-holdout
$M --layer trajectory --out results/final/trajectory --reps 2 $V66B $V66F --only T5-version-bound-workplan-holdout --only T4-version-bound-workplan
$M --layer trajectory --out results/final/trajectory --reps 2 $V66F --only T2-tolerance-within-envelope --only T3-d2-owned-default
