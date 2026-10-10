# F: what direct balancing accomplishes and what it does not

## 1. Target

Let `A={±a_1,...,±a_D}⊂Z^m` contain no parallel distinct sign-pairs. A real mean-zero finite Fourier polynomial `F(x)=Σ_{a∈A} c_a e(a·x)` and `v` need

`||F||∞≤1+δ`, `1−Cδ≤ Σ_{a∈A}|a·v|<1`, `1≤|c_a|/sqrt(|a·v|)≤1+Cδ`.

It is legitimate to explore exact balance first. Select a direction `u` for which `a_j·u≠0`, choose `v=(1−η)u/(2Σ_j|a_j·u|)`, and put `c_{±a_j}=sqrt(|a_j·v|) exp(±iφ_j)`. Then balance is exact and the total weight and energy are `1−η`. The only hard inequality is `||F||∞≤1+δ`.

## 2. Exact autocorrelation objective is NECESSARY

Let `M=||F||₂²=Σ_a|c_a|²` and `R_h=Σ_{a+b=h}c_a c_b`. Parseval gives

`||F²−1||₂²=(M−1)²+Σ_{h≠0}|R_h|²`.

Further `∫F⁴≤||F||∞² M`. Therefore

`Σ_{h≠0}|R_h|² ≤ (||F||∞²−M) M`.

For a Proposition-4.1 solution, the RHS is `O(δ)` (up to its absolute constant). Hence a small off-zero autocorrelation is a **necessary** condition. Conversely, an L² autocorrelation bound alone does not give a uniform sup bound without frequency-dependent estimates.

For normalized `M=1`, let `J=||F²−1||₂²=∫F⁴−1`. Then `||F||∞≥sqrt(1+J)`. This is an individual-candidate rejection test, not a lower bound on the globally optimal J over all supports.

For arbitrary phases, the analytic gradient of J is computed from Fourier coefficients of `(F²−1)F`; the script verifies it against finite differences. A grid of sizes `(4R_1+1)×(4R_2+1)` integrates every quartic term exactly in exact arithmetic. Independently check candidate supremum on a finer grid and then certify it with intervals or a derivative/Bernstein estimate.

## 3. Affine-hyperplane trap

One apparently cheap way to give different harmonics nonparallel tags is to take `a_k=(k,1)` for distinct integers k. For any complex trigonometric polynomial `H`,

`F(x,y)=2 Re(e(y) H(x))`.

Then `||F||∞=2||H||∞`, while `||F||₂²=2||H||₂²`, so

`||F||₂²/||F||∞² ≤ 1/2`.

Consequently tagging all one-dimensional harmonics with a common extra-coordinate frequency **cannot** give a high-energy normalized auxiliary F, even though the pairs are nonparallel and an appropriate v gives uniform coefficient weights. This is structural, not a numerical optimizer failure.

## 4. Numerical local-optimization results, not theorem bounds

Using two-dimensional primitive representatives in `[-R,R]^2`, phases optimized by L-BFGS with 3–6 restarts, direction `u=(1,ρ)`:

| R | D | ρ | best observed J | sampled sup abs |
|---:|---:|---:|---:|---:|
| 2 | 8 | 0.30 | 0.84433 | 1.88049 |
| 3 | 16 | 0.61803 | 0.77533 | 1.82273 |
| 4 | 24 | 0.30 | 0.74509 | 1.82277 |
| 5 | 40 | 0.61803 | 0.74831 | 1.91601 |
| 8 | 88 | 0.61803 | 0.72614 | 2.03606 |

All are far from Proposition 4.1. These are *local* outcomes. The moment bound already forces `||F||∞ ≥ 1.31` on the R=8 candidate, independently of sampled maxima. The test does not rule out better phases, directions, or more structured supports.

## 5. Reduced spreading fit: nonconvex diagnostic

For precisely known Fourier coefficients `b_s` of the **modified** seed from `seed_fourier.py`, set `rho_s=|s·gamma|` and try

`log(|b_s|²/rho_s) ≈ c+Σ_{j=1}^r log|s·W_j|`.

Results at 6 random restarts, with gamma = (sqrt 2,sqrt 3,...), no zero projections:

| d | sign pairs D | r | best log-RMS residual |
|---:|---:|---:|---:|
| 3 | 27 | 1 | 3.73 |
| 3 | 27 | 2 | 3.79 |
| 3 | 27 | 3 | 3.96 |
| 4 | 350 | 1 | 6.55 |
| 4 | 350 | 3 | 6.80 |

Even the easier small seeds fit poorly in these experiments. However, the optimizer is nonconvex; the fit ignores phase-error accumulation in spreading and is **not** an impossibility proof. Larger r does not have a nested exact model here, so worsening values do not by themselves imply a software defect.

## 6. Parameter-count obstruction for generic seed data

With fixed gamma and r spreading vectors W_j∈R^d, the target ratio values lie locally in a family of dimension at most `rd+1` (the `+1` is an overall scale). If D>rd+1, generic independent real target log-ratios cannot be fit exactly. This does not exclude specially structured `p_d` coefficients, and approximate fitting needs quantitative study beyond parameter counting.

## 7. Concrete next mathematics

Investigate additive-resonant supports with controlled convolution multiplicities. A good candidate must simultaneously have exact/near balance, total weight near 1, tiny convolution away from zero, and a certified uniform supremum. Replace random support growth with adding frequencies whose sum-pairs create cancellation at already large autocorrelation indices, then use a **max-norm** refinement in addition to quartic minimization. For reduced spreading, study the special algebraic structure of p_d's coefficients rather than treating log magnitudes as generic numbers.

This directory has no claimed high-quality F and no claimed ultraflat ±1 sequence.
## 8. An obstruction specific to the primitive 2D search space

The direct-balance scan deliberately uses primitive integer frequencies in two dimensions, but this is an extra restriction, NOT part of Proposition 4.1. From the third-grid averaging argument in the earlier primitive-frequency study, any real trigonometric polynomial supported entirely on primitive nonzero frequencies in dimension two satisfies

`||F||_2² / ||F||_∞² <= 80/81`.

Therefore if the weights are normalized to energy 1, its global supremum must be at least `sqrt(81/80) ~= 1.00623059`, irrespective of D or phase optimization. The present scan is valuable for debugging a direct-balance optimizer, but this restricted family cannot solve the auxiliary problem for arbitrarily small δ. A serious next search must allow nonprimitive vectors while keeping *distinct sign-pairs nonparallel* (remove at least one representative of any parallel pair).

The current larger numerical gaps (sample sup about 1.8–2.0) are far worse than this primitive-only floor, so removing primitivity alone is not guaranteed to fix them.

## 9. Breaking primitivity with direction-dependent multipliers

For each radius-4 primitive direction a_j, allow h_j in {1,2,3} and replace a_j by h_j a_j, preserving distinct nonparallel sign-pairs while breaking the primitive-only ceiling. With 100 random multiplier assignments plus all-one and all-two controls (seed 143), the smallest observed quartic objective was J≈0.75077 for **all frequencies doubled**. This is only F(2x), so does not improve intrinsic flatness. In the comparable primitive radius-4 runs, the observed J was ≈0.75486 for the same direction (or ≈0.74509 with another direction). None is good.

To understand this failure, count repeated unordered two-sum representations h=a+b, h≠0. The primitive 24-pair support has 908 repetitions beyond the first representation; 50 random multiplier assignments averaged approximately 616. Such collisions enable cancellations among coefficients of F². Fewer collisions are not an impossibility theorem, but random frequency inflation plainly does not optimize the required additive structure. The next test should insert frequencies specifically to cancel the largest nonzero autocorrelations.

## 10. Greedy cancellation of largest autocorrelations: first failure

Starting with 8 two-dimensional primitive frequency pairs (radius 2), we computed the nonzero Fourier coefficients of F². For dominant h with large |R_h|, generate additional nonparallel frequencies b=h−a using an old signed frequency a, and optimize all phases again with exact coefficient weights |b·v|. With max coordinate 8 and at most 36 candidates per iteration, the first greedy addition b=(3,1) reduced J to about 0.7828445, but the second round had no improving candidate under the selected local optimizer and budget. See `greedy_resonance.py` and the JSON record.

This does **not** establish a local or global lower bound on J: the step uses local L-BFGS, a restricted finite candidate generator, and fixed v direction. The result does suggest adding a **block of mutually resonant frequencies** and optimizing phases and weight direction jointly, instead of one frequency at a time.
