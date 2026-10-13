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

## Further capacity control: blockwise Hessian (2026-10-13)

- notes/10_blockwise_hessian_capacity.md: block-Hessian sufficient robust capacity theorem, fixed-g convex safe interval and exact thermal toy.
- code/blockwise_capacity_demo.py: dependency-free proof-formula regression; compare isotropic Hessian, block-Hessian and exact robust toy capacity.

Run: `python3 code/blockwise_capacity_demo.py`.

## Load-ramp dynamics (2026-10-13)

- notes/11_dynamic_ramp_certificate.md: conditional uniform contraction theorem for first-order inverter lag, safe transient tube, and load slew-rate limit tied to certified steady hosting margins.
- code/dynamic_ramp_demo.py: exact scalar first-order tracking model, checks derived ramp bound.

Run: `python3 code/dynamic_ramp_demo.py`. Assumes absolutely continuous renewable/load inputs with bounded change rates; not valid for jumps without additional analysis.

## IEEE 33-bus test (2026-10-13)

- notes/12_ieee33_capacity_benchmark.md: first actual 33-bus capacity-continuity study comparing isotropic vs block-Hessian envelopes, binding voltage/Q/current constraints, and a first-order inverter dynamic ramp stress test.
- **Caution:** benchmark values remain float checks. A package of the complete session numerical scripts was generated separately; the PR does not yet contain that imported dependency tree or CI verification.

## Capacity as the principal object (2026-10-13)

- notes/13_capacity_gap_theorem.md: defines physical vs certified load-hosting upper boundaries; proves a conditional bound on **lost capacity**, `Lambda_true - Lambda_cert <= delta/m`, where delta is worst-case safety-envelope overestimation and m is a verified boundary slope. Includes the gain-uniform corollary and a reverse-flow toy.
- code/capacity_gap_toy.py: self-contained analytic reverse-PV current toy checking the capacity-gap inequality.

Run: `python3 code/capacity_gap_toy.py`. IEEE-33-bus capacity gap remains *unverified*.

## Two-sided IEEE-33 capacity bracket (2026-10-13)

- notes/14_two_sided_capacity_bracket_ieee33.md: complements the certified inner capacity with a physically feasible PV disturbance witness and a componentwise interval-Jacobian sign test of squared-voltage derivative to exclude larger loads on a specified unsaturated branch.
- On fixed g=1.85 in the tested 0–1.25 MW domain, the float-based exploratory bracket is about 1.032555–1.065 MW. Not directed-rounded or verified for saturated control.

## 2026-10-13 corrected PV capability/gain capacity evaluation

- notes/15_coupled_pv_gain_capacity.md: corrects the full PV P²+Q² inverter limit (PV uncertainty plus Q/V feedback), proves the correlated one-angle support and nonlinear residual allowance, provides connected-capacity witness lemma and gain-dependent numerical inner/witness results.
- code/affine_apparent_power.py: dependency-free generic half-disc apparent-power upper and numerical self-check.
- Full IEEE 33 dependency scripts for the new experiment remain in the session research bundle and still require import/CI verification before the GitHub PR can be called independently reproducible.

## Saturation-aware connected-capacity theorem (2026-10-13)

- notes/16_saturation_aware_capacity_vi.md: replace nonsmooth clip differentiation by the projected-variational-inequality equilibrium; prove a conditional strong-monotonicity/residual bound that remains valid across Q-limit switching, and turn it into a steady connected-load capacity criterion.
- code/saturation_vi_toy.py: dependency-free exact-rational demonstration including a high-gain case `g * dV/dq = 2.7 > 1` where raw fixed-point contraction fails but projected-gradient contraction succeeds. Exhaustively **encloses continuous parameter cells**, not just sampled points. Toy bracket: `0.50 <= Lambda_conn < 0.52` (toy units, not MW for IEEE 33).
- Run `python3 code/saturation_vi_toy.py` or `python3 code/test_math.py` from this directory.

**Status:** actual nonlinear IEEE-33 saturated-mode capacity remains UNVERIFIED. Need verified open-loop branch, interval Jacobian strong-monotonicity constants, projected residual enclosures, and physical current limits before claiming an IEEE-33 improvement. This method does not prove inverter transient stability.

## IEEE-33 Hessian/phasor capacity recheck — 2026-10-13

- `notes/17_hessian_phasor_ieee33_capacity_recheck.md`: retain original block-Hessian voltage and PV capability bounds; use prior phasor geometric current upper on the whole load cell, then adaptively refine the connected inner capacity. Observed FLOAT candidates include g=1.85 inner 1.033948 MW, g=1.90 inner 1.053233 MW, and g=1.92 inner 1.058600 MW. Physical clipped-Q witness barriers computed separately. **These numbers are not outward-rounded or full IEEE-33 saturated-mode certificates.**
- Prior experimental numerical source files were recovered and rerun in the current working session and packaged as a standalone 18-file Python source/results artifact; they are **not yet imported in this GitHub branch**. Do not claim complete CI reproducibility from this README.

## Interval-certified physical unsafe witnesses — 2026-10-13

- `notes/18_ieee33_interval_witness_certificates.md`: verified 64-state interval Banach inclusions for two **fixed feasible PV disturbances** in the real clipped-control model: g=1.92 at 1.09322 MW (all PV unsaturated), g=2.6 at 1.22273 MW (PV18 positive-Q clipped). Verified voltage boxes lie strictly below 0.95 pu. These establish physical **upper obstructions** (conditional on designated normal branch), not the all-uncertainty safe **lower** bound, dynamic safety, or global root uniqueness.
- The standalone verifier is inside the recovered working-session zip but has not yet been imported to the repository: Github CI reproduction remains pending.

## Four-inverter capacity-oriented gain selection — 2026-10-13

- `notes/19_coordinated_gain_hosting_optimization.md`: **B builds on A** using the original block-Hessian voltage and phasor current inner envelopes. Select individual gains (bus 9/18/24/33) instead of forcing a common gain.
- IEEE33 FLOAT connected-inner candidates: uniform g=(1.92,1.92,1.92,1.92) gives 1.0586MW; tested coordinated g=(3.70,1.92,2.12,2.52) gives 1.1363MW (+77.7kW, ~7.34%). Neither is outward-rounded full-uncertainty certification or global optimality.
- New feasible unsafe witness at 1.1795MW for the coordinated controller was checked with **mpmath.iv interval Banach inclusion**, strictly unsaturated in the local root box, proving bus18 V<0.95pu. The previously strict uniform-g unsafe witness is 1.09322MW. A directed-interval all-disturbance safe *inner prefix through 1.10MW* for coordinated gains would prove physically improved hosting capacity. **That lower side is still open.**
- Executable joint-gain source and logs are in the separately downloadable complete experiment bundle; not imported to this repository branch yet. Dynamic inverter stability not evaluated.

## Unified maximum safe hosting-capacity design: candidate and all-gain bound — 2026-10-13

- `notes/20_unified_max_safe_capacity_design.md` unifies robust capacity assessment and gain selection as **one** maximum safe hosting design task. The original implicit Jacobian/block Hessian/phasor methods are retained for the candidate safe inner capacity.
- New **standalone standard-library**, exact-rational `code/exact_design_upper.py`: using nominal PV injection as one admissible uncertainty realization, downstream real-power loss minima, and the bus-18 DistFlow voltage identity, proves **a gain-independent NECESSARY outer bound** `L_opt <= 1.452831 MW` for the precise research benchmark (0.31 pu assumed common branch current limit, 0.95–1.05 pu voltages, 0.65 base load scale, four 1MVA PVs, all gain choices). Run `python3 code/exact_design_upper.py` from the project folder; no dependencies.
- New double-precision **candidate** with bus-9/18/24/33 gains `(3.80105,1.89598,2.39520,4.0)` passes the complete prefix `[0,1.1500] MW` using existing block Hessian + phasor + correlated PV capability checks. It is *not* yet an outward-rounded proof. Compared to uniform 1.0586 MW: +91.4 kW / +8.63% in conservative float inner objective.
- One feasible PV disturbance at 1.1870 MW for these gains received a local mpmath.iv interval Banach check with bus18 `V<0.949934` pu and strict unsaturated modes. This is **fixed-g upper obstruction only**, not a bound on all gain designs.
- The full optimized numerical source dependency bundle and interval witness logs are available as a separate session ZIP but are not yet in this PR. **Only the new analytic gain-independent upper bound has a self-contained GitHub reproduction command.**
