# Superseded operator material (skills-only 7.2, S2)

Governing SSDP version: 6.6.0. This directory is the 7.1 requalification operator material (P3 work order, runbook inputs, dev-probe builders and
diagnostics). It is frozen history and is superseded for P3 by a contract v2 work order.

- `tool-pins.sha256` pins the harness files of the 7.1 tree. The S2 consolidation changed or removed those files (see `../eval/RETIRED-MODULES.md`),
  so these pins no longer match the working tree; they describe the 7.1 tools at their pinned commits.
- `diagnose_dev_probe_20261007.py` stays valid as an independent read-only reproduction of the 2026-10-07 development-probe figures; `../qual-v2/h4.py legacy`
  re-scores the same runs, and `../qual-v2/test_h4.py` pins the two to the same figures.
