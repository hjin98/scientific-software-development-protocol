from pathlib import Path

p = Path('source/project_engineering_memory.py')
s = p.read_text(encoding='utf-8')
old = '''        if old_sig != new_sig:
            record = new_family.get("semantic_reconciliation")
            if not isinstance(record, dict):
                errors.append(f"{fid}: accepted family semantic identity/applicability changed under the same ID without explicit reconciliation or lineage")
            else:
                evidence = record.get("evidence")
                if (record.get("classification") != "WITHIN_ENVELOPE" or record.get("previous_identity_sha256") != old_sig or not record.get("reason") or not isinstance(evidence, list) or not evidence):
                    errors.append(f"{fid}: same-ID semantic reconciliation must bind the previous envelope, WITHIN_ENVELOPE classification, reason, and evidence")
                else:
                    for raw in evidence:
                        try: parse_evidence_route(raw, f"{fid}:semantic reconciliation evidence")
                        except PemError as exc: errors.append(str(exc))
'''
new = '''        if old_sig != new_sig:
            old_semantic = old_family.get("semantic_identity") if isinstance(old_family.get("semantic_identity"), dict) else {}
            new_semantic = new_family.get("semantic_identity") if isinstance(new_family.get("semantic_identity"), dict) else {}
            mechanically_material = []
            if old_family.get("kind") != new_family.get("kind"):
                mechanically_material.append("kind")
            for key in ("owner_class", "mechanism_family"):
                if old_semantic.get(key) != new_semantic.get(key):
                    mechanically_material.append(key)
            if mechanically_material:
                errors.append(
                    f"{fid}: accepted family changed mechanically material semantic identity field(s) under the same ID: "
                    + ", ".join(mechanically_material)
                    + "; use a new/successor/reclassified identity with lineage"
                )
                continue
            record = new_family.get("semantic_reconciliation")
            if not isinstance(record, dict):
                errors.append(f"{fid}: accepted family semantic identity/applicability changed under the same ID without explicit reconciliation or lineage")
            else:
                evidence = record.get("evidence")
                if (record.get("classification") != "WITHIN_ENVELOPE" or record.get("previous_identity_sha256") != old_sig or not record.get("reason") or not isinstance(evidence, list) or not evidence):
                    errors.append(f"{fid}: same-ID semantic reconciliation must bind the previous envelope, WITHIN_ENVELOPE classification, reason, and evidence")
                else:
                    for raw in evidence:
                        try: parse_evidence_route(raw, f"{fid}:semantic reconciliation evidence")
                        except PemError as exc: errors.append(str(exc))
'''
if old not in s:
    raise SystemExit('semantic strengthening anchor missing')
s = s.replace(old, new, 1)
p.write_text(s, encoding='utf-8')

p = Path('tests/test_protocol_63_independent_review_repairs.py')
s = p.read_text(encoding='utf-8')
old = '''        self.assertTrue(any("semantic identity" in e for e in pem.validate_reconciliation(doc([old]), doc([new]))))
        self.assertEqual(pem.validate_reconciliation(doc([old]), doc([copy.deepcopy(old)])), [])
'''
new = '''        errors = pem.validate_reconciliation(doc([old]), doc([new]))
        self.assertTrue(any("mechanically material semantic identity" in e for e in errors))
        laundering = copy.deepcopy(new)
        laundering["semantic_reconciliation"] = {
            "classification": "WITHIN_ENVELOPE",
            "previous_identity_sha256": pem._semantic_identity_signature(old),
            "reason": "claim that the changed mechanism is merely editorial",
            "evidence": ["repo@1111111:path#review"],
        }
        self.assertTrue(any("mechanically material semantic identity" in e for e in pem.validate_reconciliation(doc([old]), doc([laundering]))))
        self.assertEqual(pem.validate_reconciliation(doc([old]), doc([copy.deepcopy(old)])), [])
'''
if old not in s:
    raise SystemExit('D8-01 strengthening anchor missing')
p.write_text(s.replace(old, new, 1), encoding='utf-8')

p = Path('source/shared/templates/project_engineering_memory_template.md')
s = p.read_text(encoding='utf-8')
needle = 'coverage_basis:'
pos = s.find(needle)
if pos < 0:
    raise SystemExit('template coverage_basis anchor missing')
line_end = s.find('\n', pos)
if 'counterevidence_search:' not in s:
    block = '''\n  # Required before positive_guidance_eligible may be true. This is bounded to the declared scope; it is not a global-history crawl.\n  counterevidence_search:\n    state: COMPLETE_FOR_DECLARED_SCOPE\n    scope: "Replace with the aggregation/coverage scope searched"\n    search_basis: "Replace with the bounded history/evidence search performed"\n    outcomes_reviewed: [SUPPORTING, NEUTRAL, CONTRADICTING, INCONCLUSIVE]\n    blind_spots: "Replace with material unsearched history or 'none known within declared scope'"\n    evidence:\n      - SOURCE@IMMUTABLE_ID:path#stable-locator\n'''
    s = s[:line_end + 1] + block + s[line_end + 1:]
if 'semantic_reconciliation:' not in s:
    marker = 'semantic_identity:'
    mpos = s.find(marker)
    if mpos < 0:
        raise SystemExit('template semantic_identity anchor missing')
    # Document the optional same-ID within-envelope record near the first family example without making it mandatory.
    next_blank = s.find('\n\n', mpos)
    if next_blank < 0:
        next_blank = line_end
    block = '''\n  # Optional only for evidence-bound same-ID editorial/narrowing changes that remain within the accepted envelope.\n  # Changes to kind, owner_class, or mechanism_family require a new/reclassified identity and lineage instead.\n  # semantic_reconciliation:\n  #   classification: WITHIN_ENVELOPE\n  #   previous_identity_sha256: "64-hex digest of prior kind + semantic_identity + applicability"\n  #   reason: "Why this is not a material identity change"\n  #   evidence: [SOURCE@IMMUTABLE_ID:path#stable-locator]\n'''
    s = s[:next_blank] + block + s[next_blank:]
p.write_text(s, encoding='utf-8')
