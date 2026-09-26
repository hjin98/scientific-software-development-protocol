# Numerical method (accepted D2 authority)

Status: accepted-current.

`quad.trapezoid.integrate(f, a, b, n)` is the composite trapezoidal rule with `n`
uniform panels, `h = (b - a) / n`. The method is fixed by this document; changing the
quadrature rule (for example to Simpson's rule) is a D2 method change that requires
D2 review because downstream flux-conservation results were validated with the
trapezoidal rule.

Error model: for `f` in C^2 on `[a, b]`,

    |E| <= (b - a) * h**2 * max|f''| / 12.

Test tolerances for smooth integrands SHALL be derived from this bound (a safety
factor of at most 2 is acceptable); they must not be set by observing a backend.
