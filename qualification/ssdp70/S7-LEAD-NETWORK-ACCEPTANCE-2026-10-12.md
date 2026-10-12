---
kind: acceptance-evidence-addendum
governing_protocol_version: 6.6.0
target_protocol_version: 7.2.1
semantic_ref: aaeaf8b6b2121b9fb8aba31917c8265649c43954
author: design lead
date: 2026-10-12
---

# Protocol 7.2.1 S7: network-dependent acceptance checks (design lead)

The implementer and the independent reviewer (`INDEPENDENT-REVIEW-2026-10-12-PROTOCOL-7.2.1-PASS.md`) ran in sandboxes
without DNS. They recorded these checks as not executable there. The design lead ran them with network:

| Check | Tree | Interpreter | Result |
|---|---|---|---|
| `SSDP_VALIDATE_PUBLIC_FALLBACK=1 python -m unittest discover -s tests` | clean detached worktree of `aaeaf8b` (removed after) | CPython 3.11.15 (`uv` venv) | **Ran 438 tests, OK, 0 skipped**, exit 0 |
| `SSDP_VALIDATE_PUBLIC_FALLBACK=1 python -m unittest discover -s tests` | root checkout, pre-commit closeout tree (source/dist = 52ac475) | same | Ran 438 tests, OK, 0 skipped, exit 0 |
| `orchestrator/scripts/run_core_tests.py` | root checkout, pre-commit closeout tree | same | 385 tests across 12 modules, OK (installed-product 32 tests), exit 0 |

The reviewer's full Core run at `aaeaf8b` (385 OK, installed-product via cached wheels) and every other acceptance command
are in the review record. With these results the repository acceptance workflow for `aaeaf8b` is complete; 438 matches the
S3 baseline with no skips.
