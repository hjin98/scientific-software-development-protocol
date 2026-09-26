---
kind: d3-d4-implementation-workplan
workplan_id: WP-SIGNAL-CLIP
protocol_version: 6.2.0
status: accepted
---

# Bounded signal conditioning

## Stage 1 — smoothing (closed)

- `sigproc.smoothing.moving_average(values, window)` exists with tests.

## Stage 2 — clipping (ready)

- Add `sigproc.clip.clip_values(values, low, high)` returning a new list in which each value is limited to the closed interval `[low, high]`.
- `low > high` raises `ValueError`.
- The input list is not modified.

## Acceptance

- Unit tests cover values below, inside, and above the interval, the `low > high` error, and that the input list is unchanged.
