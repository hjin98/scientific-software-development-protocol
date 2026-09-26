set -x
# Candidate: dist/skills at 47dc85de6dd6be8b0adfb1a66024cfdd5397f3d8; baseline: dist/skills at 2b8ce17 (6.5.0).
# Rule frozen at 6c76ef1 (scenarios.yaml redesign) before this launch.
M="python3 run_matrix.py --layer trajectory --out results/redesign/live --parallel 4"
V65="--variant v65=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/6815631b-522b-4cf4-916e-bb28923b20d8/scratchpad/variants/v65/dist/skills"
V66="--variant v66=/tmp/claude-1000/-home-samjin-agent-skills-scientific-software-development-protocol/6815631b-522b-4cf4-916e-bb28923b20d8/scratchpad/variants/v66/dist/skills"
$M $V65 $V66 --reps 3 --only T1-first-clean-local-repair --only T7-unversioned-workplan-implementation --only T8-ordinary-feature-with-docs
$M $V66 --reps 4 --only T6-version-bound-stage-continuation-holdout
$M $V66 --reps 2 --only T5-version-bound-workplan-holdout --only T4-version-bound-workplan --only T2-tolerance-within-envelope --only T3-d2-owned-default
