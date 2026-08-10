# Supplementary computational verification

This file documents the finite verification suite accompanying the manuscript

**Binary Words with Few Abelian Squares: Four and Five Occurrences of a Letter and Run-Length Structure**.

The computations are independent error checks. No theorem in the manuscript uses finite enumeration as a substitute for proof.

## Running the verifier

From the manuscript directory, run

```text
npm test
```

which executes `python3 test_verifier.py`.

## Tests and ranges

The current verifier contains 14 checks.

1. **Main values and extremisers for x=4 and x=5.** Exhaustive enumeration through total word length 22 checks the stated minima and equality families.
2. **Exact count for the x=4, 1+3 family.** The formula for `W_4(s,q,t)` is compared with direct factor enumeration on the finite audit range used by the script.
3. **Exact count for the x=5, 2+3 family.** The formula for `W_5(s,q,t)` is compared with direct factor enumeration.
4. **Exact count and non-extremality for the x=5, 1+4 family.** The stated counting formula and the strict lower bound are checked on the finite audit range.
5. **Five-a run rigidity.** Exhaustive enumeration through length 22 checks that no minimiser with at least three a-runs occurs in that range.
6. **Four-a central concentration.** Exhaustive enumeration through length 22 checks the conclusion that every minimiser in the stated range contains `a^3`.
7. **Wing escape.** All four- and five-a gap vectors with gaps at most 5 are checked, including the exceptional pair `(abababa, abab)` stated in the lemma.
8. **Integer optimisations.** The x=4 and x=5 equality optimisations are checked through total b-mass 100.
9. **Odd near-extremal interior wing.** The finite audit checks gaps below 25.
10. **Four-a balancing lemma.** All gap vectors in `{0,1,2,3,4}^6` are checked.
11. **Positive-gap rank-window criterion.** The interval criterion is compared with direct Abelian-square factor enumeration for all positive gap words over `{1,2,3}` through six gaps and all admissible ranks/window starts.
12. **Periodic block count.** The lower bound is checked for `1 <= h <= 7` and `1 <= L <= 8`.
13. **Weakly monotone gap theorem.** Weakly monotone positive gap sequences over `{1,2,3,4}` through seven gaps are enumerated.
14. **Rank-two-free compensation.** The theorem is checked exhaustively on small positive-gap instances and on generated superadditive increasing and decreasing families.

## Reproducibility status

At the submission-preparation audit on 2026-08-09, all 14 checks passed. The verifier uses exact combinatorial enumeration and integer arithmetic for the tested instances.

The research scripts whose names begin with `research_` are exploratory files and are not part of the submission-level verification suite.
