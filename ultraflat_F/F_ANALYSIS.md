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