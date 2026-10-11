# Why q-guided F training needs *spreading*, not arbitrary frequency lifts

**Status 2026-10-11:** rigorous finite-support structural result + exact rational p2 audit. Does **not** construct Proposition 4.1 F or certify any finite Littlewood N.

## 1. What is already known about q49

Previously certified (from the retained proof scripts): `||q49||_∞ <= 1`, `||q49||²_2 > 0.990225`, hence `||q49²-1||²_2 < 0.009775`. This is a valuable seed: there is no reason to retrain its function values from scratch. The missing conditions are a balanced direction `v`, `Σ|a·v|<1` close to 1, controllable Fourier support, and preservation of the sup bound after coefficient spreading. The much smaller q2 below is only a diagnostic model: its energy is **not** near 1.

## 2. Exact one-coordinate coefficient balance is easy if we disregard the sup norm

Let `q(y)=Σ_{s∈A} b_s e(s·y)` be a finite real trigonometric polynomial with nonzero b_s, `b_-s=conj(b_s)` and nonparallel sign pairs. For each representative s, choose `k_s=round(|b_s|²/ν)`, `k_-s=-k_s`, where ν>0 is sufficiently small so k_s≥1. Define

`F(y,z)=Σ_s b_s exp(2πi (s·y + k_s z))`,  `v=(0,...,0,ν)`.

The lifted frequencies remain nonparallel and `F` is real. Furthermore

`| |b_s|² - |(s,k_s)·v| | ≤ ν/2`,  `|Σ_a |a·v| - ||q||²_2| ≤ Dν`, 

where D is the number of sign pairs and `||F||²_2=||q||²_2` exactly. By taking ν small we achieve arbitrarily accurate coefficient-weight matching with **one new circle variable**. However no bound `||F||∞≈||q||∞` follows. Indeed an arbitrary lift generally breaks the cancellations in q².

This observation disproves a *misleading algorithmic intuition*: the extra D spreading coordinates in the OpenAI construction are not intrinsically necessary merely to satisfy coefficient equalities; they are used to preserve pointwise magnitude while balancing. Numerical bandwidth and large integer frequencies may be prohibitive in this simple lift.

## 3. Exact four-point resonance identity

For any odd lift `k_-s=-k_s`, put

`R_(h,l)=Σ_{s+t=h, k_s+k_t=l} b_s b_t`, `R_h=Σ_l R_(h,l)`.

Then Parseval gives

`||F²-1||²_2=(1-M)² + Σ_{(h,l)≠(0,0)} |R_(h,l)|²`, `M=Σ_s|b_s|²`.

The original q has

`||q²-1||²_2=(1-M)² + Σ_{h≠0}|Σ_l R_(h,l)|²`.

So splitting a single original two-sum h across different lifted sums l may either raise or lower the quartic defect, depending on relative phases. When q is already close to ±1, its small autocorrelation usually relies on strong cancellation *among* these grouped terms, making arbitrary spectral relabeling risky.

If *every* additive relation `s+t=u+w` is preserved by the lift, then the fourth-moment spectrum is unchanged (exactly). For tuned p2, all 34 nontrivial pair-sum equations have rank 4 among the six independent sign-pair lift integers: the solution subspace has dimension 2 and consists precisely of linear lifts `k_s=λ·s`. Such a lift is the torus change of variables `F(y,z)=q(y+λz)`, preserving its entire range, not just its fourth moment.

## 4. Rigorous three-mode obstruction to preserving the crucial resonances

For the tuned quartic increment `b(r)=(1-r²)/2+(1-r²)²/8`, the p2 seed is exactly

`p2=cos(y1)+(19/64-(5/16)cos(2y1)+(1/64)cos(4y1))cos(y2)`.

Let `a=(1,0)`, `d=(0,1)`, `b=(2,1)`, `c=(-2,1)` denote signed Fourier modes; their coefficient magnitudes are `|b_a|=1/2`, `|b_b|=|b_c|=5/64`. The relations

`b-d=2a`, `c-d=-2a`

hold in the original support. If any lifted frequency map preserves **both** these additive relations, their images obey `b'-c'=4a'`. Consequently for every common v,

`max(|b'·v|,|c'·v|)≥2|a'·v|`.

Suppose squared coefficient weights have relative error at most η:

`(1-η)|a'·v| ≤ |b_a|² ≤ (1+η)|a'·v|` and similarly for b,c.

Then `2|b_a|²/(1+η) ≤ |b_b|²/(1-η)`, yielding

**`η ≥ (2*(1/4)-(25/4096))/(2*(1/4)+(25/4096)) = 2023/2073 ≈ 0.9758803666`.**

Therefore to achieve precise weight balance by a **single frequency relabeling**, one must break at least one of these two important additive identities, independently of the number of new coordinates and regardless of optimizer power. This does not rule out splitting one seed mode into MANY output modes (OpenAI spreading); a one-to-many operation changes the combinatorics.

## 5. Exact rational experiment (six sign-pairs)

`python exact_lift.py --trials 80 --nu-denom 10000000 --output results.json`

| Model | M=||F||²_2 | ||F||⁴_4 | ||F²-1||²_2 | sup bound after scaling to unit L² (from fourth moment) |
|---|---:|---:|---:|---:|
| Original tuned p2 | 0.56854248047 | 0.45228920225 | 0.31520424131 | ≥1.18289 |
| Linear lift k_s=2s1+s2 | same | **same exactly** | **same exactly** | ≥1.18289 |
| Directly balanced, ν=10^-7 | same | 0.59136171732 | 0.45427675638 | ≥1.35258 |

The balanced lift achieved a maximum relative *squared-weight* error of ~0.002701, and total weight 0.5685426, but broke most additive relations. Its fourth moment is exactly the generic/no-extra-resonance value `3M² - 6Σ_{pairs}|b_s|⁴`. The full energy is only ~0.569 because this is a **small teacher**, so it is NOT an F candidate at δ=.01. The sup numbers are strict lower bounds obtained from `||F||_∞² >= ||F||_4⁴/||F||_2²`, scaled by sqrt(M), not sampled sup claims.

All fourth moments and M are accumulated as exact Python `Fraction`s before decimal display. The random examples are diagnostics, not certificates of all integer lifts.

## 6. Consequence for the next training algorithm

A better q-guided F learner must **learn a one-to-many spreading operator** instead of relabeling Fourier frequencies or minimizing sampled values against q. Candidate form:

`F(y,z)=Σ_s b_s exp(2πi s·y) ∏_{j=1}^r f_(s·W_j)(z_j)`.

Train W_j and equal-modulus Fourier-phase factors f, while retaining an analytic reference `q(y + Φ(z))` and explicitly controlling the telescoped uniform deviation from that reference. Parameter loss must include (i) the maximum coefficient weight error, (ii) the *uniform* sup error, (iii) the additive-collision defect, and (iv) the cost `D, min w, H, N`. The previous low-rank log-factorization experiments had large residuals, so **r<<D is a conjectural optimization target, not achieved**.

For q49 the support cannot be enumerated. A practical next step is to develop tensor-circuit **frequency sampling** and a certified covering bound on the *unseen* modes, or a new analytic family whose coefficient-width product is known structurally. Until then, sampling q49 function values alone is not enough to certify F. Finite N=200 has no guaranteed viability from the asymptotic theorem.

## 7. A constructive *sufficient* stability bound for trainable spreading

Suppose we choose for each original Fourier mode s and j=1,...,r a spreading factor `f_(s,j)(z_j)` and a *coherent ideal factor*

`h_(s,j)(z_j)=g_j(z_j) exp(2πi (s·W_j) ψ_j(z_j))`, with `0≤g_j≤1`.

Assume the true factor is a finite trigonometric polynomial with exact equal-modulus Fourier coefficients, while `||f_(s,j)-h_(s,j)||∞≤eps_(s,j)`.

Define the constructed output and ideal bounded surrogate

`F(y,z)=Σ_s b_s exp(2πi s·y) ∏_j f_(s,j)(z_j)`;

`G(y,z)=(∏_j g_j(z_j)) q(y+Σ_j W_j ψ_j(z_j))`.

Because `||q||∞≤1`, `||G||∞≤1`. Telescoping the products gives the explicit **nonuniform** supremum certificate

`||F||∞ ≤ 1 + Σ_s |b_s| Σ_{j=1}^r eps_(s,j) ∏_{i<j}(1+eps_(s,i))`.

This can be much sharper than selecting one worst-case factor error for all frequencies (although the sum remains astronomically large for a fully expanded q49). It identifies where a model must spend approximation accuracy and supplies a **hard gate** instead of adding an arbitrary sampled-sup penalty.

If each finite factor has exactly `L_(s,j)` Fourier modes of magnitude `1/sqrt(L_(s,j))`, and frequency blocks are uniquely encoded by retaining original s, then every output coefficient from a seed s has squared modulus

`|b_s|²/∏_j L_(s,j)`.

Choose the final linear direction v with nonzero components only along old y, i.e. `(gamma,0,...,0)`; every output frequency associated with s has weight `|s·gamma|`. The coefficient-balance error is therefore controlled *mode by mode* by

`| log(|b_s|² / (|s·gamma| ∏_j L_(s,j))) |`.

These yield TWO independent trainable constraints: the integer product/weight-fitting loss, and the uniform *shared-shear* approximation. A low-rank r is not proven feasible. Strictly obtaining weight mass just below 1 and nonparallel signed output modes are further required gates, not conclusions of these formulae.

### Proposed implementation order

1. On p2 and p3, enumerate exact Fourier coefficients; fit the integer widths L and shared W; prove or refute feasibility at r=1,2,3 before training phases.
2. For feasible widths, train finite factor phases with exact equal-magnitude coefficients, against their **shared** ideal chirps; compute mode-dependent eps_(s,j) and the telescoping sup certificate.
3. Only if the resulting finite F has all Proposition 4.1 conditions and N*w_min/H² is numerically sensible, optimize the continuous packed-wave B_N and finally round to Littlewood signs.
4. On q49, do not claim computational support without an actual sparse Fourier representation or certified tensor-factor integration technique.