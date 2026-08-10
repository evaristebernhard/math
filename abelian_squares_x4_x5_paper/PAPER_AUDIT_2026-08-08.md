# Paper audit — 2026-08-08

Paper: **Binary Words with Few Abelian Squares: Four and Five Occurrences of a Letter and Run-Length Structure**

This file records the current technical status after a whole-paper audit. It is not part of the manuscript.

## 1. Main fixed-minority results

### [P] Four occurrences
- Exact value: `M(4,4)=2` and, for `n>=5`,
  \[
  M(4,n)=1+\left\lfloor\frac{n-2}{4}\right\rfloor.
  \]
- Central-concentration argument for `n>=8` rechecked.
- Exact count for the `1+3` family rechecked against the finite verifier.
- Integer optimisation and complete equality list checked by the algebraic verifier through total `b`-mass 100.
- Small cases and complete minimiser lists checked by exhaustive enumeration through length 22.

### [P] Five occurrences
- Exact value: `M(5,5)=2` and, for `n>=6`,
  \[
  M(5,n)=\left\lfloor\frac{n+1}{4}\right\rfloor.
  \]
- Four-`a` balancing lemma rechecked, including its interval/parity endpoint argument.
- Near-extremal two-`a` wing lemma rechecked.
- Run-rigidity proof re-audited branch by branch; no new boundary-availability or distinctness defect was found.
- Exact `1+4`, `2+3`, and one-run counts checked by exhaustive finite verification.
- Equality optimisation and complete minimiser list checked by the verifier.

## 2. General run-length section

Let
\[
E(g)=ab^{g_1}\cdots ab^{g_m},\qquad g_i\ge1.
\]

### [P] Positive-gap rank-window criterion
For a rank-`k` window, the exact existence condition is
\[
-(p_i+q_i)\le \Delta_i^{(k)}\le 2c_i.
\]
The proof was rewritten so that the union of attainable integer intervals is explicit. An independent brute-force audit now checks the criterion for all gap words over `{1,2,3}` through six gaps, all admissible ranks, and all window starts.

### [P] Periodic block count
For `P_h=ab^h`, an occurrence of `P_h^L` yields at least
\[
C(h)\left\lfloor\frac{L-1}{2}\right\rfloor
+\mathbf 1_{2\mid L}B(h),
\]
where
\[
C(h)=\left\lceil\frac{(h+1)^2}{2}\right\rceil,
\qquad
B(h)=\left\lfloor\frac h2\right\rfloor+1.
\]
The count was independently tested for `1<=h<=7`, `1<=L<=8`.

### [P] Weakly monotone gaps
If `g_1,...,g_m` is weakly monotone, then
\[
\theta(E(g))\ge\left\lfloor\frac{m+\sum g_i}{2}\right\rfloor-1.
\]
The nonincreasing case is now stated explicitly as the right-to-left analogue using `Q_h=b^h a`. The final-block parity calculation and the comparison with the FMMS function `F(t)=floor((t+2)/4)` were expanded. The small totals `6<=m+S<=9` are handled explicitly rather than hidden inside a coarse inequality.

### [P] Rank-two-free compensation
If no Abelian-square factor contains four occurrences of `a`, then
\[
\theta(E(g))\ge F(m)+F(S),\qquad S=\sum g_i.
\]
A previous endpoint overcount in the descending branch was corrected before insertion into the main paper: only the rank-one families through `g_{m-2}` are charged automatically. The remaining tail mass is controlled by the superadditive recurrence. The ascending branch was likewise audited with `g_m` treated separately. The cases `m=6` are handled by stronger recurrence estimates, while `m=4,5` use the already proved fixed-minority theorems.

## 3. Claims deliberately NOT promoted to the paper

The following remain research notes / candidates and are not used as manuscript theorems:
- the false universal `|E(g)|/2` lower bound (counterexample recorded in the research notes);
- Mixed-square lemma `#AS_mix >= m-1` [C];
- two-step extension / zero-extension candidates [C];
- dispersion lower-bound candidates [C/O];
- separator-surplus recursion [O];
- good-center / arbitrary-return bridge lemmas, although proved, because they do not yet close a new FMMS class and would distract from the current paper's main narrative.

## 4. Citation and scope corrections made in this audit

- Added the original Fici--Saarela 2014 Dagstuhl Reports citation for the length-`n` conjecture.
- Removed an unnecessary attribution suggesting that the exact two-`a` counting lemma had to be imported from FMMS; the manuscript gives its own proof.
- Replaced the overly specific unverified Cassaigne--Richomme--Saari--Zamboni theorem-number/density wording with the source-supported statement that their binary avoidance problem is equivalent to the classical Pirillo--Varricchio / Halbeisen--Hungerbuehler additive-square problem.
- Clarified that the general theorems concern the normalized positive-gap encoding `E(g)` and do not silently claim all binary words with arbitrary boundary gaps.
- Defined rank terminology before use and removed the undefined word `mixed` from theorem statements.
- Unified the Discussion with the formal rank-window lemma instead of repeating a second indexing convention.

## 5. Reproducibility status

Current `test_verifier.py`: **14 tests, all passing**.

The tests cover:
1. x=4/x=5 main values and extremisers;
2. x=4 exact count;
3. x=5 `2+3` exact count;
4. x=5 `1+4` exact count and nonextremality;
5. x=5 run rigidity finite audit;
6. x=4 central concentration finite audit;
7. wing escape and unique exception;
8. both integer optimisations through total `b`-mass 100;
9. odd near-extremal wing;
10. balancing lemma on small gaps;
11. exact rank-window criterion against direct factor enumeration;
12. periodic block count;
13. weakly monotone gaps;
14. rank-two-free compensation.

Current LaTeX/BibTeX build: successful, 26-page PDF. At the time of this audit the final log contains no unresolved references/citations and no overfull/underfull box warnings.

## 6. Remaining caveat

This is a detailed human/machine-assisted audit, not a formal proof-assistant verification. The longest case analyses (especially run rigidity and the modular integer optimisations) have both been independently finite-tested over substantial ranges, but their written proofs remain conventional mathematical proofs and should still receive normal referee scrutiny.
