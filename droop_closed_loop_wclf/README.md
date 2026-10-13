# Nonlinear closed-loop worst-case DistFlow certificates

Research record, 2026-10-13. Scope: radial balanced distribution networks with inverter Q/V feedback. This directory is independent of the other math projects in this repository.

## Research question

Given a radial network, bounded renewable/controllable power injections, and voltage-dependent inverter reactive output, obtain **provable steady-state** bus-voltage and line-current envelopes without solving one nonconvex optimization for every bus. The downstream application is safe flexible-load hosting; that control optimization is not yet part of a proved result.

## What is established mathematically

1. A half-disc support function evaluates the exact maximum of a linear response over each independent injection uncertainty set.
2. An affine approximation of a line's complex-power numerator admits an exact reduction of the robust Euclidean-norm maximum to one angular variable. A sampled angular grid needs an additional Lipschitz error allowance to become an upper bound.
3. A new **conditional cubic-gap proposition**, proved in notes/02_cubic_gap.md: when the first-order maximizer has a uniform quadratic-growth margin and the actual nonlinear response has bounded Hessian, evaluating it at the analytic first-order maximizer gives a worst-case-value gap bounded by a constant times uncertainty-scale cubed. This does not require zero nominal line flow.
4. A constructive route to bound the needed Hessian uses implicit differentiation of nonlinear DistFlow and a verified inverse-Jacobian enclosure. See notes/03_nonlinear_certificate_route.md.

These are conditional mathematical statements, not a completed IEEE-33-bus computer-assisted proof or a claim of publication novelty.

## Included files

- notes/01_model_and_prior_work.md — paper comparison and model definition.
- notes/02_cubic_gap.md — exact statement, proof, nondegeneracy cases, limitations.
- notes/03_nonlinear_certificate_route.md — how to convert the theorem to a strict DistFlow certificate.
- notes/04_prior_numerical_work.md — clearly labeled earlier floating-point prototype observations.
- code/half_disc_support.py — dependency-free support function and candidate optimizer.
- code/cubic_demo.py — standalone illustration and scaling test.
- code/test_math.py — elementary regression checks.

Run from this directory: python3 code/test_math.py and python3 code/cubic_demo.py.

## Status / strict scope

- **Proved on paper**: convex half-disc support, angular dual identity, conditional cubic-gap theorem.
- **Still to certify**: uniform interval bound on the actual closed-loop DistFlow Hessian, exact numerical enclosures with directed rounding, handling Q saturation/active-power-dependent Q limits.
- **Not established**: global uniqueness of all AC power-flow roots, dynamic transient safety, or globally optimal hosting capacity.
- Previous 33-bus numbers were obtained with double-precision prototypes and are retained only as research history.

## Relevant prior work

- Sou et al., *Real-Time Worst-Case Load Flow for Distribution Systems With Power Injection Uncertainties*, IEEE Transactions on Power Systems (2026). Uses nonlinear DistFlow with half-disc injection uncertainty and worst-case voltage/current bounds.
- Pantazis & Chong, *Certificate-based Synthesis of Coordinated Droop Control for Heterogeneous Radial Distribution Networks*, arXiv:2608.11141v2 (2026). Linearized DistFlow with dynamic droop; forward-invariant all-time voltage/reactive-command certificates and LP controller synthesis.
- Earlier interval/Krawczyk power-flow literature already provides nonlinear enclosure machinery. The general notions of interval certification, support functions, and contraction are not claimed to be original here.

Next mathematical task: derive and **independently check** an implementable Hessian norm bound M using an explicit, interval-verified inverse-Jacobian bound, then determine in what network regimes the cubic certificate actually beats published worst-case power-flow enclosures.

## Capacity-first extension (2026-10-13)

- notes/06_explicit_hessian_and_capacity.md: closed-loop Jacobian and all mixed second derivatives; computable uniform Hessian bound.
- notes/07_hosting_capacity_control.md: physical vs certified hosting capacity, safe ramping, derivative sign tests, and certified 1-D global search.
- code/one_line_capacity_hessian.py: dependency-free numerical derivative regression on nonlinear two-node DistFlow with incremental load capacity.

Run: `python3 code/one_line_capacity_hessian.py`.

- notes/08_gain_to_capacity_sensitivity.md: use implicit gain sensitivity and active robust constraints to identify which inverter gain locally releases hosting capacity.

## Capacity-first certified quadratic design (2026-10-13)

- notes/09_quadratic_safe_capacity.md: theorem turning validated joint Hessian bounds and half-disc supports into a convex conservative (lambda,g) capacity optimization; explicit fixed-g safe interval and physical toy comparison.
- code/certified_capacity_interval.py: standard-library calculator for the fixed-g certified inner interval, with an exactly solvable line-current toy.

Run: `python3 code/certified_capacity_interval.py`.
