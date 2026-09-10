from __future__ import annotations

from pathlib import Path

source = Path('.github/protocol-61-second-repair-v8.py').read_text(encoding='utf-8')
old = "subprocess.run(['python', '.github/protocol-61-second-repair-v7.py'], check=True)"
if old not in source:
    raise RuntimeError('v8 execution anchor missing')

transport_paths = [
    '.github/workflows/protocol-61-second-repair.yml',
    '.github/workflows/protocol-61-second-repair-v8.yml',
    '.github/workflows/protocol-61-second-repair-v9.yml',
    '.github/protocol-61-second-repair.py',
    '.github/protocol-61-second-repair-v3.py',
    '.github/protocol-61-second-repair-v4.py',
    '.github/protocol-61-second-repair-v5.py',
    '.github/protocol-61-second-repair-v6.py',
    '.github/protocol-61-second-repair-v7.py',
    '.github/protocol-61-second-repair-v8.py',
    '.github/protocol-61-second-repair-v9.py',
    'workplans/active/.protocol-61-second-repair-diagnostic.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v3.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v4.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v5.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v6.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v7.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v8.txt',
    'workplans/active/.protocol-61-second-repair-diagnostic-v9.txt',
]
args = ', '.join(repr(item) for item in transport_paths)
injected = f'''base = Path('.github/protocol-61-second-repair.py')\nbase_text = base.read_text(encoding='utf-8')\nanchor = "    run('python', 'orchestrator/scripts/generate_protocol_snapshot.py', '--check')"\nprecleanup = "    run('git', 'rm', '-f', '--ignore-unmatch', {args})\\n"\nif anchor not in base_text:\n    raise RuntimeError('orchestrator pre-cleanup anchor missing')\nbase.write_text(base_text.replace(anchor, precleanup + anchor, 1), encoding='utf-8')\n\n{old}'''
source = source.replace(old, injected, 1)
exec_path = Path('/tmp/protocol-61-second-repair-v9-exec.py')
exec_path.write_text(source, encoding='utf-8')
compile(source, str(exec_path), 'exec')
exec(compile(source, str(exec_path), 'exec'), {'__name__': '__main__', '__file__': str(Path('.github/protocol-61-second-repair-v9.py').resolve())})
