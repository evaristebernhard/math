# Octic even sets — full archive and single-paper submission

This directory deliberately separates **preservation** from **submission**.

## Files

- `RESULTS_LEDGER.md` — complete audited ledger of proved theorems, computational certificates, conditional theorems, corrections, and genuinely open interfaces. Nothing is deleted merely because it does not belong in the single paper.
- `paper_submission/main.tex` — the single-paper manuscript. Its narrative is the low-weight even-set problem, not a toolbox catalogue.
- `paper_submission/SCOPE.md` — explicit keep / appendix / archive-only decisions after the proof audit.
- `paper_submission/PROOF_AUDIT_2026-08-08.md` — theorem-by-theorem audit against the August 5 technical manuscript.
- `paper_submission/scripts/check_tex.mjs` — static LaTeX structure checker, run by `npm test`.

## Current submission route

The paper keeps tools only when they close or substantially reduce a concrete branch:

- Beauville–Endraß coding reduction and the low-weight trichotomy `d(K) in {48,64,72}`;
- exact exclusion of the **minimum-distance-72** branch (not a global prohibition of every 72-word);
- weight-64 symmetric determinant / reduced transverse `CI(4,4,4)` theorem;
- local first-residual classification `32/36/40`;
- `A64 >= 533` plus the exact incidence theorem, which **unconditionally selects a base word with residual distance 32 or 36** and therefore removes the old global dependence on the `40A/40B` interpretation;
- the global minimum-64 incidence route selects a base word with residual distance `32` or `36`; the old split-MacWilliams exclusion of residual 32 is only conditional on the unsupported extra vanishing of weights `88,96,104,112`;
- residual-32 determinant/Hilbert geometry remains an actual proof branch; residual 36 is deliberately left open, with J1/J2, Horrocks and QT/Smith retained as partial structural results;
- a minimum-distance-48 section with the unconditional bound `24 <= d(R) <= 48`, ten local lift profiles, and the 16-point contact-quadric intersection theorem.  No analogue of `A64 >= 533` is currently proved for weight 48.

The more general Jacobian-defect, hidden-defect, circuit, and deformation results remain in `RESULTS_LEDGER.md` for preservation and possible later use.

## Important audit corrections

- The weight-72 MacWilliams theorem excludes `d(K)=72`; it does not imply `A72=0` in the minimum-distance-48 branch.
- The old `40B = unique weight-64 word` interpretation needs an extra residual-intersection input and is not used by the new main route.
- The archived weight-48 second/third residual scripts imposed `A72=0`; those results are currently conditional until rerun with weight 72 allowed.
- The contact-quadric 16-point proof uses a sextic control term on repeated components, giving `6e`, not the erroneous `3e` in the first short submission draft.
- The QT homotopy-error elimination currently uses irreducibility of the quartic carrier.

## Logical boundary

The manuscript does **not** claim `mu(8)=168`.  In the minimum-64 branch the global coding/incidence reduction leaves residual distances 32 and 36: residual 32 remains a geometric branch, while residual 36 is deliberately not pursued to full closure.  The deeper minimum-distance-48 geometry is likewise recorded without overclaiming.

## Verification / build

`npm test` currently passes both (i) the static TeX audit (duplicate labels, undefined references/citations, environment nesting, braces, and duplicate explicit tags) and (ii) exact BigInt/rational verification of the weight-72 certificate, weight-64 residual certificate, weight-48 first-residual certificate/profile list, the `A64` LP polynomial, and the incidence arithmetic. The connector is configured in safe-bash mode and blocks direct `pdflatex` execution, so a genuine TeX compile still needs to be run in a normal TeX environment.
