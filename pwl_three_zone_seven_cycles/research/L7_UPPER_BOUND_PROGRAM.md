# Toward a sharp upper bound of seven: a new discriminant target

**Status (2026-10-10): conditional reduction + high-precision experiments, NOT a proof of $L^*\le7$.**

This note continues `pwl_three_zone_8216_bound/main.tex` and the seven-cycle
construction in `pwl_three_zone_seven_cycles/paper/main.tex`.

## 1. Verified mathematical facts and why seven would follow

Use the original equation

\[
 x'=-Ax+(A+B)\operatorname{sat}(x)+\mu\sin t,\qquad A,B,\mu>0.
\]

Let $\Lambda(\xi,\mu)$ be the biased periodic response parametrized by its
mean $\xi$, and let $T$ denote total time with $|x|<1$. The existing
manuscript proves

\[
\Lambda_\xi J=(A+B)(\rho-T),\quad J>0,\quad
\rho=\frac{2\pi A}{A+B},\quad T_\mu<0\quad\text{at genuine three-zone critical fibres}.
\]

For fixed $\mu$, if the *positive-mean genuine three-zone family* contains at
most two isolated solutions of $T=\rho$ (counting grazing limits
appropriately), then the two-zone tail has at most one more critical fibre,
and the one-zone tail has none. Since $\Lambda(0,\mu)=0$, each isolated
positive zero of $\Lambda$ requires a preceding distinct critical point.
Consequently at most three positive isolated periodic solutions occur; odd
symmetry gives $L\le2\cdot3+1=7$.

The seven-cycle certificate provides the complementary bound $L^*\ge7$,
subject to independent auditing of the directed-rounding implementation.

**Global missing ingredient:** show that the genuine positive critical graph
is connected and every amplitude slice meets it at most twice, including
multiple intersections and grazing endpoints. A sufficient but unproved
property is that each stationary point of $\mu_s(\xi)$ is a strict minimum.
The earlier manuscript's **no-valley** condition for a five-cycle bound is
numerically disproved and should not be used.

## 2. An exact easy parameter regime: $\mu\le B$ gives precisely three cycles

At $x=1$ the vector field has value $B+\mu\sin t\ge0$, while at $x=-1$
it is $-B+\mu\sin t\le0$. Thus the upper/lower half-lines are forward
invariant and no periodic orbit can cross a switching line.

There are exactly three periodic solutions, one in each affine region:

\[
 x_0(t)=\frac{\mu}{1+B^2}(-B\sin t-\cos t),
\]

\[
 x_\pm(t)=\pm\left(1+\frac BA\right)
          +\frac{\mu}{1+A^2}(A\sin t-\cos t).
\]

Indeed, $\|x_0\|_\infty=\mu/\sqrt{1+B^2}<1$ and the outer
harmonic amplitudes obey $\mu/\sqrt{1+A^2}\le B/\sqrt{1+A^2}<B/A$.
The corresponding multipliers are $e^{2\pi B}$ at the center and
$e^{-2\pi A}$ in either outer zone. Therefore **$L(A,B,\mu)=3$ for
$0<\mu\le B$**, including the endpoint $\mu=B$. The interesting global
parameter region is $\mu>B$.

## 3. Algebraic-exponential reduction of a fold to two equations

On a genuine three-zone *critical* fibre, write the four flight durations
$(r,s,u,v)$ as in the original toric paper. Criticality forces

\[
 u=\rho-r,\qquad v=2\pi-\rho-s.
\]

Its Cramer matching quantities $Z_1,Z_2,Z_3,Z_4,d_2,d_3,d_4$ depend
explicitly on $(A,B,r,s)$. Define

\[
 U=Z_1-Z_3,\quad V=Z_1-Z_4,\quad Q=Z_1-Z_2,\quad
 [X,Y]=\operatorname{Im}(X\overline{Y}),\quad\Delta=[U,V].
\]

The compatible physical four-flight data satisfy

\[
\boxed{F:=d_2\Delta-d_3[Q,V]+d_4[Q,U]=0.}
\]

The recovered forcing phase is

\[
 W=\mu e^{it_1}=\frac{d_3\overline V-d_4\overline U}{\Delta},
 \quad
 \boxed{M:=\mu^2=\frac{|d_3V-d_4U|^2}{\Delta^2}.}
\]

On any **regular** curve $F(r,s)=0$ with $\nabla F\neq0$, let

\[
 w=(F_s,-F_r),\qquad
 K:=w\cdot\nabla M=M_rF_s-M_sF_r.
\]

A stationary point of $M$, hence of $\mu>0$, along $F=0$ obeys

\[
\boxed{F=K=0.}
\]

This replaces direct differentiation of all four crossing times by a
**two-equation discriminant problem**. The converse identification with a
stationary point of $\mu_s(\xi)$ assumes the physical parametrization of the
critical graph remains regular. The sign of the curvature is computable
without reconstructing $\xi$.

At $K=0$, $\nabla M=\tau\nabla F$, where
$\tau=(\nabla M\cdot\nabla F)/\|\nabla F\|^2$. Set

\[
\boxed{\mathscr C:=w^\top(\nabla^2M-\tau\nabla^2 F)w.}
\]

In the chart $F_s\ne0$, so $s'(r)=-F_r/F_s$, differentiation gives

\[
 \frac{d^2\mu}{dr^2}=\frac{\mathscr C}{2\mu F_s^2}
 =\frac{K_rF_s-K_sF_r}{2\mu F_s^2}
 \quad\text{when }F=K=0.
\]

Thus the **new precise candidate inequality** is

\[
\boxed{F=K=0,\ \text{positive-mean real first-hit physical fibre}
 \quad\Longrightarrow\quad \mathscr C>0\,?}
\]

It is the correct mathematical replacement for the previously false
claim $T_\xi>0$ on every three-zone critical fibre. A proof of this
inequality, *combined with global connectedness and endpoint control*,
would give a seven-cycle upper bound. No such global proof is known here.

The form using $\mathscr C$ is intrinsically valid even where $F_s=0$;
using $r$ as a global parameter is **not** justified.

## 4. Independent numerical fold checks (mpmath, 38 digits)

`research/discriminant_scan.py` reconstructs $F,M$, differentiates at high
precision, solves $F=K=0$, and verifies that the four sampled flight interiors
stay within their assigned zones. The approximate results are:

| A | B | r | s | forcing at valley $\mu$ | mean $\xi$ | $d^2\mu/dr^2$ |
|---:|---:|---:|---:|---:|---:|---:|
| 9 | 1.5 | 2.855275285135 | 0.254993055043 | 1.813583979091 | 0.019152895531 | +0.02166200517 |
| 8 | 1.5 | 2.720158486462 | 0.408262148486 | 1.816399848698 | 0.009624369606 | +0.00230567291 |
| 9 | 4 | 2.933255928878 | 0.137450537562 | 4.145367096512 | 0.222044217964 | +0.39660900414 |
| 16 | 3 | 3.071995421432 | 0.011012103723 | 3.166167593904 | 0.048477915527 | +1.21794549718 |

These are **local numerical minima**, not certified global uniqueness. At
$A=16,B=3$ the valley lies very near the vanishing lower flight $s=0$;
a coarse uniform mesh missed it. Across an exploratory grid of 165 slope
pairs, no verified local *maximum* was found, but this is not evidence of
absence: roots can escape meshes, and algebraic matching roots still need
first-hit checks and proper continuation.

### Critical warning: one $r$ can have multiple compatible $s$

For slope pairs such as $A=0.2,B=3$, numerical matching produced two
candidate $s$ roots for a single $r$. Some have strongly distinct
amplitudes. Consequently the representation $s=s(r)$ need not be global,
and a rigorous proof must use multiple regular charts or a more intrinsic
parameter (e.g. the mean coordinate). Local curvature positivity **alone**
will not prove $L\le7$ if there are separate critical components.

## 5. Recommended next proof effort

1. Derive a sign factorization for $\mathscr C$ on $F=K=0$ using the
   cyclic-order/positivity of weighted Fourier arc centroids $Z_j$.
2. Establish connectedness of the **physical**, positive-mean critical
   locus, and classify the two endpoint types (symmetric center and
   lower-zone grazing); avoid assuming $F_s\ne0$ globally.
3. Search for negative $\mathscr C$ on all feasible branches, especially
   $A/B\ll1$, near $s\to0$, and $A,B\to\infty$ with different ratios.
4. Audit degeneracies $\mathscr C=0$ and possible higher-order stationary
   points, and then extend the zero-count argument through grazing.

**Important:** The original paper `pwl_three_zone_8216_bound/main.tex`
still refers to a conjectural sharp value five. This is outdated given the
seven-cycle computer-assisted construction and should be revised before
publication once the independent audit is complete.