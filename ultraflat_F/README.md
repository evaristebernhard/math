# Directly balanced Fourier auxiliary F — exploratory research

We seek the auxiliary polynomial in Proposition 4.1 of *Ultraflat real Littlewood polynomials* (OpenAI, 2026-10-05). This is **not** a completed ultraflat Littlewood construction.

## Two experiments

**Direct balance:** select distinct nonparallel integer frequencies `a_j` in Z²; fix a direction `u`; put `w_j=|a_j·u|/(2 sum_i|a_i·u|)` and `c_{a_j}=sqrt(w_j) exp(i phi_j)`, `c_{-a_j}=conj(c_{a_j})`. Then `F=2 Re sum c_{a_j} exp(2π i a_j·x)` has mean zero, `||F||_2²=1`, and exact balance with vector `v=u/(2 sum|a_i·u|)`. Optimize the phases to minimize `J=||F²−1||_2²`. This **does not guarantee a small supremum**. Numerical L-BFGS searches only provide candidate diagnostics, not globally optimal values.

**Reduced spreading:** starting from exactly expanded small `p_d`, test whether `log(|b_s|²/|s·gamma|)` can be fitted by an additive constant plus `sum_{j=1}^r log|s·W_j|`. The objective is nonconvex and fits are not impossibility certificates.

## Run

```bash
python -m pip install numpy scipy
python -m unittest -v test_balanced_f.py
python balanced_f.py --radius 4 --rho 0.3 --restarts 6 --maxiter 650 --output candidate.json
python low_rank_fit.py --restarts 6 --output low_rank.json
python primitive_jackson_math.py
python certify_primitive.py --n 8 --dimension 2
```

The two recorded scans in `experiments/` are from fixed seeds and the indicated local optimizers. Reproduction needs NumPy/SciPy; exact primitive energy certification additionally needs mpmath or the packages noted in that script.

## Hard distinction

* `||F||_2²=1` + exact Fourier balance is easy to impose, but **cannot** hold with `||F||∞=1` for a real continuous mean-zero F. Near-1 sup requires constructing an almost sign-valued F with narrow transition regions.
* `J=||F²−1||₂²` is an exact finite Fourier quartic quantity, and for `M=||F||₂²=1`, `||F||∞ >= sqrt(1+J)`. Hence large J certifies failure of an *individual candidate*. Small J alone does not certify success: a separate global supremum bound is required.
* Grid maxima are **lower bounds** for the true torus supremum. The FFT computation of the quartic mean is exact in real arithmetic because each grid dimension exceeds four times the maximum frequency coordinate; IEEE floats still have rounding error.
* The source seed for `low_rank_fit.py` is a modified experiment with `p_1=cos(2π y_1)` (not the paper's `p_0=0, p_1=½ cos`). Numerical fits refer to that particular variant, not the original first step.

See `F_ANALYSIS.md` for proofs, numerical results, limitations, and next steps.