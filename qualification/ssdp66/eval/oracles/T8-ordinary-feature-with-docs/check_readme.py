"""T8 deterministic check: the README API section lists median."""
import sys
from pathlib import Path

api = (Path(sys.argv[1]) / "README.md").read_text(encoding="utf-8").split("## API", 1)[-1]
ok = "median" in api
print("README API lists median" if ok else "README API does not list median")
raise SystemExit(0 if ok else 1)
