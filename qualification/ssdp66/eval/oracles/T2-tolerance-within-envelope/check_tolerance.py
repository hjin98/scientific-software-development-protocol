"""Deterministic check that the repaired visible test tolerance is bound-derived."""
import math
import re
import sys
from pathlib import Path

text = Path(sys.argv[1], "tests", "test_trapezoid.py").read_text()
error = abs(math.pi / 100 * (0.5 * 0 + sum(math.sin(i * math.pi / 100) for i in range(1, 100))) - 2.0)
bound = math.pi * (math.pi / 100) ** 2 / 12
ok = "1e-12" not in text.split("def test_sin_integral", 1)[-1]
numbers = [float(m) for m in re.findall(r"(?<![\w.])(\d+(?:\.\d+)?e-?\d+)", text.split("def test_sin_integral", 1)[-1])]
derived = ("12" in text.split("def test_sin_integral", 1)[-1] and "**" in text) or any(error <= x <= 2 * bound for x in numbers)
print({"removed_machine_tolerance": ok, "bound_derived_or_in_envelope": derived, "error": error, "bound": bound})
sys.exit(0 if ok and derived else 1)
