# Sharp bound seven research

The manuscript in `../paper/` constructs seven isolated cycles (computer-assisted).
The mathematical target here is an unconditional global upper bound of seven.

- `L7_UPPER_BOUND_PROGRAM.md` derives a rigorous conditional reduction, a fully
  analytic three-cycle parameter regime for $\mu\le B$, and a two-variable
  constrained-Hessian fold discriminant.
- `discriminant_scan.py` numerically computes candidate physical folds in four
  test slope regimes. It is exploratory, **not** a proof of $L\le7$.

Run `python3 research/discriminant_scan.py` from the seven-cycle project root
with `numpy` and `mpmath` installed.