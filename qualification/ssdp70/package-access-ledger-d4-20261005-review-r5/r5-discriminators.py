import copy,json
import package_ledger as pl
import core70
from test_package_ledger import ReviewDiscriminators,overlap_ledger,event,TWIN,TEST_PARAMETERS,MOUNT
checks=[]
def check(label,value):
    assert value,label
    checks.append(label)
events=[{'sequence':i} for i in range(1,13)]
requests=[{'t_ns':50,'position':2},{'t_ns':150,'position':7},{'t_ns':250,'position':10}]
check('request inside bracket cannot move either edge',pl.candidate_window(100,200,requests,events)=={'start':2,'end':9,'timing_loss':False})
requests=[{'t_ns':100,'position':7},{'t_ns':200,'position':10}]
check('edges use strict before/after comparisons',pl.candidate_window(100,200,requests,events)=={'start':1,'end':12,'timing_loss':False})
p=ReviewDiscriminators();p.setUp()
try:
    ledger=overlap_ledger([(2000,'x/references/owner.md')])
    arguments=dict(mount=MOUNT,parameters=TEST_PARAMETERS,owner_name='owner.md',request_records=[{'t_ns':1000,'monotonic_ns':1000,'position':1,'pairing_verified':True}])
    for label,mutate in [('tree mismatch',lambda l:l['tree_files'].update({'extra':1})),('frozen parameter mismatch',lambda l:l['parameters'].update({'owner_load_quantum':257}))]:
        changed=copy.deepcopy(ledger);mutate(changed)
        result=pl.account(changed,1000,[event(3,TWIN)],p.root,**arguments)
        check(label+' denies exactness',not result['exact'] and result['active_ssdp_bytes'] is None)
        check(label+' preserves pre-R2 positive FAIL',core70.owner_floor_state(result,5,r2_adjudicated=True)=='FAIL')
    changed=copy.deepcopy(ledger);changed['heartbeats']=changed['heartbeats'][:1]
    result=pl.account(changed,1000,[event(3,TWIN)],p.root,**arguments)
    check('missing heartbeat end taints owner negative',not result['owner_floor_exact'])
    check('positive exactly at R2 is not before R2',core70.owner_floor_state({'owner_floor_exact':True,'owner_read_observed':[{'sequence':5}]},5,r2_adjudicated=True)=='PASS')
    requests=copy.deepcopy(arguments['request_records']);requests[0]['monotonic_ns']=requests[0]['t_ns']+TEST_PARAMETERS['clock_tolerance_ns']+1
    result=pl.account(ledger,1000,[event(3,TWIN)],p.root,**{**arguments,'request_records':requests})
    check('request versus fixed baseline disagreement denies owner exactness',not result['owner_floor_exact'])
finally:p.tearDown()
print(json.dumps({'checks':checks,'result':'PASS'},indent=2))
