from pathlib import Path
import re


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one occurrence, found {count}: {old!r}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')


def regex_replace_once(path: str, pattern: str, replacement: str) -> None:
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    new, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f'{path}: expected exactly one regex match: {pattern!r}')
    p.write_text(new, encoding='utf-8')


workplan = 'workplans/active/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md'
replace_once(workplan, 'independent_review_state: no-pass-reopened', 'independent_review_state: repaired-awaiting-fresh-review')
replace_once(workplan, 'implementation_handoff: repair-required', 'implementation_handoff: repair-complete-awaiting-fresh-review')
replace_once(workplan, 'active_serious_challenge: SC64-R1-USES-DEFINITION-DIRECTION', 'active_serious_challenge: none')
replace_once(
    workplan,
    '**STAGE-E INDEPENDENT ASSEMBLED-CANDIDATE REVIEW: NO-PASS.** Fresh independent Review of immutable assembled target `0377e798fbbb1054badd1193950d9c10f723be75` against accepted Protocol 6.3 repository state `0928accd337a13f864b292ed81c36372828cfb4c` found one active Serious Challenge and two additional blocking findings. Protocol 6.3 remains accepted-current. Protocol 6.4 recovery remains unavailable and Stage F remains blocked. The sixth design-review disposition below records the pre-implementation design acceptance that authorized the original implementation; it does not override this Stage-E result. Section 27 is the current repair/re-entry contract.',
    '**STAGE-E REPAIR COMPLETE; FRESH INDEPENDENT RE-REVIEW REQUIRED.** The NO-PASS on immutable assembled target `0377e798fbbb1054badd1193950d9c10f723be75` remains historical Review evidence, while its three owning-layer repairs are now integrated under Section 27. The `USES_DEFINITION` direction is explicitly adjudicated as subject -> prerequisite with prerequisite-change impact using reverse traversal; the QF64-H oracle discriminates reversed edges and wrong impact traversal; and the canonical Markdown fence defect is repaired with a real structural presentation oracle. Protocol 6.3 remains accepted-current. Protocol 6.4 recovery remains unavailable and Stage F remains blocked until a fresh independent Review passes a new immutable assembled target. The sixth design-review disposition below records the pre-implementation design acceptance that authorized the original implementation.'
)
old_graph = r'''\[
(x,y)\in E_D^{\mathrm{def}}
\iff
\text{the canonical semantic statement of }y\text{ directly requires the canonical meaning of }x.
\]'''
new_graph = r'''For semantic unit `s` (the subject) and material direct prerequisite `p`,

\[
(s,p)\in E_D^{\mathrm{def}}
\iff
\text{the canonical semantic statement of }s\text{ directly requires the canonical meaning of }p.
\]

Thus the stored semantic-relation direction is `subject -> prerequisite`. If a prerequisite changes, dependent subjects are discovered by reverse traversal of `E_D^{\mathrm{def}}`; reverse impact traversal is a query over the stored relation, not a second semantic relation or a reversal of its canonical direction.'''
replace_once(workplan, old_graph, new_graph)
new_section_27 = '''## 27. Stage-E repair closure — 2026-09-15

The Stage-E NO-PASS on `0377e798fbbb1054badd1193950d9c10f723be75` identified three blocking findings. Their detailed review chronology remains recoverable in Git and the review handoff; this current handoff records only the resolved contract and the remaining lifecycle gate.

- **SC64-R1 — RESOLVED at D3.** Canonical `USES_DEFINITION` orientation is `subject -> prerequisite`. Formally, `(s,p) in E_D^def` means the canonical semantic statement of subject `s` directly requires prerequisite `p`. A prerequisite mutation discovers dependent subjects by reverse traversal. Stored semantic direction and impact traversal direction are distinct.
- **B64-R2 — RESOLVED at D4 qualification.** QF64-H now encodes subject/prerequisite endpoint roles, rejects the same endpoints with a reversed `USES_DEFINITION` edge, and rejects an impact query that fails to reach the dependent subject from the changed prerequisite while preserving the existing completeness, endpoint, relation-family, cycle and composite-recursion checks.
- **B64-R3 — RESOLVED at canonical source plus D4 qualification.** The Protocol 6.4 public-bootstrap Markdown fence in `protocol-versioning-and-compatibility.md` closes on its own line. A bounded structural Markdown-fence oracle executes over the current 6.4 canonical owner/handoff surfaces and includes a malformed closing-fence-plus-prose negative fixture.

The D3 direction repair is a clarification of the already-implemented subject-to-prerequisite semantics in the canonical 6.4 source owners and derived dependency view; it does not alter the scientific/numerical/software meaning of the published self-reference-safe bootstrap `e09a9d1480211eea2d16d722182bb5c6de1bee12`. The additional source sentences make the already-existing direction/impact distinction explicit. Therefore the published bootstrap identity remains valid; no new bootstrap or recovery identity is invented by this repair.

### Fresh Stage-E re-entry gate

Before Stage F, freeze a new immutable assembled review target containing these repairs and fresh applicable qualification evidence, then perform a fresh independent Stage-E Review against accepted Protocol 6.3 repository state `0928accd337a13f864b292ed81c36372828cfb4c`. The re-review SHALL cover all P64-A..P64-O, QF64-A..QF64-P and F64-A..F64-L obligations, not only the three repaired findings. Until that Review passes, Protocol 6.3 remains accepted-current, Protocol 6.4 recovery remains absent, and Stage F remains blocked.
'''
regex_replace_once(workplan, r'## 27\. Stage-E independent Review reopen — 2026-09-15\n.*\Z', new_section_27)

kernel = 'source/shared/references/abstraction-and-concretization.md'
replace_once(
    kernel,
    'A material direct prerequisite relation may be represented as `x USES_DEFINITION -> y` when the canonical meaning of `x` directly depends on the canonical semantic statement of `y`. Dependency traces/graphs are derived review and impact aids, not authority, and may claim completeness/absence only for an explicitly bounded reviewed scope.',
    'A material direct prerequisite relation may be represented as `x USES_DEFINITION -> y` when the canonical meaning of subject `x` directly depends on prerequisite `y`. The stored relation direction is therefore `subject -> prerequisite`. If prerequisite `y` changes, dependent subjects are discovered by reverse traversal over stored `USES_DEFINITION` edges; reverse impact traversal is a query, not a second relation or a change in canonical direction. Dependency traces/graphs are derived review and impact aids, not authority, and may claim completeness/absence only for an explicitly bounded reviewed scope.'
)

evidence = 'source/shared/references/evidence-evolution-and-dependencies.md'
replace_once(
    evidence,
    "Use `USES_DEFINITION` only for direct semantic prerequisites whose materially different meaning can alter the subject's denotation, admissible domain, validity, parameterization, contract or accepted interpretation. Do not use it for ordinary hyperlinks, imports/call graphs, prose mentions, evidence execution dependencies or every transitive ancestor. A semantic trace may compute transitive closure from direct edges, but the trace is a derived review/impact view rather than authority.",
    "Use `USES_DEFINITION` only for direct semantic prerequisites whose materially different meaning can alter the subject's denotation, admissible domain, validity, parameterization, contract or accepted interpretation. Stored edge direction is `subject -> prerequisite`. A prerequisite-change impact query finds dependent subjects by reverse traversal over those stored edges; the reverse traversal is impact analysis, not a second semantic relation. Do not use `USES_DEFINITION` for ordinary hyperlinks, imports/call graphs, prose mentions, evidence execution dependencies or every transitive ancestor. A semantic trace may compute transitive closure from direct edges, but the trace is a derived review/impact view rather than authority."
)

writing = 'source/shared/references/scientific-technical-writing.md'
replace_once(
    writing,
    'A document fails semantic traceability when a material object is used before it is available, has materially ambiguous meanings, depends on undeclared specialized background, cites a source without identifying the imported semantics, presents external knowledge as local derivation or project invention as universal fact, changes meaning between occurrences, hides a current-owner conflict, or leaves a materially used definition/assumption/validity condition without a recoverable owner/path. Derived dependency traces may assist review but never replace the owner text.',
    'A document fails semantic traceability when a material object is used before it is available, has materially ambiguous meanings, depends on undeclared specialized background, cites a source without identifying the imported semantics, presents external knowledge as local derivation or project invention as universal fact, changes meaning between occurrences, hides a current-owner conflict, or leaves a materially used definition/assumption/validity condition without a recoverable owner/path. When `USES_DEFINITION` is exposed, write the stored relation as `subject -> prerequisite`; a prerequisite-change impact review follows the relation in reverse to dependent subjects rather than redefining the edge. Derived dependency traces may assist review but never replace the owner text.'
)

dependencies = 'source/SEMANTIC_DEPENDENCIES.md'
replace_once(
    dependencies,
    '`USES_DEFINITION` is a direct semantic relation only: ordinary hyperlinks, package/import graphs, call graphs, evidence execution dependencies and incidental prose mentions are not definition edges. A generated dependency trace or strongly connected component condensation is a derived review/impact view and never supplies semantic meaning or warrant. Completeness/absence claims apply only to an explicitly declared reviewed scope.',
    '`USES_DEFINITION` is a direct semantic relation only and is stored as `subject -> prerequisite`: ordinary hyperlinks, package/import graphs, call graphs, evidence execution dependencies and incidental prose mentions are not definition edges. When a prerequisite changes, reverse traversal over stored `USES_DEFINITION` edges finds dependent subjects for impact review; that inverse query does not change the semantic relation direction. A generated dependency trace or strongly connected component condensation is a derived review/impact view and never supplies semantic meaning or warrant. Completeness/absence claims apply only to an explicitly declared reviewed scope.'
)

prompts = 'source/shared/references/development-workflow-prompts.md'
replace_once(
    prompts,
    'Derived `USES_DEFINITION` traces aid bounded review/impact only and are not authority or warrant.',
    'Derived `USES_DEFINITION` traces aid bounded review/impact only and are not authority or warrant. Stored `USES_DEFINITION` direction is `subject -> prerequisite`; prerequisite-change impact follows those edges in reverse to dependent subjects.'
)

versioning = 'source/shared/references/protocol-versioning-and-compatibility.md'
replace_once(versioning, '``` `AUTO_LOCAL_FIRST` may use', '```\n\n`AUTO_LOCAL_FIRST` may use')

tests = 'tests/test_protocol_64_axiomatic_traceability.py'
replace_once(tests, 'import unittest\nfrom pathlib import Path', 'import re\nimport unittest\nfrom pathlib import Path')
replace_once(
    tests,
    'def norm(text: str) -> str:\n    return text.lower().replace("`", "").replace("**", "")\n',
    '''def norm(text: str) -> str:\n    return text.lower().replace("`", "").replace("**", "")\n\n\ndef markdown_fences_well_formed(text: str) -> bool:\n    active: tuple[str, int] | None = None\n    for line in text.splitlines():\n        if active is None:\n            match = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)\n            if match:\n                fence = match.group(1)\n                active = (fence[0], len(fence))\n            continue\n\n        char, minimum = active\n        candidate = re.match(rf"^ {{0,3}}({re.escape(char)}{{{minimum},}})(.*)$", line)\n        if not candidate:\n            continue\n        if candidate.group(2).strip():\n            return False\n        active = None\n    return active is None\n'''
)
replace_once(
    tests,
    '''def qf_h(c):\n    families = {"definition", "assumption", "algorithm", "contract"}\n    return bool(c.get("endpoints") and c.get("direct_complete")) and families <= set(c.get("relations", ())) and not (c.get("independence") and not c.get("scope_complete")) and not (c.get("cycle") and not c.get("composite"))\n''',
    '''def qf_h(c):\n    families = {"definition", "assumption", "algorithm", "contract"}\n    if not bool(c.get("endpoints") and c.get("direct_complete")):\n        return False\n    if families - set(c.get("relations", ())):\n        return False\n    if c.get("uses_definition") != (c.get("subject"), c.get("prerequisite")):\n        return False\n    if c.get("impact_from") != c.get("prerequisite"):\n        return False\n    if c.get("subject") not in set(c.get("impact_dependents", ())):\n        return False\n    return not (c.get("independence") and not c.get("scope_complete")) and not (c.get("cycle") and not c.get("composite"))\n'''
)
replace_once(
    tests,
    '"H": {"endpoints": True, "direct_complete": True, "relations": ("definition", "assumption", "algorithm", "contract")},',
    '"H": {"endpoints": True, "direct_complete": True, "relations": ("definition", "assumption", "algorithm", "contract"), "subject": "algorithm-A", "prerequisite": "definition-X", "uses_definition": ("algorithm-A", "definition-X"), "impact_from": "definition-X", "impact_dependents": ("algorithm-A",)},'
)
replace_once(
    tests,
    '"H": ({"relations": ("definition",)}, {"independence": True, "scope_complete": False}, {"cycle": True, "composite": False}),',
    '"H": ({"relations": ("definition",)}, {"uses_definition": ("definition-X", "algorithm-A")}, {"impact_dependents": ()}, {"independence": True, "scope_complete": False}, {"cycle": True, "composite": False}),'
)
replace_once(
    tests,
    '        self.prompts = read("source/shared/references/development-workflow-prompts.md")\n        self.readme = read("README.md")',
    '        self.prompts = read("source/shared/references/development-workflow-prompts.md")\n        self.semantic_dependencies = read("source/SEMANTIC_DEPENDENCIES.md")\n        self.readme = read("README.md")'
)
replace_once(
    tests,
    '        for phrase in (\n            "floating latest link", "external-source evolution is a binding event",\n            "absence/completeness claims remain bounded",\n            "the semantic dependency graph widens impact discovery; it does not recursively warrant endpoints",\n        ):\n            self.assertIn(phrase, evidence)\n',
    '''        for phrase in (\n            "floating latest link", "external-source evolution is a binding event",\n            "absence/completeness claims remain bounded",\n            "the semantic dependency graph widens impact discovery; it does not recursively warrant endpoints",\n            "stored edge direction is subject -> prerequisite",\n            "reverse traversal",\n        ):\n            self.assertIn(phrase, evidence)\n        self.assertIn("stored relation direction is therefore subject -> prerequisite", kernel)\n        self.assertIn("stored relation as subject -> prerequisite", writing)\n        semantic_dependencies = norm(self.semantic_dependencies)\n        self.assertIn("stored as subject -> prerequisite", semantic_dependencies)\n        self.assertIn("reverse traversal", semantic_dependencies)\n        self.assertIn("stored uses_definition direction is subject -> prerequisite", norm(self.prompts))\n'''
)
anchor = '    def test_qf64_o_candidate_lifecycle_preserves_bootstrap_recovery_separation(self) -> None:\n'
presentation_test = '''    def test_qf64_n_real_markdown_fence_integrity(self) -> None:\n        surfaces = [\n            ROOT / "source/shared/references/abstraction-and-concretization.md",\n            ROOT / "source/shared/references/evidence-evolution-and-dependencies.md",\n            ROOT / "source/shared/references/scientific-technical-writing.md",\n            ROOT / "source/shared/references/protocol-versioning-and-compatibility.md",\n            ROOT / "source/shared/references/development-workflow-prompts.md",\n            ROOT / "source/SEMANTIC_DEPENDENCIES.md",\n            ROOT / "workplans/active/SSDP-6.4-AXIOMATIC-FORMAL-DEFINITION-AND-SEMANTIC-TRACEABILITY-CONSOLIDATED.md",\n        ]\n        for path in surfaces:\n            with self.subTest(path=str(path.relative_to(ROOT))):\n                self.assertTrue(markdown_fences_well_formed(path.read_text(encoding="utf-8")))\n\n        malformed = "before\\n```text\\nvalue\\n``` trailing prose\\nafter\\n"\n        self.assertFalse(markdown_fences_well_formed(malformed))\n\n'''
replace_once(tests, anchor, presentation_test + anchor)
