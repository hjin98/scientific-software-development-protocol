from pathlib import Path

p = Path('tests/test_protocol_63_engineering_memory.py')
s = p.read_text(encoding='utf-8')
old = '''        family["binding_health"] = "HEALTHY"\n        self.assertFalse(any("positive guidance eligibility" in error for error in pem._validate_family(family)))\n'''
new = '''        family["binding_health"] = "HEALTHY"\n        family["counterevidence_search"] = {\n            "state": "COMPLETE_FOR_DECLARED_SCOPE",\n            "scope": family["aggregation_scope"],\n            "search_basis": "bounded test history",\n            "blind_spots": "broader history not claimed",\n            "outcomes_reviewed": ["SUPPORTING", "NEUTRAL", "CONTRADICTING", "INCONCLUSIVE"],\n            "evidence": ["repo@1111111:path#counterevidence-search"],\n        }\n        self.assertFalse(any("positive guidance eligibility" in error for error in pem._validate_family(family)))\n'''
if old not in s:
    raise SystemExit('positive guidance fixture anchor missing')
p.write_text(s.replace(old, new, 1), encoding='utf-8')
