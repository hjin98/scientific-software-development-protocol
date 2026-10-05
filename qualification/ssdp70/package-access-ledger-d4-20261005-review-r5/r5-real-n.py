import json
import core70
from test_activation_accounting import RealActivationPath
p=RealActivationPath()
rows=[]
for form,command,expected in [('echo-only','echo '+p.OWNER_PATH,'PASS'),('package-scan',"grep -rl '__SSDP_REVIEW_NEVER_MATCHES_943c__' /opt/ssdp/skills || true",'UNRESOLVED')]:
    summary,agg,identity,rig=p.realize(scenario={'steps':[{'tool_calls':[{'name':'bash','arguments':{'command':command}}]},{'text':'done'}]},claims=[])
    accounting=summary['resource_observation']['accounting']
    state=core70.owner_floor_state(accounting,None,r2_adjudicated=True)
    assert state==expected,(form,state)
    rows.append({'form':form,'owner_floor_state':state,'exact':accounting['exact'],'owner_opens':len(accounting['owner_open_windows']),'positive':accounting['owner_read_observed'],'outer_integrity':agg.get('integrity_outcome')})
print(json.dumps(rows,indent=2))
