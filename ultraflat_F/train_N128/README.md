# Finite-length real Littlewood training: N=128

This experiment **does not** solve the asymptotic ultraflat construction of OpenAI. It replaces the giant auxiliary Fourier F with 128 directly trainable coefficient logits, preserving a small part of OpenAI's finite-stage idea: wave/phase-based initialization followed by projection to real Fourier coefficients/sign rounding and strict verification.

For a real sign vector `s in {-1,+1}^128`:

    U_s(t) = 128^{-1/2} sum_{k=0}^{127} s_k exp(2 pi i k t)
    epsilon(s) = sup_{t in [0,1]} ||U_s(t)| - 1|

## Endpoint arithmetic lower bound

Both P(1) and P(-1) are even integers. Since sqrt(128)=8 sqrt(2)=11.3137085..., any sign vector has `epsilon >= 12/sqrt(128)-1 = 0.0606601717798212`. To target optimal endpoint parity we enforce P(1)=P(-1)=12, i.e. 38 positive entries at even positions and 32 positive entries at odd positions. This constraint is not logically necessary for a weak epsilon=0.76 witness, but it is necessary (up to signs/reflections) for a hypothetical epsilon below 0.116.

## Two-stage training

1. **Differentiable surrogate:** learn `theta in R^128` with an Adam optimizer using `s_soft=tanh(theta/1.2)`, and hard parity-constrained top-k projection. Evaluate hard signs but take straight-through (STE) derivatives through `s_soft`. The loss is the smooth max

       L_k(s) = (log[(1/M) sum_j exp(kappa*| |FFT_M(s)_j|/sqrt(128)-1 |)])/kappa.

   This is only a surrogate gradient because top-k projection is discontinuous. `--ste-steps` enables this stage.

2. **Discrete refinement:** swap opposite signs at indices of the same parity; this keeps both endpoints at +12 exactly. Simulated annealing on `L_k`, then polish at higher `kappa`, using precomputed Fourier bases to cheaply update the spectrum. Seeds include an OpenAI-style wave construction from our previous small-F experiments and p_d-based seeds, as well as random initializations.

## Measured observations (not a general convergence guarantee)

Original F -> N=128 candidate from previous work: exact full-circle epsilon <= 0.80 (rather weak). More direct training experiments yielded a better candidate, with dense grid min `~0.259602` and max `~1.743532`, but still extremely far from unit modulus. An independent exact-rational integer certificate yields `0.24 <= |P(e^{2pi it})|/sqrt(128) <= 1.76` **for all real t**, i.e. epsilon <= 0.76, through a rational parametrization of the circle and a derivative gap estimate. See `certificate_N128_e076.json`. This exact integer certificate checks the *sign sequence*, not the correctness of the training process. The provided run is reproducible with a fixed seed but machine/platform implementation may change optimization search trajectories.

The STE seeds were **not** reliably better than random seeds; this is a negative experimental observation, not evidence against the model-based strategy. Training on 1024 grid values alone is not a valid continuum certificate. No claim of epsilon <= 0.1 or a usable N0(delta) is made.

## Quickstart

    python -m pip install numpy numba torch
    python train128.py --steps 55000 --polish-steps 15000 --restarts 12 --mesh 1024 --seed 20261013
    python train128.py --steps 10000 --polish-steps 2000 --ste-steps 1250 --ste-restarts 6
    python certify_rational.py --file best_signs_N128.csv --M 65536 --epsilon-num 76 --epsilon-den 100
    python -m unittest discover -p 'test_*.py'

**Important:** the exact certificate is for committed `best_signs_N128.csv`. Re-training overwrites the default output, so give another `--out` path to preserve the certified witness.

## What to optimize next

The most fruitful upgrade is **train the phase/curvature parameters of B_N**, not just sign logits, then derive s via its real Fourier projection, and optimize the signed sequence in an inner loop. Require the phase derivative to stay in (0,1), force B(-t)=conj(B(t)), and optimize the spectral L_infinity objective. That is substantively closer to the wave framework of the original paper and supplies a more structured low-dimensional parameterization. It remains an experimental problem.
