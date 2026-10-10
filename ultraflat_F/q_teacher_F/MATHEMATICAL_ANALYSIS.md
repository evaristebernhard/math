# Learning the balanced auxiliary F from the certified q49: mathematics first

Date: 2026-10-10. Status: a **negative feasibility analysis and exploratory training baselines**, **not** an effective F or a proof that N=200 works.

## 1. Certified seed and the teacher proxy

The earlier verified quartic recursion starts at `p1(y1)=cos(2πy1)` and proceeds by

`p_j = p_{j−1} + b(p_{j−1}) cos(2πy_j)`, with `b(r)=(1−r²)/2+(1−r²)²/8`.

The certified positive Fejér-squared/Jackson convolution `q49=K*p49` has

`||q49||∞≤1`, `||q49||²₂ ≥ 0.99022519960275`, and `||p49||²₂−||q49||²₂ < 0.00499444856555`.

Crucially, the Fourier multiplier of a normalized Fejér-squared kernel is **nonnegative and ≤1**. Hence

`||p49−q49||²₂ = Σ_s (1−Khat(s))² |b_s|² ≤ Σ_s (1−Khat(s)²)|b_s|² < 0.00499444856555`, so

`||p49−q49||₂ < 0.070672`.

**Meaning:** p49, which costs O(49) to evaluate at a point, can serve as an L² teacher proxy to q49, *but not a pointwise-accurate substitute*. Student loss against p49 of `η` in RMS gives no better guarantee than `||F−q49||₂≤η+0.070672`.

## 2. Exact martingale and parity structure

Because the new `cos(2πy_j)` has zero conditional mean,

`E[p49 | y1,...,yj]=p_j`. Therefore old Fourier coefficients **never change** in later unsmoothed recursion steps; in the smoothed q49 they are only multiplied by known positive Jackson Fourier multipliers.

Since `b(r)` is even and p1 is odd under a half-period translation, for a simultaneous shift of all variables by 1/2,

`p_j(y1+1/2,...,yj+1/2) = −p_j(y1,...,yj)`.

Thus all nonzero Fourier frequencies satisfy `Σ_i s_i ≡ 1 (mod 2)`. The convolution preserves this selection rule. Every `cos yi cos yj` (even total frequency parity) has **exactly zero** Fourier coefficient, so an unconstrained pairwise feature model is a bad architecture. The first useful mixed modes include `(2e_i±e_j)`.

For a student depending only on the first k coordinates, Fourier orthogonality and conditional expectation give the exact information-theoretic floor

`||F−q49||²₂ ≥ ||q49||²₂ − ||E[q49|y1..yk]||²₂ ≥ 0.9902251996 − ||p_k||²₂`.

The reported `M_k` values are Monte Carlo estimates, NOT certified upper bounds. The identity itself is exact.

## 3. Rigorous obstruction to treating the old q coefficients as the balanced F coefficients

Use only the first two recursion layers. The exact expansion is

`p2(y1,y2)=cos θ1 + (19/64−(5/16)cos 2θ1+(1/64)cos 4θ1)cos θ2`.

Consequently, three nonzero Fourier coefficients of every later p_j are

`b_{e1}=1/2`, `b_{2e1+e2}=b_{2e1−e2}=−5/64`.

For a Fejér-squared Jackson cutoff L, write κ_L(h) for its Fourier multiplier. A direct finite sum gives (L≥2)

`κ_L(1)=1−3/(2L²+1)`,

`κ_L(2)=1−(12−9/L)/(2L²+1)`.

The certified q49 cutoffs are L1=2,041,028 and L2=1,041,558. Thus in q49,

`A=|qhat(e1)|=(1/2) κ_L1(1) ≈0.5`,

`B=|qhat(2e1+e2)|=|qhat(2e1−e2)|=(5/64) κ_L1(2)κ_L2(1)≈0.078125`.

Suppose we try to balance **these same coefficients at the same frequencies**, with a single vector v, to relative squared-weight precision η<1:

`(1−η)|a·v| ≤ |qhat(a)|² ≤ (1+η)|a·v|`.

Because `max(|2v1+v2|, |2v1−v2|)≥2|v1|`, necessarily

`2A²/(1+η)≤B²/(1−η)`, or

`η≥(2A²−B²)/(2A²+B²) > 0.97588`.

**This is a rigorous obstruction to direct balance of q49 itself**: relative error below about 97.6% is impossible even on these three modes. It does **not** preclude the OpenAI spreading operation, which replaces an old frequency by a large box of new frequencies and changes individual coefficient magnitudes.

If an exactly balanced student F retains all three original frequency modes, a simple individual-Fourier-coefficient estimate also yields `||F−q49||₂≥(√2 A−B)/(1+√2)≈0.26053`. It does not apply if the student drops/relocates these modes.

## 4. What actually happened in q49-supervised Fourier learning

Two independent 65,536-point Monte Carlo replicas give approximately:

- teacher p49 energy 0.9983–0.9986;
- Fourier energy in singleton cosines: ~0.6814;
- Fourier energy in allowed mixed `cos(2yi)cos(yj)` modes: ~0.0857;
- combined projection: ~0.7671 (49 singleton pairs + 1,176 mixed features, the latter each taking two Fourier sign-pairs, or **D=2401** in total).

The numbers above are **sampling diagnostics, not mathematical certificates**. The simple ordinary pair features `cos yi cos yj` have exactly zero true coefficients by parity. The Jackson q multipliers can only reduce the energy of each retained frequency relative to unsmoothed p49.

A genuine 24-sign-pair Fourier student was trained with Adam on p49 sample values, using 16 singleton modes and four allowed `(2,1)` mixed groups. On an independent 12,000-point holdout, the final squared teacher error was ~0.269, student energy ~0.705, and sampled sup ~2.05. The student does NOT meet the balance, energy, or supremum requirements of Proposition 4.1. The teacher's near-constant modulus does not transfer under sparse Fourier projection.

A separate **exactly balanced** six-pair model was trained against p2 (not q49) with a fixed mass `||p2||²≈0.5685`, optimizing six phases and the v direction. After 1200 Adam steps, sampled sup was still ~1.59, and teacher MSE ~0.644. This is another unsuccessful pilot; small p2 does not have enough initial energy anyway.

## 5. The correct learnable object: coefficient-spreading rather than q-regression

For finite exact original coefficients `b_s`, the OpenAI-style lifted model is

`F(y,z)=Σ_s b_s e(s·y) Π_{j=1}^r f_{s·W_j}(z_j)`, where the Fourier coefficients of each f_β have **exactly equal modulus** `L_β^(-1/2)`.

Then `|chat_(s,u)|²=|b_s|² / n_s`, with `n_s=Π_j L_{s·W_j}`. The balance target requires

`log n_s ≈ log |b_s|² −log |s·γ| +constant`, while the **additional essential** requirement is a uniform approximation by a common shifted q:

`F(y,z) ≈ (Π_j g(z_j)) q49(y+(T/2)Σ_j W_j z_j²)`.

A trainable factor may be parametrized as

`f_β(z)=L_β^(-1/2) Σ_{|u|≤(L_β−1)/2} exp(iθ_{β,u}) exp(2πiuz)`.

The equal-magnitude condition is then exact for every training step. Optimizing θ against `g(z) exp(πi Tβz²)` addresses Lemma 4.2 directly. **But** the factor must be trained for the whole finite list of β, not only one, and full F norm control and n_s balancing need independent certificates.

First sampled pilot: T=63, L=63, 650 Adam steps, chirp approximation maximum grid error 1.00→0.516; at T=127 and 500 steps 1.00→0.492. These are too large to pass the paper's small-δ telescoping error. This is an actual negative feasibility check, not a success.

## 6. Next research gate before N=200

1. Use exact p2 then p3 seed Fourier coefficients to train **several coherent f_β simultaneously**, with exact equal-modulus factors, real symmetry f_{−β}=conj f_β, and certified/controlled sup error.
2. Jointly train a *small* number r of spreading directions W_j with a balance loss on the **explicit small support**. Existing low-rank p3/p4 experiments found large residuals; a successful r≪D construction is not assumed.
3. Only upon obtaining `||F||∞≤1+δ`, nonparallel support, `Σ_a|a·v|<1` close to 1, and uniform coefficient-weight control should the model optimize wave packing/curvature to generate signs.
4. For each finite N, separately check the necessary individual-wave amplitude-resolution `N min_a|a·v|/H²`; N=200 is an experiment target, not implied by the asymptotic theorem. Continue to use an exact integer certificate for the final signs.

**Conclusion:** Use q49 as a certified bounded teacher and preserve its nonlinear Fourier cancellations through the lifted spreading architecture. Direct low-rank regression against q49 provably cannot fix the native weight mismatch by small coefficient perturbations. Do not attempt joint q+F→P200 learning until the F certificate gate is passed.
