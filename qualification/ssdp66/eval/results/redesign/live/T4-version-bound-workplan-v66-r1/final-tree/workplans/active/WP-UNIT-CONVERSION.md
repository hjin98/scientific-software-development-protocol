---
kind: d3-d4-implementation-workplan
workplan_id: WP-UNIT-CONVERSION
protocol_version: 6.4.0
status: accepted
---

# Add pressure unit conversion

Governed by SSDP Protocol 6.4.0. Interpret this workplan under that exact protocol
version.

## Cycle decisions

- Add `units.pressure.to_pascal(value, unit)` supporting `"Pa"`, `"kPa"`, `"bar"`, `"atm"`.
- Unknown units raise `ValueError`; no silent fallback.
- `atm` is the standard atmosphere, 101325 Pa exactly.

## Acceptance

- Unit tests cover every supported unit and the unknown-unit error.
- Existing tests continue to pass.
