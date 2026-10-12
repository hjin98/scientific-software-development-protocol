import json
from test_batch_cli import SlotScoringComposition
p=SlotScoringComposition(); p.setUp()
try:
    r=p.build(replaced="T1-p70-r0",question="bytes",owner_replacement={"evidence_state":"INADMISSIBLE","qualification_outcome":"NOT_EVALUATED","dispositions":[],"original_dispositions":[{"item":"i1","measure":"critical","critical":True,"result":"fail"}]})
    print(json.dumps({"selected":r["scored_slots"]["T1-p70-r0"],"record":r["package_access_replacements"]["records"][0],"critical_failures":r["critical_failures"],"candidate_dispositions":r["arms"]["p70"]["dispositions"]},indent=2))
finally:
    p.tearDown()
