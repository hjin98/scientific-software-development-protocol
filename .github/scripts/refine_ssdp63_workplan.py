from pathlib import Path
p = Path("workplans/active/PROTOCOL-6.3-EVIDENCE-BACKED-PROJECT-ENGINEERING-MEMORY-WORKPLAN.md")
s = p.read_text(encoding="utf-8")
repls = [
    ("reopened_stages: D,E,F", "reopened_stages: B,C,D,E,F"),
    ("The architectural design remains implementation-authorized; Stages D, E, and F are reopened because the candidate's D4 Project Engineering Memory (PEM) validation/representation and Stage-F qualification can accept invalid states.", "The architectural design remains implementation-authorized; the affected portions of Stages B and C, and Stages D, E, and F are reopened because the candidate's PEM schema/workflow concretization, D4 validation/representation, and Stage-F qualification can accept invalid states."),
    ("- Introduce the minimum non-self-referential publication-coherence metadata needed to prove that root and declared canonical partitions belong to the same semantic update, for example a root-issued logical publication token carried by every partition and replaced for each semantic publication spanning the unit. The token is representation metadata, not semantic authority and not a Git self-SHA.", "- Introduce the minimum non-self-referential publication-coherence metadata needed to prove the exact canonical partition content expected by the root. Prefer root-declared immutable content identities/digests for each detail file, or an equivalently discriminating owner-layer mechanism, so a changed partition plus root can publish coherently without forcing unrelated unchanged partitions to churn. The binding metadata is representation metadata, not semantic authority and not a Git self-SHA."),
    ("Implementation remains authorized on the dedicated 6.3 branch only for the current repair contract: Stages D, E, and F are reopened, the reviewed candidate `8d0ad2395ccd126c133d8aad206cfc859f660124` is NO-PASS, and Stage G is blocked.", "Implementation remains authorized on the dedicated 6.3 branch only for the current repair contract: the affected portions of Stages B and C, and Stages D, E, and F are reopened; the reviewed candidate `8d0ad2395ccd126c133d8aad206cfc859f660124` is NO-PASS; and Stage G is blocked."),
]
for old, new in repls:
    if old not in s:
        raise SystemExit("missing refinement marker: " + old[:80])
    s = s.replace(old, new, 1)
p.write_text(s, encoding="utf-8")
