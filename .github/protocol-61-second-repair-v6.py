from __future__ import annotations

from pathlib import Path

source = Path('.github/protocol-61-second-repair-v5.py').read_text(encoding='utf-8')
old = "exec(code, {'__name__': '__main__', '__file__': str(exec_path)})"
new = "exec(code, {'__name__': '__main__', '__file__': str(Path('.github/protocol-61-second-repair.py').resolve())})"
if old not in source:
    raise RuntimeError('v5 execution-context anchor missing')
source = source.replace(old, new, 1)
exec_path = Path('/tmp/protocol-61-second-repair-v6-exec.py')
exec_path.write_text(source, encoding='utf-8')
code = compile(source, str(exec_path), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(Path('.github/protocol-61-second-repair-v5.py').resolve())})
