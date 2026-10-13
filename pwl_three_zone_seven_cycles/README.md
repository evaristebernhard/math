# Competing Residence Times and Seven Limit Cycles

The manuscript **Competing Residence Times and Seven Limit Cycles in a Periodically Forced Three-Zone Equation** proves a parameter-uniform seven-cycle counterexample, with the principal theorem stated in the introduction and proved through the rational witness, exact crossing certificates and uniform continuation.

The equation is

\[
\dot x=-Ax+(A+B)\operatorname{sat}(x)+\mu\sin t,\qquad A,B,\mu>0.
\]

At \((A,B,\mu)=(9,3/2,181363/100000)\), we certify **at least seven distinct isolated periodic orbits**. This contradicts the conjectural maximum five discussed by Bravo, Carmona, Fernández and Ojeda, [arXiv:2507.06705](https://arxiv.org/abs/2507.06705). It does **not** establish an upper bound of seven.

**Main theorem:** for **every** `|A-9|, |B-1.5|, |mu-1.81363| < 1e-12` there are at least seven **isolated** periodic cycles, including **four locally attracting and three locally repelling** cycles. Directed-interval grazing barriers are `>3e-4`, while their perturbation is `<1.505e-6`. The central Floquet logarithm stays `>0.0043`. The ordered response zeros force three distinct critical residence-time profiles. Noncentral hyperbolicity and a global seven-cycle upper bound are not claimed.

## Mathematical idea

A three-zone affine ODE has explicit flights but unknown switching times. The mean-parametrized biased periodic response satisfies

\[
\Lambda_\xi J=(A+B)(\rho-T),\qquad
\rho=2\pi A/(A+B),\quad J>0,
\]

where \(T\) is time spent in the expanding middle zone. If \(s\) and \(v\) denote the lower and upper exterior visits, then \(T=2\pi-s-v\), with \(s_\xi<0\), \(v_\xi>0\): they compete.

At a nondegenerate lower grazing, the disappearing lower visit follows the square-root law

\[
s(\xi)\sim2\sqrt{2z_g/(\mu\cos t_g)}\,\sqrt{\xi_g-\xi}.
\]

The paper derives this local law and explains why it makes an extra response bend possible. It describes how a negative residence derivative on a physical critical flight led to the rational witness. The existence proof does not assume the numerical response graph is exact.

## Project map

- [Research manuscript](paper/main.tex) — a single main theorem stated in the introduction, the residence-time mechanism, parameter selection and its exact return-map certificate.
- [Continuation of the principal proof](paper/robustness.tex) — quantitative grazing and central multiplier bounds; this is a proof subsection, **not a second main theorem**.
- [Analytic persistence certificate](proof/certify_parameter_persistence.py) — checks six signs, four grazing barriers at each shooting endpoint, and central orbit stability; **not** an independent interval-arithmetic backend.
- [Discovery record](notes_discovery.md) — how the seven-cycle example was found.
- [Interval certificate](proof/certify_seven.py) — six Poincaré displacement sign checks, first-hit and grazing barriers, central hyperbolicity.
- [Exploratory response data](paper/figures/response_data.csv) — illustration, not proof data.
- [Independent ODE cross-check](experiments/independent_ode.py) and [high-precision roots](experiments/high_precision_roots.py).
- [Separate upper-bound research](research/L7_UPPER_BOUND_PROGRAM.md) — a conditional program, not a proof of a global upper bound.

## Reproducibility

From this folder:

    python3 proof/certify_seven.py
    python3 proof/certify_parameter_persistence.py
    python3 -m unittest discover -s tests -v

Optional experiments:

    python3 -m pip install -r requirements-experiments.txt
    python3 experiments/independent_ode.py
    python3 experiments/high_precision_roots.py
    python3 experiments/plot_mechanism.py

To compile the manuscript, use TeX Live with pgfplots:

    cd paper
    pdflatex -interaction=nonstopmode -halt-on-error main.tex
    pdflatex -interaction=nonstopmode -halt-on-error main.tex

The public repository contains editable LaTeX and plot data. The PDF can be obtained by compiling the source; a compiled copy is attached in the associated ChatGPT discussion.

## Proof status

The certificate uses exact affine flights and directed Decimal interval arithmetic, including rational Taylor remainders and first-hit checks. A second independently implemented interval backend (for example Arb/FLINT) would be desirable before formal publication. Numerical response extrema are exploratory only. The explicit `1e-12` cube now controls all grazing barriers and the central multiplier, yielding a **numerically specified cube of isolated cycles**. No global bound of seven has been proved.

## Literature

- [Bravo et al., arXiv:2507.06705](https://arxiv.org/abs/2507.06705).
- [Bravo and Trinidad-Forte, arXiv:2605.05805](https://arxiv.org/abs/2605.05805).
