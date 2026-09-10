from __future__ import annotations

from pathlib import Path

source = Path('.github/protocol-61-second-repair-v3.py').read_text(encoding='utf-8')
source = source.replace("injected = r'''", 'injected = r"""', 1)
marker = "\n'''\n\nanchor = '\\ndef build_and_validate"
pos = source.rfind(marker)
if pos < 0:
    raise RuntimeError('could not locate outer injected-string terminator')
source = source[:pos] + '\n"""\n\nanchor = \'\\ndef build_and_validate' + source[pos + len(marker):]
exec_path = Path('/tmp/protocol-61-second-repair-v4-exec.py')
exec_path.write_text(source, encoding='utf-8')
compile(source, str(exec_path), 'exec')
exec(compile(source, str(exec_path), 'exec'), {'__name__': '__main__', '__file__': str(exec_path)})
