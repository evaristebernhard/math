# Supplementary computational certificates

This file records the machine-verifiable material supporting the exact finite coding statements in `main.tex`.  All submission-level computations use integer or exact rational arithmetic; no floating-point sign decision enters a theorem.

## Core finite certificates

`verify_core_certificates.mjs` checks the weight-72 lift-pair certificate, the weight-64 residual upper bound, the exact degree-five identity giving `A_64 >= 533`, the weight-48 first-residual bound, the `A_64 + 21 A_48 >= 533` identity, and the incidence thresholds used in the paper.

SHA-256:

`ad5b3f598a45917f7dc9f9140274a4c615228c860cbbfe7f90d9581b54fba48b`

## Residual-32 split-MacWilliams certificates

The three scripts below enumerate the complete allowed four-block state space for a residual-32 triangle with block sizes `(73,32,32,32)`.  They retain the full octic weight spectrum; in particular, weights `88,96,104,112` are not deleted.  The nonnegative dual multipliers are embedded as integer numerators over a common exact denominator, and every pointwise inequality is checked with Python integers.

1. `verify_triangle_A88_A96_abundance.py`
   - certifies `A_88 + A_96 >= 65`;
   - SHA-256: `d786165da52a1db52212f948587760a92650c33d9d0c0acde857d05fedf5db52`.

2. `verify_triangle_A88_3A96_abundance.py`
   - certifies `A_88 + 3 A_96 >= 185`;
   - SHA-256: `fcc9ba8c906673dffe16e1fc5e0a7c48d432eec8dfd520304efba79ecb81ff78`.

3. `verify_triangle_mixed_or_471.py`
   - certifies that absence of a nonzero `H`-coset mixing weight `64` with weight `88` or `96` forces `A_88 + A_96 >= 471`;
   - SHA-256: `6a1e80cb031e8db4c50344c161c58280d92cfcf03d484a5eab95e00ed603b19d`.

## Hilbert and liaison checks used by the submission

The submission test suite also runs:

- `verify_triangle_hilbert.mjs`;
- `verify_triangle_cubic_reduction.mjs`;
- `verify_triangle_unique_cubic_nested.mjs`.

These scripts reproduce the finite Hilbert-vector enumerations and liaison arithmetic quoted in the residual-triangle section.

## Verification command

From the `paper_submission` directory, run

```text
npm test
```

The separate command `npm run test:research` additionally executes exploratory weight-48 residual experiments.  Those research-only experiments are not inputs to any theorem in the submitted manuscript.

## Scope

The scripts verify finite enumerations, polynomial identities, exact dual certificates, and integer incidence calculations.  They do not replace the geometric arguments in the manuscript.  In particular, the determinant-presentation theorem, transversality arguments, blow-up geometry, invariant-Lagrangian analysis, and ramification/Euler arguments are proved in the text itself.
