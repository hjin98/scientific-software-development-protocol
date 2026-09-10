# Algorithm and Numerical Method Design (D2)

D2 owns the accepted computational/mathematical concretization of D1: algorithm/estimator/discretization/solver semantics, approximation/error/convergence/conditioning/stability, precision and stochastic policy, reproducibility where numerical, and numerical uncertainty. D2 does not own scientific meaning or ordinary software decomposition merely because software executes it.

Universal authority/Challenge/representation rules are in [Abstraction, concretization, authority, challenge, and representation](abstraction-and-concretization.md); evidence lifecycle in [Evidence, evolution, and semantic dependencies](evidence-evolution-and-dependencies.md); test/oracle methodology in [Testing and validation](testing-and-validation.md); human-facing exposition in [Scientific and technical writing](scientific-technical-writing.md).

## D2 normative content

A D2 abstraction may govern, as applicable: estimator/algorithm definition; basis/mesh/time-step/order/sampling; solver/convergence criteria; normalization/weighting/quadrature/integration/reduction/ordering; stability/conditioning/forward-backward error and error budgets; precision/dtype when consequential; stochastic variable/bias/variance/reproducibility semantics; approximation regimes and numerically meaningful failure/fallback; and numerical uncertainty propagated toward D1 observables.

Loops/data structures/libraries/helpers/process topology/device kernels remain D3/D4 unless their identity is itself a numerical invariant.

The logical current owner is the **Numerical & Algorithmic Method Paper** family. It should let a competent reader reconstruct the governed method without reverse-engineering code. Distinguish normative method/error semantics from derivations, benchmarks, literature and pedagogy.

## Method design and acceptance

Recover applicable D1 invariants and directly governed numerical/resource/hardware constraints. State the method mathematically enough to distinguish materially different concretizations; identify approximation sources/regimes; define error, convergence, stability/conditioning, precision and stochastic semantics proportionately to risk; choose minimum justified algorithmic complexity; preserve alternative lower concretizations where identity is unnecessary; and define evidence targets/oracles before optimization can obscure reference behavior.

Do not widen tolerances, lower resolution, change estimand/estimator, alter reduction semantics or relax convergence merely because an implementation/backend otherwise fails.

A material D2 mutation remains proposed until the owning acceptance process completes, including independent falsification and human adjudication where the change can alter scientific conclusions or a governing algorithm/error guarantee.

## Numerical verification and uncertainty

Select the cheapest sufficiently strong authority-backed evidence: units/dimensions; exact/analytical/limiting/asymptotic or manufactured cases; residual/conservation/normalization/symmetry/monotonicity/positivity invariants; refinement and observed convergence order; extrapolation where justified; conditioning/sensitivity; forward/backward error; floating-point range/cancellation; trusted reference/direct comparison; independently justified differential backends; stochastic convergence/bias/variance/seed robustness; and accuracy/performance tradeoff only after correctness.

Tolerance/equivalence derives from accepted conditioning/precision/stochastic/error semantics. Backend/compiler/reduction/vectorization/mixed-precision/accelerator/restart changes must stay within that envelope or reopen D2. Reference implementations are useful only when independently justified enough not to duplicate the production defect.

D2 uncertainty includes discretization/truncation, iterative, stochastic sampling, conditioning/sensitivity, finite precision, approximation and backend/precision variation. Characterize/propagate what can materially change D1 interpretation; keep D1 model/data/parameter uncertainty separate.

## D2 -> D3 handoff and Review

Hand D3 only the computational semantics architecture must preserve: governed operations/data dependencies, precision/reproducibility, error/tolerance, numerically meaningful state/restart, and resource/hardware constraints that shape architecture. Do not freeze software decomposition/library choice without numerical need.

D3 must be faithful to D2 and abstractly adequate: omitting ordering, precision, state or reduction semantics can make a locally coherent architecture numerically wrong. On accepted D2 change, close dependent D3/D4, evidence, documentation/dependency views, required re-ratification and semantic history while preserving unaffected siblings/still-valid evidence.

Material Review seeks wrong limiting behavior, degraded convergence, hidden normalization, instability/ill-conditioning, estimator/stochastic bias, precision bias, non-equivalent restart and parallel/reordered arithmetic outside the accepted envelope. If accepted D2 itself may be materially false, contradictory, ambiguous or unrealizable, raise **SERIOUS CHALLENGE** instead of patching D3/D4 around it.
