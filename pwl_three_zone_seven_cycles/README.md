# Seven periodic orbits from a grazing-induced fold

**Sharp upper-bound research:** see [research/L7_UPPER_BOUND_PROGRAM.md](research/L7_UPPER_BOUND_PROGRAM.md) for the new (L^*\le7) conditional program, an exact three-cycle parameter theorem, and high-precision fold tests. This is not an established upper bound.

This folder in `evaristebernhard/math` contains a research manuscript and executable certificate accompanying the revised draft

**Seven Periodic Orbits from a Grazing-Induced Fold: A Computer-Assisted Counterexample in a Three-Zone Saturation Equation.**

The equation is

\[
 x'=-9x+\frac{21}{2}\operatorname{sat}(x)+\frac{181363}{100000}\sin t,
 \qquad \operatorname{sat}(x)=\max(-1,\min(1,x)).
\]

The claim is **at least seven distinct isolated $2\pi$-periodic solutions**, not an upper bound of seven. The former suggestion that five might be a universal upper bound was explicitly conjectural in the 2025 Bravo–Carmona–Fernández–Ojeda preprint. Our proof is computer-assisted and should undergo an independent second implementation audit before journal submission.

## Repository contents

- `paper/main.tex`: revised reader-facing research paper (residence-time mechanism, discovery, exact-flow proof, symmetry, center hyperbolicity, limitations)
- `paper/main.tex`: LaTeX paper source; compile to produce `paper/main.pdf` (a precompiled PDF is provided separately in the ChatGPT conversation)
- `paper/figures/response_data.csv`: numerical continuation data used by the pgfplots figure in LaTeX; not a proof input. `experiments/plot_mechanism.py` replots the saved CSV as PNG without a missing external solver.
- `proof/certify_seven.py`: **primary executable certificate**; six return-map displacement signs, four possible grazing-phase barriers, center ordering and center multiplier; standard Python library only
- `experiments/independent_ode.py`: independent adaptive ODE integration cross-check (SciPy)
- `experiments/high_precision_roots.py`: high-precision roots via exact flight matching (mpmath)
- `experiments/plot_mechanism.py`: exploratory figures (SciPy, matplotlib)
- `notes_discovery.md`: Chinese record of the failed five-cycle proof approach and the search route to this witness
- `tests/test_certificate.py`: standard-library regression test
- `ci/verify.yml`: workflow template; lives in the subfolder and is not yet active as a root GitHub Actions workflow.

## Minimal reproduction

Python 3.10+ is sufficient. Run from the repo root:

```bash
python3 proof/certify_seven.py
python3 -m unittest discover -s tests -v
```

The certificate checks (i) three distinct intervals with opposite Poincaré displacement signs, (ii) transverse switching-time brackets and itinerary geometry, (iii) no grazing on any of the three complete initial-value intervals by strict signs at all four possible tangency phases, (iv) center ordering, and (v) the strict nonunit Floquet multiplier inequality for the center. A successful run ends with

```
CERTIFIED SIGNS, center ordering, and nonunit center multiplier: >= 7 isolated cycles
```

For optional cross-checks:

```bash
python3 -m pip install -r requirements-experiments.txt
python3 experiments/independent_ode.py
python3 experiments/high_precision_roots.py
python3 experiments/plot_mechanism.py
```

Compile manuscript:

```bash
cd paper
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Proof strategy

Write $P(y)=x(2\pi;0,y)$ and $D(y)=P(y)-y$. There are three disjoint intervals

```
[-0.571,-0.567]
[-0.55677,-0.55675]
[-0.55517,-0.55514]
```

whose endpoint displacement signs are `+/-`, `-/+`, `+/-`, respectively. Each therefore contains a fixed point. Exact constant-slope flow formulas and first-hit shape checks show analyticity on the three brackets, hence these zeros are isolated. The half-period involution $x(t)\mapsto-x(t+\pi)$ produces three more distinct orbits. The central antisymmetric orbit is unique and its isolation is certified by $s<\pi/7$, where $s$ is its lower-outer residence time, implying

\[
\log P'(y_c)=3\pi-21s>0.
\]

The argument depends on explicit interval computations. In particular, numerical root values and plotted curve shapes are **not** accepted as the proof.

## Audit status

- Primary rational-decimal interval checker: executed locally and passing.
- Adaptive ODE shooting with a different implementation: agrees with all signs.
- High-precision exact flight matching: agrees with the three roots and multipliers.
- Independent third-party review / a second formally independent interval library: **still outstanding**.
- Paper authorship/affiliation and venue formatting: **provisional, confirm before public release**.

## References

J. L. Bravo, V. Carmona, M. Fernández, I. Ojeda, *Upper bound of the number of limit cycles for symmetric scalar piecewise linear differential equations with three zones*, [arXiv:2507.06705](https://arxiv.org/abs/2507.06705), 2025.

J. L. Bravo, R. Trinidad-Forte, *Finitude of Limit Cycles of Linear Piecewise ODEs in the Cylinder*, [arXiv:2605.05805](https://arxiv.org/abs/2605.05805), 2026.
## Mathematical mechanism (read this before the tables)

Introduce the biased periodic response `lambda=Lambda(xi,mu)` parametrized by the orbit mean `xi`. If `T` is the time inside `|x|<1` and `J>0`, then `Lambda_xi * J=(A+B)(rho-T)` with `rho=2*pi*A/(A+B)`. On a four-crossing orbit, `T=2*pi-s-v`: as the mean increases, the lower exterior time `s` shrinks while the upper exterior time `v` expands, so their competing derivatives can reverse the sign of `T_xi`. For `A=9,B=1.5`, a narrow near-grazing fold in the response creates three positive zeros. The paper explains this geometry first; the interval certificate proves the existence separately.

The paper's `pgfplots` figure reads `paper/figures/response_data.csv`, so LaTeX compilation works without any numerical solver. The script `experiments/plot_mechanism.py` renders PNGs from the same numerical CSV, and does not certify them. The complete numerical generation script used during the initial exploration was a separate RK4/Numba shooting program; the supplied CSV is a reproducibility snapshot, not an independent regenerated dataset.
