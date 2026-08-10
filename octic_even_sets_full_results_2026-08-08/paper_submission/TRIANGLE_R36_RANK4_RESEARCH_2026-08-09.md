# Residual-36: rank-four quadratic-complex outlet

Date: 2026-08-09

Status: **new clean-case exclusions; paper-level audit still required before promotion.**

## 0. Setup

Continue the global-map reduction from `TRIANGLE_R36_GLOBAL_MAP_RESEARCH_2026-08-09.md`. In the normal quadratic-complex outlet
\[
(m,e)=(2,9),
\qquad
X'=Q_0\cap Q_1\subset\mathbf P^5,
\]
we have a rank-four pencil member. After a linear change of coordinates in the six-dimensional quartic space `W`, write the corresponding quadratic relation as
\[
f_1f_2=f_3f_4.
\]
Unique factorization gives
\[
f_1=ab,\qquad f_3=ac,\qquad f_2=cd,\qquad f_4=bd,
\]
with
\[
\deg a=\deg d=\alpha,
\qquad
\deg b=\deg c=\beta,
\qquad
\alpha+\beta=4.
\]
The only nontrivial clean types are
\[
(\alpha,\beta)=(1,3)\quad\text{or}\quad(2,2).
\]
Let `r,s` denote the two radical quartic coordinates. The common 28-point block `A` is contained in
\[
V(f_1,f_2,f_3,f_4,r,s).
\]
Every point of `A` is a transverse `CI(4,4,4)` point for either determinant net, so the six first jets have rank at least three there.

---

## 1. Clean (1,3) type is impossible

Assume
\[
\deg a=\deg d=1,
\qquad
\deg b=\deg c=3.
\]
Then
\[
C:=V(b,c)
\]
is a degree-nine `CI(3,3)` curve in the clean case.

On `C`, the first four quartic coordinates vanish identically. The second independent quadratic relation defining the quadratic complex therefore restricts to a nonzero binary quadratic relation in the two radical coordinates `r,s`. On every irreducible component on which `(r,s)` is not identically zero, the image in the radical line is finite; in the clean connected/irreducible case this forces `[r:s]` to be constant. After replacing the radical basis, one may assume
\[
r|_C=0.
\]
Then the base points of the six-quartic system on `C` are precisely the zeros of `s|_C`. Since `s` is quartic,
\[
\deg \mathcal O_C(4)=4\deg C=36.
\]
Thus a nonzero `s|_C` cuts a zero divisor of length 36, whereas the entire common block has only 28 points. If `s|_C=0` as well, the six-quartic system has the positive-dimensional base curve `C`, impossible.

Therefore the clean irreducible `(1,3)` type cannot occur:
\[
\boxed{(1,3)\text{ clean rank-four outlet is impossible}.}
\]
Any reducible/nonreduced `CI(3,3)` degeneration has a component of degree at most three and must be returned to the low-degree carrier analysis rather than treated as a new rank-four outlet.

---

## 2. Clean (2,2) type is impossible by 16+16 versus 28

Assume
\[
\deg a=\deg b=\deg c=\deg d=2.
\]
The common zero locus of the four non-radical quartics is
\[
C_1\cup C_2,
\qquad
C_1=V(a,d),
\qquad
C_2=V(b,c),
\]
where each `C_i` is a degree-four `CI(2,2)` curve in the clean case.

### 2.1 Each carrier contributes a full length-16 base divisor

Restrict the second quadratic relation to `C_1`. The first four coordinates vanish there, so again the radical coordinates satisfy a binary quadratic relation. In the clean connected case, after a radical basis change one radical quartic vanishes identically on `C_1`; the other therefore cuts the complete base divisor on `C_1`. Its degree is
\[
\deg\mathcal O_{C_1}(4)=4\cdot4=16.
\]
Hence the six-quartic system has a length-16 base divisor `A_1` on `C_1`. Similarly it has a length-16 base divisor `A_2` on `C_2`:
\[
|A_1|=|A_2|=16.
\]

### 2.2 The two length-16 divisors cannot overlap

Suppose
\[
p\in A_1\cap A_2.
\]
Then
\[
a(p)=d(p)=b(p)=c(p)=0.
\]
Consequently each of
\[
ab,\ ac,\ dc,\ db
\]
has zero first derivative at `p`, because every differential contains one of the four vanishing quadratic factors. Thus among the six quartic sections only the two radical coordinates can contribute nonzero first jets. The first-jet rank of `W` at `p` is therefore at most two.

But `p\in A` is a transverse common block point for a `CI(4,4,4)` determinant net. On the exceptional plane over `p`, the corresponding three quartic first jets must be linearly independent. Hence the first-jet rank must be at least three. Contradiction.

Therefore
\[
A_1\cap A_2=\varnothing.
\]
It follows that the common base block contains at least
\[
|A_1|+|A_2|=32
\]
points, contradicting
\[
|A|=28.
\]
Hence
\[
\boxed{(2,2)\text{ clean rank-four outlet is impossible}.}
\]

This is the key distinction from residual-32: there the `16+16` saturation exactly matches `|A|=32` and produces the desmic-type survivor; here the same geometry overshoots the common block by four points and is impossible.

---

## 3. Consequence for the normal quadratic-complex branch

Under the clean reduced hypotheses, both rank-four types are excluded. Rank-three relations already return to a quadric factor / `CI(2,2)` low-degree carrier by the same UFD analysis used in residual-32.

Therefore the normal `(m,e)=(2,9)` quadratic-complex branch has no clean finite rank-three/rank-four outlet. Any survivor must lie in one of the following degenerations:

1. reducible/nonreduced `CI(3,3)` or `CI(2,2)` carriers;
2. common components among `a,b,c,d`;
3. a positive-dimensional family of maximal planes;
4. a nonnormal quadratic-complex target.

The first three are expected to return to already studied plane/quadric/cubic carrier geometry; this return still requires a concise audit before one can declare the entire `(2,9)` branch closed.

---

## 4. Current implication for residual-36

Combining with the global-map note, residual-36 is now reduced, in the normal-target setup, to
\[
\boxed{(m,e)=(3,6)}
\]
plus low-degree/nonnormal degenerations from the `(2,9)` branch.

The next priority is therefore the cubic-target equality problem:
\[
X'=Q_0\cap C_3,\qquad e=6,\qquad R_{D^2}=28.
\]
One should prove the actual divisorial ramification structure by local differential methods rather than by reading coefficients from a divisor-class identity.
