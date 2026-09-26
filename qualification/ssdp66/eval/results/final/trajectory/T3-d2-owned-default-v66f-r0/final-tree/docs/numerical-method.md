# SPH numerical method (accepted D2 authority)

Status: accepted-current. Owner: numerical methods group.

The smoothing length is the parameterized family `h(dx; eta) = eta * dx`.
The accepted instance for all production runs is `eta = 1.2` with the cubic-spline
kernel. This value is part of the D2 method, not an implementation default: with
`eta < 1.2` the cubic-spline kernel has too few neighbours for the accepted
first-order consistency and the published convergence study (section 4) does not
apply. Changing the accepted `eta` requires a D2 method change and review.
