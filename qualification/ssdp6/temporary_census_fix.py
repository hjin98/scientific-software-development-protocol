import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / 'qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md'
text = p.read_text()
replacements = {
    'reviewed NO-PASS repair state:              100cbde296de6c1a8db14151f34cfacfebc90eb3': 'latest reviewed NO-PASS candidate:             42eb89388dc96879157ba92db9e7f3c59f2c0b36',
    'current repaired public bootstrap:          e12572c021087308570abfa41657a910c6896457': 'current repaired public bootstrap:          190c8b4d352c203ef74c94d57c4f18d30eb7186d',
    'later public mapping descendant:            e6a8c12f065c3d25a41da804c129d6bc0a4f7b50': 'later public mapping descendant:            092c784383868081e9dee2081e3895f3d1263630',
    'final implementation semantic candidate:    3bbbdfa8120646d76336c7b916e6a891c9ed38f2': 'final implementation semantic candidate:    190c8b4d352c203ef74c94d57c4f18d30eb7186d',
    'fresh F2/static-sensor evidence:             6fc26ce374b5346495782871d5d7241de5b90071': 'fresh F5/static-sensor evidence:             092c784383868081e9dee2081e3895f3d1263630',
}
for old, new in replacements.items():
    if old not in text:
        raise SystemExit(f'missing census binding: {old}')
    text = text.replace(old, new, 1)
p.write_text(text)
subprocess.run(['git','diff','--check'], cwd=ROOT, check=True)
subprocess.run(['git','config','user.name','Protocol 6.3 F5 census repair automation'], cwd=ROOT, check=True)
subprocess.run(['git','config','user.email','protocol63-f5-census@users.noreply.github.com'], cwd=ROOT, check=True)
subprocess.run(['git','rm','.github/workflows/temporary-protocol63-census-fix.yml','qualification/ssdp6/temporary_census_fix.py'], cwd=ROOT, check=True)
subprocess.run(['git','add','qualification/ssdp6/SSDP-6.3-PRESERVATION-CENSUS.md'], cwd=ROOT, check=True)
subprocess.run(['git','commit','-m','Correct Protocol 6.3 F5 census identity block'], cwd=ROOT, check=True)
subprocess.run(['git','push','origin','HEAD:ssdp-6.3-engineering-memory'], cwd=ROOT, check=True)
