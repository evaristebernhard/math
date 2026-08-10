# Residual-36: the cubic-target outlet `(m,e)=(3,6)`

Date: 2026-08-09

Status: **major new reduction.** The finite case with isolated target singularities is excluded. The true remaining outlets are divisorial contraction and positive-dimensional target singular locus.

## 0. Setup

Continue `TRIANGLE_R36_GLOBAL_MAP_RESEARCH_2026-08-09.md`. In the `k=0` six-quartic map, suppose the normal image has
\[
X'=Q_0\cap C_3\subset\mathbf P^5,
\qquad
(m,e)=(3,6).
\]
On
\[
Y=\operatorname{Bl}_A\mathbf P^3,
\qquad |A|=28,
\qquad D=4H-\sum_{a\in A}E_a,
\]
we have
\[
\phi^*H_{X'}=D,
\qquad
K_Y=-4H+2\sum E_a,
\qquad
K_{X'}=-H_{X'}.
\]
Hence
\[
K_Y-\phi^*K_{X'}
=K_Y+D
=\sum_{a\in A}E_a
\]
as a divisor class.

The point of this note is that, unlike the residual-32 situation, in the **finite** cubic-target case this class identity actually determines the ramification divisor exactly.

---

## 1. Finite case: the ramification divisor is exactly the exceptional sum

Assume
\[
\phi:Y\to X'
\]
is finite and `X'` is normal. Since `X'` is a local complete intersection, it is Gorenstein, and the finite-map canonical formula gives an effective ramification divisor
\[
R_\phi=K_Y-\phi^*K_{X'}.
\]
Thus
\[
R_\phi\sim\sum_{a\in A}E_a.
\]

Intersect with `H^2`, where `H` denotes the pullback of a hyperplane from the original `P^3`. The class `sum E_a` has zero `H^2`-degree. Any effective nonexceptional prime divisor on `Y` is the strict transform of a positive-degree surface in `P^3`, so it has positive `H^2`-degree. Therefore an effective divisor linearly equivalent to `sum E_a` cannot contain any nonexceptional component.

The exceptional classes are independent in `Pic(Y)`. Hence all coefficients are forced to be one:
\[
\boxed{R_\phi=\sum_{a\in A}E_a.}\tag{C3.1}
\]

Consequences:

1. every exceptional plane is a simple ramification divisor;
2. there is no other divisorial ramification;
3. if `L_a=phi(E_a)` is the target plane, then a generic point of `L_a` receives local degree two from `E_a`;
4. in a degree-six cover, at most three exceptional planes can dominate the same target plane.

Therefore the finite case contains at least
\[
\boxed{\left\lceil\frac{28}{3}\right\rceil=10}
\]
distinct branch planes.

---

## 2. Hyperplane-section Euler contradiction when the target singularities are isolated

Assume further that `Sing(X')` is finite. Choose a general hyperplane
\[
H'\subset\mathbf P^5
\]
avoiding `Sing(X')`. Then
\[
S'=X'\cap H'
\]
is a smooth anticanonical K3 surface of degree six, so
\[
e(S')=24.
\]

Its inverse image
\[
S=\phi^{-1}(S')\in|D|
\]
is smooth for general `H'`. Downstairs in the original `P^3`, `S` is the strict transform of a general quartic surface through the 28 points of `A`. A general quartic in the six-quartic system is smooth at those points and away from them by Bertini, so `S` is the blowup of a smooth quartic K3 surface at 28 points. Hence
\[
\boxed{e(S)=24+28=52.}\tag{C3.2}
\]

Restrict the finite cover:
\[
\phi_S:S\to S'.
\]
Its degree is six. By (C3.1), the ramification divisor is the disjoint union
\[
R_{\phi_S}=\bigsqcup_{a\in A} e_a,
\qquad
 e_a=E_a\cap S\simeq\mathbf P^1.
\]
Each `e_a` maps isomorphically onto the line
\[
\ell_a=L_a\cap S'\subset S'.
\]
The ramification is simple everywhere along `e_a`, because the ramification coefficient is one and the target is smooth along the chosen section.

For a degree-six cover of smooth surfaces with simple ramification curves `e_a` mapping degree one to branch curves, constructible-function integration gives
\[
e(S)=6e(S')-\sum_a e(e_a).
\]
This remains true even when distinct branch lines meet: at an intersection point the fibre-cardinality loss is the sum of the independent simple ramification losses, and the source ramification curves are disjoint.

Therefore
\[
e(S)=6\cdot24-28\cdot2=88,
\]
contradicting (C3.2). Thus
\[
\boxed{\text{finite }(3,6)\text{ target with isolated singularities is impossible}.}\tag{C3.3}
\]

---

## 3. Divisorial contractions before the finite model

If the six-quartic map is not finite, let an irreducible divisor `S_0` be contracted to dimension at most one. Write its image in the original `P^3` as a surface of degree `d` having multiplicities `m_a` at points of `A`. Since `D|_{S_0}` has image dimension at most one,
\[
D^2\cdot S_0=0,
\]
so
\[
\boxed{\sum_{a\in A}m_a=16d.}\tag{C3.4}
\]

Because the six restricted quartics span at most a two-dimensional system, at least four independent members of `W` vanish identically on `S_0`. Hence the defining equation of `S_0` divides at least four quartics. This forces
\[
d\le3.
\]

The clean possibilities are then strongly restricted:

- `d=1`: exactly 16 points of `A` lie on a plane; this is the residual-36 analogue of the plane-16 contraction;
- `d=2`: an irreducible smooth quadric can contribute at most 28 to the multiplicity sum, and a quadric cone at most 29, both below the required `32`; thus no irreducible quadratic contraction occurs;
- `d=3`: the required multiplicity sum is 48. A normal cubic surface has too little singular multiplicity to reach this; hence any cubic survivor must be a nonnormal/singular-curve cubic and is already a low-degree degeneration outlet.

Thus the only clean divisorial contraction is again a plane containing 16 points of `A`; cubic contractions are necessarily singular low-degree degenerations.

---

## 4. What remains after the Euler contradiction

The cubic-target branch can survive only if at least one of the following occurs:

1. the six-quartic map has a divisorial contraction, whose clean model is plane-16;
2. `X'` is normal but has a positive-dimensional singular locus, so every general anticanonical K3 section is singular and the smooth-K3 Euler calculation does not apply directly;
3. the target is nonnormal.

This is a much smaller gap than an unrestricted ramification problem.

Moreover, if the singular locus of a normal target is a curve, a general hyperplane section has isolated surface singularities. Comparing the actual Euler number `52` with the smooth-branch baseline `88` shows that the singular section must account for an Euler deficit of 36. Thus a surviving positive-dimensional singular locus must be quantitatively substantial; a single mild isolated degeneration on a general section cannot repair the contradiction.

---

## 5. Relation to existing residual-36 comparison machinery

The new global route suggests a revised role for the older tools:

- J1/J2 should be reintroduced only when the target acquires positive-dimensional singularities / nonfactorial defect;
- QT/Smith analysis is naturally interpreted as controlling precisely such nonregular image degenerations;
- the clean finite isolated-singularity cubic target is already impossible by the Euler argument and needs none of the Horrocks/QT machinery.

Thus the main residual-36 difficulty is now concentrated in **degenerate target geometry**, rather than generic comparison geometry.

## 6. Current status

Combining the rank-four note and this cubic-target note, the normal clean residual-36 branch has been compressed to:
\[
\boxed{
\begin{array}{c}
(m,e)=(2,9):\ \text{clean rank-four }(1,3),(2,2)\text{ excluded};\\[1mm]
(m,e)=(3,6):\ \text{finite target with isolated singularities excluded}.
\end{array}}
\]

The remaining work is now:

- low-degree/reducible degenerations in `(2,9)`;
- plane-16 or singular-cubic divisorial contractions;
- positive-dimensional singular locus or nonnormal target in `(3,6)`.

Do not yet claim residual-36 fully closed.
