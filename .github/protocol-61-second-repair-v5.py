from __future__ import annotations

from pathlib import Path

source = Path('.github/protocol-61-second-repair-v3.py').read_text(encoding='utf-8')
source = source.replace("injected = r'''", 'injected = r"""', 1)
source = source.replace('    """Return the finite local-Markdown closure of direct SKILL activation seeds."""', "    'Return the finite local-Markdown closure of direct SKILL activation seeds.'", 1)
source = source.replace('    """Validate local Markdown closure and reachability from the SKILL entrypoint."""', "    'Validate local Markdown closure and reachability from the SKILL entrypoint.'", 1)
marker = "\n'''\n\nanchor = '\\ndef build_and_validate"
pos = source.rfind(marker)
if pos < 0:
    raise RuntimeError('could not locate outer injected-string terminator')
source = source[:pos] + '\n"""\n\nanchor = \'\\ndef build_and_validate' + source[pos + len(marker):]
exec_path = Path('/tmp/protocol-61-second-repair-v5-exec.py')
exec_path.write_text(source, encoding='utf-8')
code = compile(source, str(exec_path), 'exec')
exec(code, {'__name__': '__main__', '__file__': str(exec_path)})
