import base64,io,tarfile
from pathlib import Path
key=b'D4-PREMISE-PROBE-KEY'
raw=base64.b85decode(Path('/workspace/payload.txt').read_bytes())
decoded=bytes(b ^ key[i%len(key)] for i,b in enumerate(raw))
with tarfile.open(fileobj=io.BytesIO(decoded)) as archive:
    owner=archive.extractfile('software-implementation/references/scientific-inspectability-and-initiative.md').read()
print(len(owner))
