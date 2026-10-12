import sys,json,time
from pathlib import Path
repo=Path('/home/samjin/agent-skills/scientific-software-development-protocol')
sys.path.insert(0,str(repo/'qualification/ssdp70/eval'))
import omp_rig,observer70,stand_in_provider
from adapters import omp
original_sse=stand_in_provider._sse
def delayed(handler,chunks):
    if chunks and chunks[0].get('id')=='stand-1':
        time.sleep(2)
    return original_sse(handler,chunks)
stand_in_provider._sse=delayed
rig=omp_rig.Rig(Path('/tmp'),entry='pinned:software-implementation',timeout_s=45)
old=rig.profile
def profile(*a,**kw):
    p=old(*a,**kw)
    p.update(runtime_mode='rpc',activation_mechanism='runtime-command',delivery_transform=observer70.OMP_RPC_TRANSFORM,runtime_input_template=omp.input_template('runtime-command'))
    return p
rig.profile=profile
owner='/opt/ssdp/skills/software-implementation/references/scientific-inspectability-and-initiative.md'
scenario={'steps':[{'tool_calls':[{'name':'bash','arguments':{'command':"python3 -c 'import os,time; pid=os.fork(); (time.sleep(0.5),open(\"/workspace/background-count.txt\",\"w\").write(str(len(open(\""+owner+"\").read())))) if pid==0 else None' </dev/null >/workspace/bg.stdout 2>/workspace/bg.stderr"}}]}, {'text':'R2: Begin consequential analysis.', 'tool_calls':[{'name':'bash','arguments':{'command':'echo R2-ACTION'}}]}, {'text':'Done.'}]}
s=rig.run(scenario)
out=Path(s['_out'])
trace=[json.loads(l) for l in (out/'trace.jsonl').read_text().splitlines()]
records=s['resource_observation']['accounting']['request_records']
proof={'out':str(out),'state':s['evidence_state'],'observation':s['resource_observation'], 'positions':[{k:v for k,v in r.items() if k!='body'} for r in records], 'trace_excerpt':[(i,r) for i,r in enumerate(trace) if ('R2:' in json.dumps(r) and r.get('type') != 'agent_end') or r.get('type')=='tool_execution_start']}
Path('/tmp/ssdp-ledger-background-proof.json').write_text(json.dumps(proof,indent=2))
print(json.dumps({'out':str(out),'state':s['evidence_state'],'windows':s['owner_open_windows'],'positions':proof['positions'],'excerpt_types':[(i,r['type']) for i,r in proof['trace_excerpt']]},indent=2))
