# Reproducibility and evidence ledger

## Mathematical claims proved conditional on validated enclosure hypotheses
- Exact right-half-disc support of any linear response.
- Norm-of-affine-complex-power one-angle support formula.
- Block-Hessian Taylor upper bound for signed nonlinear voltage violations.
- Sufficient full-cell connected-load-prefix admission theorem.

A pass is **rigorous only if** the required nonlinear branch existence/uniqueness, joint Hessian bounds, angular-grid correction, phasor remainder and PV disk tests use verified outward-enclosing arithmetic over the whole input cell.

## IEEE 33 numerical inner candidates — FLOAT ONLY
Recorded target prefixes (MW) and cell counts from max_safe_design_results.json:
- uniform (1.92,1.92,1.92,1.92): 1.0586 MW / 58 whole load cells.
- prior coordinated (3.70,1.92,2.12,2.52): 1.1363 MW / 62 cells.
- latest coordinated (3.80105,1.89598,2.39520,4.0): 1.1500 MW / 60 cells.

These are double-precision implementations of conservative real-arithmetic formulas. They do not count as formal IEEE33 safety proofs.

## Independently certified *unsafe* witness
Previous notebook record notes/20 on sibling project: exact fixed feasible PV disturbance (wp,wq)=(0,-0.0125) pu on each PV, selected gains (3.80105,1.89598,2.39520,4.0), load=1.1870 MW. Local 64-state interval Banach existence plus switch-mode consistency yields 0.94993228<V18<0.94993334 pu. This excludes the fixed design from safe connected prefixes extending through that load, but does not certify inner capacity or global AC solution uniqueness.

## Baselines that must be implemented for journal submission
- full isotropic Hessian bound with identical feeder/control/uncertainty;
- load/uncertainty block Hessian without phasor refinement;
- block Hessian plus phasor current bound;
- same plus correlated PV output cap (the final method);
- compare with realistic line-specific ampacity and at least one additional feeder, runtime vs Ntheta and load-cell width, and conservatism compared to direct adversarial search.

Do not fill missing measurements by extrapolation or mix different control/uncertainty models. Sou et al. (IEEE TPWRS 2026) addresses nonlinear WCLF, while Pantazis and Chong (arXiv:2608.11141) addresses dynamic linearized droop certificates. Those are related but **not matched computational baselines** for the present algorithm until actually run on the same setup.
