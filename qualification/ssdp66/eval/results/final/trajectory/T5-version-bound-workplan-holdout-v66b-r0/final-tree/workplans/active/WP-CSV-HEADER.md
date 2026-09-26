---
kind: d3-d4-implementation-workplan
workplan_id: WP-CSV-HEADER
protocol_version: 6.3.0
status: accepted
---

# Read CSV headers

This workplan is bound to SSDP Protocol 6.3.0.

## Cycle decisions

- Add `tabular.header.read_header(path)` returning the list of column names from the first line of a comma-separated file, with surrounding whitespace stripped from each name.
- An empty file raises `ValueError`.
- Duplicate column names raise `ValueError`.

## Acceptance

- Unit tests cover normal headers, whitespace stripping, empty files, and duplicates.
