# Continuous waveform first: separating F from B_N

Date: 2026-10-10. Status: mathematical notes and negative numerical baselines, **not** a new ultraflat-sign construction.

## 1. The four distinct stages

OpenAI (2026-10-05) uses a real bounded high-dimensional seed q / p_d, then a **real mean-zero trigonometric polynomial F** whose Fourier coefficients match the weights |a·v|, then a complex one-dimensional continuous waveform B_N, then real ±1 Littlewood coefficients.

A nonzero continuous real mean-zero F has a zero on its connected torus, so || |F|-1 ||_infinity >= 1. **Never train F to be pointwise unimodular.** F is required to have ||F||_infinity <= 1+δ and near-unit L2 energy. Pointwise unit modulus belongs to B_N.

## 2. Finite-N waveform-to-sign lemma

Let B:T→C have |B(t)|=1, a real absolutely summable Fourier sequence b_k, and N≥2. Put
- y_k=√N b_k for 0≤k<N
- η=max(0, max_{0≤k<N}|y_k| - 1)
- τ_2=Σ_{k<0 or k≥N}|b_k|²
- τ_1=Σ_{k<0 or k≥N}|b_k|.

Parseval gives (1/N)Σy_k²=1-τ_2. Rescale x_k=y_k/(1+η) so |x_k|≤1. Its rounding defect obeys

μ/N = (1/2N)Σ(1-|x_k|) ≤ 1/2 [1-(1-τ_2)/(1+η)²] =: q_N,

because |x|≥x² on [-1,1]. The *real-sign discrepancy rounding lemma* (OpenAI §3) yields signs s_k for which

|| (1/√N)Σs_k e(kt) - (1/√N)Σx_k e(kt) ||∞
    ≤ C [N^(-1/2) + q_N log(80/q_N)].

Moreover ||(1/√N)Σx_k e(kt)-B/(1+η)||∞≤τ_1/(1+η). Consequently,

sup_t ||P_N(e(t))|/√N-1|
    ≤ (η+τ_1)/(1+η) + C [N^(-1/2) + q_N log(80/q_N)].

The absolute constant C is not extracted here, and no claim is made that this gives an effective ε at N=200. **This explains what to train:** the interior coefficient cap η and both exterior tail statistics, not merely |B| or an L2 coefficient loss. Independent naive sign rounding does not inherit this discrepancy lemma.

## 3. Exact continuous-waveform parameterization

As an alternate mathematical baseline, choose m conjugate pairs of roots α_j=r_j exp(iφ_j), 0<r_j<1, and define the finite real Blaschke product

B(z)=Π_j (z²-2r_j cosφ_j z+r_j²)/(1-2r_j cosφ_j z+r_j² z²).

This satisfies |B(e(t))|=1 **identically**, has REAL Taylor/Fourier coefficients, and no negative Fourier coefficients. With θ=2πt,

(d/dθ)arg B(e^(iθ))=Σ_j [ (1-r_j²)/|e^(iθ)-α_j|² + (1-r_j²)/|e^(iθ)-conj α_j|² ].

OpenAI's derivative condition 0<ψ'<1 translates to requiring the above speed divided by N to be <1. Its mean value is 2m/N. More root pairs may make this constraint worse.

The constant coefficient is b_0=Π_j r_j². It can be made *exactly* 1/√N by setting r_j=exp(-a_j), a_j>0, Σa_j=(log N)/4. This removes a degenerate direction in optimization.

For any 1<R<1/max r_j, Cauchy's estimate gives a rigorous, although typically very pessimistic, positive-frequency ℓ1 tail bound:

Σ_{k≥N}|b_k|≤R^(-N)/(1-1/R) Π_j (R+r_j)²/(1-r_j R)².

Finite Blaschke products are classical; this is an experimental alternative waveform model, NOT a novel theorem or a proven replacement for OpenAI's signed interval packing.

## 4. Diagnostics (not certificates)

For N=200, we trained real conjugate-zero pairs, constrained b_0 exactly, and recomputed diagnostics on a separate 32768-point mesh.

| m pairs | sampled |B|-1 max | √N b0 | min/max √N|b_k| for k<200 | exterior L2 | max normalized phase speed | naive endpoint-projected sign max error (grid) |
|---:|---:|---:|---:|---:|---:|---:|
| 24 | 6.3e-14 | 1 | .0024 / 2.0072 | .00145 | .899 | 1.303 |
| 48 | 1.0e-13 | 1 | .0052 / 2.0027 | .06853 | 2.354 | .991 |

The 24-pair model solves the easy exact structural conditions, but its η≈1.007 and defect parameter q_N≈.376 are far too large. The 48-pair model is also worse on exterior tail and phase-speed criteria. These are FLOATING-POINT DIAGNOSTICS; do not mistake them for exact global certification. No good P200 resulted.

## 5. How to use q49, without destroying phase coherence

The previous certified q49 has |q49|≤1, M=||q49||²₂>0.990225. Therefore the high-dimensional lift

U_q(y)=q49(y)+i√(1-q49(y)²)

satisfies |U_q|=1 and ||U_q-q49||²₂=1-M<0.009775. This is exact, but U_q is **not** automatically a one-dimensional real-Fourier waveform nor an analytic positive-band B_N. In particular, a one-dimensional conjugate-symmetric B obeys B(0),B(1/2)∈{±1}, an endpoint constraint not ensured by simply restricting U_q to a torus orbit.

Taking p49(Y_k) at independent torus points Y_k and setting s_k=sign p49(Y_k) loses the requisite Fourier phase coherence. For independent unbiased Rademacher signs, the normalized squared-modulus 4th moment defect satisfies

E[ || |P_N|²/N -1 ||²₂ ]=(N-1)/N,

by the aperiodic autocorrelation identity. A 200-point independent p49-proxy sign experiment gave measured defect 1.0148 and grid amplitudes [0.0312,2.6336], i.e. very poor flatness (sampling only). The high teacher energy by itself DOES NOT produce the needed ordered signs.

Proper q-guided training must preserve OpenAI's structured stationarity orbit kθ_h+NvQ_h(k/N), rather than generating independent pointwise labels.

## 6. Status / decision

Rigorous: waveform-to-sign lemma; exact Blaschke structure and b0 normalization; q49 unimodular high-dimensional lift; random-label 4th-moment obstruction. Numerical only: m=24/48 experiments and p49 independent-label baseline.

Next: train B_N by constrained phase speed + coefficient cap + exterior ℓ1/ℓ2 tail, and separately train a true balanced F/q-derived structured stationarity orbit. Do not claim these are already integrated. N=200 is an experiment target, not a proof-effective threshold.
