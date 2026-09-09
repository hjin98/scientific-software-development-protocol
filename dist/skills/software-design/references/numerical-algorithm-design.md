# Algorithm and Numerical Method Design (D2)

D2 owns the accepted computational/mathematical realization of D1: algorithms, discretizations, estimators, solvers, approximation/error semantics, convergence expectations, precision policy, and numerical uncertainty. D2 is not owned by Software Design merely because software implements it.

## D2 authority

A D2 abstraction may include, as applicable:

- discrete/stochastic estimator or algorithm definition;
- discretization, basis/mesh/time-step/order/sampling semantics;
- solver and convergence criteria that affect the governed result;
- normalization, weighting, quadrature/integration, reduction, and ordering semantics;
- numerical stability, conditioning, forward/backward error, and tolerance/error budgets;
- precision/dtype policy where it can affect scientific conclusions;
- reproducibility/stochastic semantics, random-variable definitions, bias/variance guarantees;
- approximation regimes and fallback/failure behavior with numerical meaning;
- numerical uncertainty and how it propagates to D1 observables.

Implementation-specific loops, data structures, libraries, helper APIs, process layouts, and device kernels remain D3/D4 unless their identity is itself an accepted D2 semantic requirement.

## Numerical & Algorithmic Method Paper

The logical D2 normative document family is the **Numerical & Algorithmic Method Paper**. It should be sufficient to reconstruct the governed method without reverse-engineering implementation details.

Distinguish normative algorithm/error semantics from supporting derivations, benchmark evidence, literature, and pedagogy. Proposed edits are not accepted current authority. Each material D2 claim has one accepted-current semantic owner even when several upstream authorities constrain it.

## D2 design

For a new or changed D2 method:

1. enumerate applicable D1 invariants and domain-local numerical/performance/hardware constraints;
2. state the algorithm mathematically enough to distinguish materially different realizations;
3. identify approximation sources and the regime in which they are admissible;
4. define error, convergence, stability/conditioning, precision, and stochastic semantics proportionately to risk;
5. choose the minimum justified algorithmic complexity within the admissible set;
6. preserve alternative implementation freedom below D2 when exact mechanism identity is unnecessary;
7. define numerical verification evidence before optimization can obscure the reference behavior.

A material proposed D2 mutation is not accepted-current authority until an independent reviewer/context that did not author it has attempted falsification and passed it, followed by any required human adjudication. If either prerequisite is missing, preserve the proposal as non-governing rather than allowing implementation or later review to make it authoritative by use.

Do not widen tolerances, lower resolution, change an estimator, alter summation/reduction semantics, or relax convergence criteria merely because a backend otherwise fails.

## Numerical oracle and verification strategy

Select the cheapest sufficiently strong evidence for the actual D2 claim. Useful evidence includes:

- dimensional/unit consistency;
- analytical, exact, limiting, or asymptotic cases;
- manufactured solutions where valid;
- residual checking;
- conservation, normalization, symmetry, monotonicity, positivity, or other authority-backed invariants;
- mesh/time-step/order/sample refinement and observed convergence order;
- Richardson/extrapolation methods where justified;
- conditioning and sensitivity analysis;
- forward/backward error analysis;
- floating-point range/cancellation/precision analysis;
- trusted reference/direct solver comparison;
- differential comparison across independently justified implementations/backends;
- stochastic convergence, bias, variance, and seed robustness;
- accuracy/performance Pareto analysis after correctness is established.

A simple dense/direct/reference implementation can be retained as an oracle when it has independent justification and the maintenance cost is warranted. It must not merely duplicate the production algorithm's defect.

## Exactness, tolerance, and equivalence

Use exact equality for discrete identities where the abstraction requires exactness. Use absolute/relative/statistical tolerances only when justified by conditioning, precision, stochastic semantics, or an accepted error budget. Compare final governed observables, not only an optimized intermediate kernel.

Backend, compiler, parallel-reduction, vectorization, mixed-precision, accelerator, or restart changes must remain inside the accepted D2 equivalence/error envelope. If they cannot, the issue is D2 redesign rather than a D4 test adjustment.

## Numerical uncertainty

D2 uncertainty includes discretization/truncation error, iteration error, stochastic sampling error, conditioning/sensitivity, finite-precision/rounding effects, approximation error, and backend/precision variation. Characterize and propagate only what can materially change D1 interpretation; do not create uncertainty bureaucracy for exact/local claims.

D1 owns model/data/parameter/assumption uncertainty. Keep the boundary explicit so numerical and model uncertainty are not conflated.

## D2 -> D3 handoff

D3 should receive the minimum computational semantics necessary to preserve the method: governed operations/data dependencies, required precision/reproducibility, error/tolerance semantics, state/checkpoint semantics that affect the algorithm, and target resource/hardware constraints where they shape architecture.

Do not freeze one software component decomposition or library choice merely because it is an obvious realization.

Before accepting D3, verify both D3 fidelity to D2 and D3 abstraction adequacy: an architecture that omits ordering, precision, state, or reduction semantics can be locally coherent while violating the method.

## Human ratification

Material D2 decisions require human adjudication when they can change the scientific conclusion or a governing algorithm guarantee, including materially different estimator semantics, approximation validity, accepted bias, error/tolerance budget, or unexplained failure of an expected numerical property. Routine equivalent algorithmic refinements and independently verified implementation detail remain autonomous.

## Review and challenge

Material D2 review should attempt counterexamples: wrong limiting behavior, degraded convergence order, hidden normalization changes, precision bias, unstable/ill-conditioned regimes, stochastic bias, non-equivalent restart, and parallel reductions exceeding the accepted error budget.

If the accepted D2 abstraction itself appears false, contradictory, materially ambiguous, or unrealizable under applicable constraints, raise a Serious Challenge to D2 rather than patching D3/D4 around it.