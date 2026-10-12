import sys,json,base64,hashlib,io,tarfile
from pathlib import Path
repo=Path('/home/samjin/agent-skills/scientific-software-development-protocol')
sys.path.insert(0,str(repo/'qualification/ssdp70/eval'))
import omp_rig,observer70,core70
from adapters import omp
owner=(omp_rig.DIST_SKILLS/'software-implementation/references/scientific-inspectability-and-initiative.md').read_bytes()
key=b'D4-PREMISE-PROBE-KEY'
buffer=io.BytesIO()
with tarfile.open(fileobj=buffer,mode='w') as archive:
    for path in sorted(omp_rig.DIST_SKILLS.rglob('*')):
        if path.is_file(): archive.add(path,arcname=str(path.relative_to(omp_rig.DIST_SKILLS)),recursive=False)
package_archive=buffer.getvalue()
encoded=base64.b85encode(bytes(b ^ key[i%len(key)] for i,b in enumerate(package_archive))).decode()
reader="""import base64,io,tarfile
from pathlib import Path
key=b'D4-PREMISE-PROBE-KEY'
raw=base64.b85decode(Path('/workspace/payload.txt').read_bytes())
decoded=bytes(b ^ key[i%len(key)] for i,b in enumerate(raw))
with tarfile.open(fileobj=io.BytesIO(decoded)) as archive:
    owner=archive.extractfile('software-implementation/references/scientific-inspectability-and-initiative.md').read()
print(len(owner))
"""
rig=omp_rig.Rig(Path('/tmp'),entry='pinned:software-implementation',timeout_s=45,
    project_files={'payload.txt':encoded,'read_payload.py':reader},claims=['active-byte burden'])
old=rig.profile
def profile(*a,**kw):
    p=old(*a,**kw)
    p.update(runtime_mode='rpc',activation_mechanism='runtime-command',delivery_transform=observer70.OMP_RPC_TRANSFORM,runtime_input_template=omp.input_template('runtime-command'))
    return p
rig.profile=profile
s=rig.run({'steps':[{'tool_calls':[{'name':'bash','arguments':{'command':'python3 /workspace/read_payload.py'}}]},{'text':'Done.'}]})
account=s['resource_observation']['accounting']
proof={'out':s['_out'],'encoded_source_sha256':hashlib.sha256(encoded.encode()).hexdigest(),
       'reconstructed_owner_sha256':hashlib.sha256(owner).hexdigest(),
       'package_copy_file_count':sum(path.is_file() for path in omp_rig.DIST_SKILLS.rglob('*')),
       'archive_sha256':hashlib.sha256(package_archive).hexdigest(),
       'fixture_has_whole_owner_line':any(l in (encoded+'\n'+reader).encode() for l in owner.splitlines() if len(l)>=48),
       'state':s['evidence_state'],'byte_exact':account['exact'],'active_ssdp_bytes':s['active_ssdp_bytes'],
       'owner_floor_exact':account['owner_floor_exact'],'owner_read_observed':account['owner_read_observed'],
       'owner_open_windows':account['owner_open_windows'],
       'owner_floor_no_R2':core70.owner_floor_state(account,None,r2_adjudicated=True)}
Path('/tmp/ssdp-ledger-encoded-package-proof.json').write_text(json.dumps(proof,indent=2))
print(json.dumps(proof,indent=2))
