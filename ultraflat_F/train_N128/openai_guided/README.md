# OpenAI-guided training for real Littlewood polynomials (N=128)

**2026-10-10; experimental, negative result.** The purpose is to train the actual parameters appearing in OpenAI, *Ultraflat real Littlewood polynomials*, §§4–6 (especially Prop. 4.1 and Eqs. (5.7)–(5.12)) rather than optimize only unconstrained 128-sign vectors. **No algorithm in this folder has reproduced the full theorem or outperformed the prior certified N=128 witness.**

## Three complementary, explicitly labeled approximations

### A. `packed_wave_train.py`: piecewise inverse curvature

Sample `B_N(t)=exp(2πi N φ(t))`, where `φ(-t)=-φ(t)` and `φ(1/2)=1/4` at N=128. Parameterize `φ'=x(t)` on `[0,1/2]` as a trainable *continuous piecewise-linear* function with `0.03<=x<=0.97`, and integrate it exactly on each piece. Therefore `|B|=1`, its Fourier coefficients are real, and the principal stationary index lies between 0 and N. Each nonflat piece has constant `φ''=x'`, corresponding to OpenAI's `ψ''=-1/(λχ²)` with constant `χ`. Joined profiles are C¹, preserving the main-phase-derivative boundary cancellation principle. Train the Fourier coefficients `Y_k=sqrt(N) \hat B(k)` to have `|Y_k|≈1`, with exterior spectral leakage penalty. Then apply endpoint-constrained sign projection and parity-preserving sign-swap annealing.

**Difference from paper:** There is no signed hypergraph interval packing (`Lemma 5.2`), fixed finite balanced F, coherent contribution identity (5.12), independent per-wave multipliers `c_a/sqrt(w_a)`, or the paper's certified three-piece gap structure. This is a differentiable baseline for inverse-curvature waves, not a proof of Prop. 5.1. It performed poorly despite nearly unit energy in the target band.

### B. `coherent_F_train.py`: coherent stationary-phase expression with compact `p_d`

For block `h` and `x=k/N`, optimize `θ_h∈T^d`, common `v`, and use the explicit constant-curvature `Q_h(x)=(x-x_h)²/2`. Set

    Y_k = p_d(k θ_h + N v Q_h(k/N))

as in the coherent main-term identity of Eq. (5.12), but substitute an easily evaluated high-energy recursive `p_d` for the fully coefficient-balanced F. Train via straight-through gradients through endpoint-constrained sign projection, then discrete sign-swap search.

**Difference from paper:** The raw `p_d` has no equal-magnitude Fourier coefficient spreading; its coefficients are not matched to one vector v. Thus stationary-phase amplitude normalization and a valid B_N are unproven. This is an isolated test of the coherent *functional form* (5.12).

### C. `balanced_coherent_train.py`: exactly balanced Fourier F

Pick D distinct nonparallel sign-pairs `±a_j` in Z². For a learned direction u and target total mass `m` set

    v = m u / (2 sum_j |a_j·u|),  w_j = |a_j·v|,
    F(x) = 2 sum_j sqrt(w_j) cos(2π a_j·x + φ_j).

Consequently `|c_{±a_j}|²=w_j=|a_j·v|` and `sum_{a} |a·v|=m` **exactly**, while `||F||_2²=m` by Parseval. Train phases, u and piecewise torus trajectories `k θ_h + Nv Q_h` jointly against Fourier-flatness of rounded signs and the *exact* fourth-moment defect `J=∫_{T²}(F²-1)²`. For radius 3 the 32×32 quadrature is exact for this trigonometric polynomial (up to ordinary floating rounding).

**Difference from paper:** We do not obtain `||F||∞<=1+δ`! The observed torus grid already gives `||F||∞>1.96` for the mass-1 run, which rules out Prop. 4.1. The finite-period, signed-interval packing and continuous B_N are not implemented for this model. In the `m=1` ablation, the paper's strict `sum wa<1` is also not met; `--mass .995` enforces this strictness but still has large sup norm. These witnesses are **not** admissible F's.

## Controlled actual results, N=128 (lower is better)

All `ε` in the table are **conservative numeric full-circle Bernstein bounds**, from 131072-point FFT sampling and first-derivative control. They are **not formal floating-point-independent certificates** unless marked separately.

| Model | Setup | Best ε (numeric, conservative) | Key failure |
| --- | --- | ---: | --- |
| Previously committed trained signs | endpoint-constrained direct search | 0.748855 | No OpenAI F structure |
| A: piecewise inverse curvature | 32 pieces; 3×1600 Adam + swaps | 0.915883 | Small spectral tails, large coefficient deviations |
| A: alternating-curvature start | 16 pieces; 3×1800 Adam + swaps | 0.960245 | Similar coefficient collapse |
| B: compact p_d coherent sample | d=20, H=2; 2×400 + swaps | 0.849236 | High p_d energy but no coefficient balance |
| C: exact balance, weak J penalty | D=16, H=4, m=1; 2×250 | 0.895097 | `J=1.29–1.43`, `||F||∞` grid ≳2.30 |
| C: exact balance, strong J penalty | D=16, H=4, m=1; 2×500 | 0.850936 | `J≈0.79–0.83`, sampled `||F||∞≥1.96` |
| C: mass under one | D=16, H=4, m=.995; 2×400 | 0.961854 | `J≈0.80`, sampled `||F||∞≥2.00` |

A separate arbitrary-integer verification of the *mass=1 strong-J* sign witness (not of the model/training) confirms **`0.05 <= |P_128(e^{it})|/sqrt(128) <= 1.95` for every real t**, i.e. ε≤0.95; see `exact_certificate_balanced_e095.json` and `balanced_coherent_signs_N128.csv`. The older sign vector has a better existing exact certificate, ε≤0.76, in the parent `train_N128/` directory.

The endpoint integrality obstruction for N=128 gives ε≥12/sqrt(128)-1≈0.06066. Our finite-N results are far from that lower bound; it is *not* a claim that this lower bound is attainable.

## Repeat experiments

From `ultraflat_F/train_N128/` (this directory's scripts should be copied there):

    python -m pip install numpy scipy numba torch
    python packed_wave_train.py --pieces 32 --steps 1600 --restarts 3 --swaps 9000
    python coherent_F_train.py --dimension 20 --blocks 2 --steps 400 --restarts 2
    python balanced_coherent_train.py --radius 3 --blocks 4 --mass 1 --f-weight 2.5 --steps 500 --restarts 2
    python balanced_coherent_train.py --radius 3 --blocks 4 --mass .995 --f-weight 2.5 --steps 400 --restarts 2
    python certify_rational.py --file balanced_coherent_signs_N128.csv --M 8192 --epsilon-num 95 --epsilon-den 100
    python -m unittest test_openai_wave_train.py

The training outputs are **overwritten** on reruns. Keep separate copies to reproduce each ablation. In particular the exact certificate is for the committed *mass=1* witness, not for a different run or changed training outputs. The original baseline `best_signs_N128.csv` must remain unchanged.

## What the mathematics says to improve next

Trainability alone is not the issue. The missing common structural condition is **simultaneously** low uniform norm of F and coefficient balance:

    |c_a|²≈|a·v|,   Σ_a |a·v|≈1,   ||F||∞≈1.

Under exact balance the Fourier self-correlation defect is

    ∫(F²-1)² = (M-1)² + Σ_{h≠0} |Σ_{a+b=h}c_a c_b|²,   M=||F||_2².

The objective is therefore to jointly design *many cancelling additive resonances* in a sparse set of nonparallel frequencies (possibly optimizing structured phase blocks rather than random phases), while controlling `||F||∞` on the entire torus. Only after constructing an acceptable F can the signed interval packing and coherent B_N phase parameters be optimized as a faithful finite-N instantiation of Prop. 5.1. The direct-balanced D=16 experiment is a useful negative benchmark, not evidence of such a construction.
