import json
import batch_assess70,core70
from test_batch_cli import SlotScoringComposition,SHA
p=SlotScoringComposition();p.setUp(); owner=batch_assess70.score_slots

def augmented(result,manifest,expected,out,key):
    for arm in ('p70','p66'):
        base=next(d for d in manifest['runs'] if d['id']=='T1-'+arm+'-r0')
        for i in range(3):
            rid='critical-'+arm+'-'+str(i)
            d={**base,'id':rid}
            manifest['runs'].append(d);expected[rid]=d
            result['runs'][rid]=p.good(arm);p.write(rid)
        ids=[d['id'] for d in manifest['runs'] if result['runs'][d['id']]['arm']==arm and not d['id'].endswith('-repl')]
        for i,rid in enumerate(ids):
            manifest['opportunities'].append({'id':'critical-'+arm+'-'+str(i),'part':'critical','arm':arm,'fixture':'f','profile_key_sha256':SHA,'realizations':[{'run':rid,'item':'i1'}]})
    p.write("T7-p70-r0",active_ssdp_bytes=14000,owner_read_sequences=[])
    return owner(result,manifest,expected,out,key)

batch_assess70.score_slots=augmented
try:
    r=p.build(replaced='T7-p70-r0',question='t7-owner-floor',owner_replacement={'dispositions':[{'item':'i1','critical':True,'measure':'critical','result':'unresolved'}]},original_overrides={'evidence_state':'COMPLETE_ADMISSIBLE','qualification_outcome':'PASS','criteria':{'harness/admissibility':'PASS','deterministic activation':'PASS'},'resource_observation':{'exact':True},'dispositions':[{'item':'i1','critical':True,'measure':'critical','result':'pass'}]})
    print(json.dumps({'record':r['package_access_replacements']['records'][0],'critical_part':r['parts']['critical'],'critical_failures':r['critical_failures'],'candidate_dispositions':r['arms']['p70']['dispositions'],'owner_part':r['parts']['owner_false_activation']['state'],'fixed_part':r['parts']['fixed_cost']['state'],'harness':r['profiles'][SHA]['harness/admissibility']},indent=2))
finally:
    batch_assess70.score_slots=owner;p.tearDown()
