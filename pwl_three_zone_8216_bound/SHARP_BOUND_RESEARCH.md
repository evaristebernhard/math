> **SUPERSEDED BY THE SEVEN-CYCLE CONSTRUCTION (2026-10-10).** This historical ledger attempts to prove the now numerically contradicted (L^*\le5) conjecture. See [seven-cycle project](../pwl_three_zone_seven_cycles/) and its [new (L^*\le7) research program](../pwl_three_zone_seven_cycles/research/L7_UPPER_BOUND_PROGRAM.md). Do not use the no-valley target below as a valid global hypothesis.

# \(L^*\le 5\) sharp-bound research ledger

Status: **[GAP]**.  This file is deliberately separate from the proved
\(L^*\le16437\) manuscript.

The lower bound \(L^*\ge5\) is supplied by the perturbative construction in
Bravo--Carmona--Fernández--Ojeda,
[arXiv:2507.06705](https://arxiv.org/abs/2507.06705).  Thus the remaining sharp
problem is the upper bound.

## 1. What is already closed

For the mean-parametrized biased family

\[
u'+g(u)=\mu\sin t+\Lambda(\xi,\mu),\qquad
\frac1{2\pi}\int_0^{2\pi}u\,dt=\xi ,
\]

the manuscript proves

\[
z=\partial_\xi u>0,\qquad
\Lambda_\xi J=(A+B)(\rho-T),\qquad
\rho=\frac{2\pi A}{A+B},\quad J=\int_0^{2\pi}z^{-1}\,dt.
\]

It also proves, on the genuine three-zone critical set \(T=\rho\),

\[
T_\mu<0,\qquad
\mu_s'(\xi)=-\frac{T_\xi}{T_\mu},\qquad
\Lambda_{\xi\xi}=-\frac{(A+B)T_\xi}{J}.
\]

The new grazing audit in main.tex closes the independent theorem

\[
\boxed{\text{no positive genuine three-zone fibre}\Longrightarrow L\le3}.
\]

Therefore

\[
\boxed{L\ge5\Longrightarrow\text{genuine three-zone dynamics occurs}.}
\]

This reduction does not use the number \(8216\).

## 2. A smaller sharp obstruction: exclude a valley of the singular graph

The sharp problem does not require a complete oscillation classification of
every matching function.  For regular fibres, a more focused sufficient target
is

\[
\boxed{\mu_s\text{ has no local minimum on the positive genuine
three-zone critical graph}.}\tag{NV}
\]

Here is the zero-count mechanism.  Suppose a fixed horizontal slice
\(\mu=\mu_0\) has at least three positive simple zeros of
\(\Lambda(\cdot,\mu_0)\).  Reading the signs between consecutive zeros, and
using \(\Lambda(0,\mu_0)=0\), forces somewhere on the positive axis a strict
local minimum of \(\Lambda\) followed by a strict local maximum.  The
right-two-zone/upper-one-zone tail has at most one critical point and that point
is a minimum.  Hence both the earlier minimum and the later maximum must lie on
the genuine three-zone interval.

At those two critical fibres,

\[
\begin{array}{c|c|c}
 &\operatorname{sgn}\Lambda_{\xi\xi}
 &\operatorname{sgn}\mu_s'\\ \hline
\text{local minimum of }\Lambda & +&-\\
\text{local maximum of }\Lambda & -&+
\end{array}
\]

because \(T_\mu<0\).  Both points lie on the same horizontal level
\(\mu_s=\mu_0\).  The singular graph therefore decreases below that level and
later returns to it with positive slope, so it has an intervening local
minimum.  Consequently,

\[
\boxed{\text{three positive simple zeros}\Longrightarrow
\text{a local minimum of }\mu_s.}\tag{O}
\]

Thus (NV) implies at most two positive simple zeros, and odd symmetry then gives
\(L\le5\) in the regular case.

This is narrower than a full “one-turning theorem.”  It is enough to rule out
the turning type

\[
\mu_s':\quad -\longrightarrow +.
\]

A monotone graph is allowed, and a single cap
\(+\to-\) is also allowed.

## 3. Exact cusp sign to prove

At a turning point of the singular graph,

\[
T=\rho,\qquad T_\xi=0.
\]

Differentiating along \(T(\xi,\mu_s(\xi))=\rho\) and using
\(\mu_s'=0\) gives

\[
\mu_s''=-\frac{T_{\xi\xi}}{T_\mu},
\qquad
\operatorname{sgn}\mu_s''=\operatorname{sgn}T_{\xi\xi},
\]

whereas differentiating the residence identity at fixed \(\mu\) gives

\[
\Lambda_{\xi\xi\xi}
=-\frac{(A+B)T_{\xi\xi}}{J}.
\]

Hence a forbidden valley is exactly

\[
\boxed{
\mu_s''>0
\iff T_{\xi\xi}>0
\iff \Lambda_{\xi\xi\xi}<0
}\qquad(T=\rho,\ T_\xi=0).
\]

A direct sharp theorem can therefore be targeted as the cusp inequality

\[
\boxed{T_{\xi\xi}\le0\quad\text{whenever }T=\rho,\ T_\xi=0.}\tag{C}
\]

Strict \(<0\) would say that every turning is a cap.  Equality would require a
higher-order audit but would still exclude a strict valley if the first
nonzero higher derivative has the correct parity and sign.

## 4. Crossing-speed primitive

Let

\[
q=\frac{u'}{z}
\]

and let \(t_1<t_2<t_3<t_4<t_1+2\pi\) be the four genuine three-zone
crossings used in the manuscript.  From

\[
t_{i,\xi}=-\frac{z(t_i)}{u'(t_i)}=-\frac1{q_i}
\]

one obtains the exact formula

\[
\boxed{
T_\xi=
\frac1{q_1}-\frac1{q_2}
+\frac1{q_3}-\frac1{q_4}.
}\tag{D}
\]

Therefore (NV) is equivalent to proving that, along the critical graph, the
quantity in (D) cannot change sign from negative to positive.  At a simple
zero of (D), condition (C) says that its derivative along the singular graph is
negative.

This is the shortest current proof target: it involves only the four crossing
speeds, not the full Laurent support system.

## 5. Boundary anchors

At a symmetric central genuine three-zone critical fibre, half-period symmetry
gives

\[
r=u=\frac{\rho}{2}=\frac{\pi A}{A+B},\qquad
s=v=\pi-\frac{\rho}{2}=\frac{\pi B}{A+B}.
\]

At the other end of the positive genuine branch, the lower outer flight
collapses and the orbit enters the right two-zone tail.  The tail residence
time is strictly decreasing, so its only possible critical point is a minimum.
Any global proof of (C) should be checked against both anchors; a sign argument
valid only away from the collapsed flight is not yet enough.

## 6. Remaining proof obligations

1. **Global graph topology.** Upgrade the local graph furnished by
   \(T_\mu<0\) to the needed connected positive critical graph, including its
   central and lower-grazing endpoints.
2. **No-valley inequality.** Prove (C), or directly prove that (D) cannot
   undergo a \(-\to+\) crossing.  The crossing-map/Schwarzian formulas are the
   most plausible route; local convexity alone does not determine this global
   sign.
3. **Degenerate slices.** Extend obstruction (O) from simple zeros to isolated
   multiple zeros by a two-sided regular-level argument.
4. **Grazing parity.** Verify that a critical point converging to the collapsed
   lower flight cannot create the forbidden minimum--maximum pair at the
   itinerary boundary.

Until these four items are discharged, \(L^*\le5\) remains **[GAP]** and is not
used by the manuscript.
