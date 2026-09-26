---
kind: d3-d4-implementation-workplan
workplan_id: WP-SIGNAL-RESCALE
status: implemented
---

# Linear rescaling

## Cycle decisions

- Add `sigproc.rescale.rescale(values, low, high)` returning a new list that maps the minimum input to `low` and the maximum input to `high` linearly.
- Constant or empty input raises `ValueError`.
- The input list is not modified.

## Acceptance

- Unit tests cover a normal range, a negative range, constant input, empty input, and that the input list is unchanged.
