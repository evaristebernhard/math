# Residual-32 triangle: complete closure of the k=1 case by transversality

Date: 2026-08-09

Status: **paper-level candidate; short independent proof.**

## Setup

Let
\[
Z_{AB}=A\sqcup B,\qquad Z_{AC}=A\sqcup C,
\qquad |A|=|B|=|C|=32,
\]
be two of the three reduced transverse \(CI(4,4,4)\) determinant sets in the residual-32 triangle, with determinant nets \(U,V\subset S_4\). Assume
\[
k=\dim(U\cap V)=1,
\qquad U\cap V=\langle q\rangle.
\]
The common-pencil argument already gives \(k\le1\), so this is the only nonzero-intersection case.

The difference of the two determinant quadrics on \(W=U+V\), \(\dim W=5\), has rank at most four because every exceptional plane over \(A\) maps to a plane contained in its zero quadric and a smooth quadric threefold contains no plane.

We treat all three isotropy types below, including the degenerations that were previously hidden behind a clean-factorization assumption.

## 1. Both non-isotropic

After completing squares, write
\[
F=\lambda q^2+u_1u_2=\mu q^2+v_1v_2.
\]
If \(\lambda\ne\mu\), the difference relation has rank five on the five-dimensional space \(W\), contradicting the rank-at-most-four bound. Hence \(\lambda=\mu\) and
\[
u_1u_2=v_1v_2.
\]
Since each determinant net has zero-dimensional base locus, \(u_1,u_2\) and \(v_1,v_2\) have no common curve factor. Unique factorization therefore gives
\[
u_1=ab,\qquad u_2=cd,\qquad v_1=ac,\qquad v_2=bd,
\]
with
\[
\deg a=\deg d=\alpha,\qquad
\deg b=\deg c=\beta,\qquad
\alpha+\beta=4.
\]
The common block is set-theoretically
\[
A=V(q,a,d)\cup V(q,b,c).
\]
If a point lay in both pieces, then \(a=b=c=d=0\), so the first jets of all four product quartics \(ab,cd,ac,bd\) would vanish. Either determinant net would then have first-jet rank at most one after adjoining \(q\), contradicting transversality. Thus the two pieces are disjoint.

At a point of \(V(q,a,d)\), transversality forces \(b,c\ne0\) and the first jets of \(q,a,d\) to be independent; hence this complete intersection is reduced of length \(4\alpha^2\). Similarly \(V(q,b,c)\) is reduced of length \(4\beta^2\). Therefore
\[
32=|A|\ge4(\alpha^2+\beta^2).
\]
For \(\alpha+\beta=4\) with \(\alpha,\beta>0\), the minimum is \(32\), attained only at \(\alpha=\beta=2\); the types \((1,3)\) and \((3,1)\) would already give \(40>32\).

Thus \(a,b,c,d\) are quadrics and
\[
F=\lambda q^2+abcd.
\]
Here \(\lambda\ne0\): otherwise \(F=abcd\) would be singular along positive-dimensional pairwise intersections of its factors, contrary to the nodal hypothesis. On each of the quadrics \(a=0,b=0,c=0,d=0\), the octic restricts to the square \(\lambda q^2\). If any of these quadrics is reduced, it is a reduced contact quadric and yields a strict weight-48 even set, contradicting minimum weight 64. Hence all four quadrics would have to be double planes. If two underlying planes are distinct, their weak weight-28 even sets have a nonzero strict symmetric difference of weight at most 56, again impossible. Thus all four double planes have the same underlying plane, which makes the four product quartics proportional and collapses the determinant nets. Contradiction.

Hence the both-non-isotropic case is impossible.

## 2. Mixed isotropic/non-isotropic

One determinant form can be written as
\[
qu+v^2,
\]
and the other as
\[
\lambda q^2+xy.
\]
Their difference is a rank-five quadratic form on \(W\), contradicting the rank-at-most-four bound. Hence the mixed case is impossible.

## 3. Both-isotropic normal form

Choose bases so that
\[
U=\langle q,u,v\rangle,
\qquad
V=\langle q,u',v'\rangle,
\]
and
\[
F=qu+v^2=qu'+(v')^2.
\]
Thus
\[
(v-v')(v+v')=q(u'-u). \tag{K1.1}
\]
Moreover
\[
Z_{AB}=V(q,u,v)
\]
is a reduced transverse complete intersection. In particular at every point of this scheme the first jets of \(q,u,v\) are linearly independent.

## Lemma 1: q is squarefree

Suppose an irreducible factor \(r\) occurs in \(q\) with multiplicity at least two. Write \(q=r^2s\). On the surface \(R=(r=0)\) one has
\[
q=0,\qquad dq=0.
\]
The two quartics \(u|_R,v|_R\) have a common zero. Indeed, if they have a common curve then the base locus \(V(q,u,v)\) is positive-dimensional, impossible; otherwise their intersection number on the positive-degree projective surface \(R\) is positive, so a zero exists.

At such a point
\[
q=u=v=0,\qquad dq=0,
\]
so the first jets of \(q,u,v\) have rank at most two, contradicting transversality. Therefore
\[
\boxed{q\text{ is squarefree}.}
\]

## Lemma 2: no irreducible factor of q divides both v-v' and v+v'

Let \(r\mid q\) be irreducible. If
\[
r\mid(v-v'),\qquad r\mid(v+v'),
\]
then \(r\mid v\) and \(r\mid v'\). On the surface \(r=0\), the equations \(q=v=0\) hold identically. Hence \(u=0\) cuts a positive-dimensional curve contained in \(V(q,u,v)\), contradicting that the determinant base locus is zero-dimensional.

Thus each irreducible factor of the squarefree quartic \(q\) divides exactly one of \(v-v'\) and \(v+v'\).

## Lemma 3: a split assignment contradicts transversality

By (K1.1), every irreducible factor of \(q\) divides one of the two factors \(v-v'\), \(v+v'\). Suppose factors occur on both sides. Since \(q\) is squarefree, write
\[
q=rs,
\qquad \gcd(r,s)=1,
\]
with \(r,s\) nonconstant and
\[
r\mid(v-v'),\qquad s\mid(v+v').
\]
On the complete-intersection curve
\[
\Gamma=V(r,s)
\]
one has
\[
v-v'=v+v'=0,
\]
hence
\[
v=v'=0.
\]
Also \(q=rs\), so
\[
dq=s\,dr+r\,ds=0
\qquad\text{on }\Gamma.
\]

The quartic \(u|_\Gamma\) must vanish somewhere: if it vanishes identically on a component then the determinant base locus contains a curve; otherwise its divisor on the positive-degree projective curve \(\Gamma\) has positive degree. Choose \(p\in\Gamma\) with \(u(p)=0\). Then
\[
q(p)=u(p)=v(p)=0,
\qquad dq(p)=0,
\]
again contradicting transversality of \(V(q,u,v)\).

Therefore all irreducible factors of \(q\) must divide the same one of \(v-v'\), \(v+v'\).

## Lemma 4: same-side assignment makes the two nets equal

Since \(q\) is squarefree of degree four, if all its irreducible factors divide, say, \(v-v'\), then
\[
v-v'=c q
\]
for some constant \(c\). Equation (K1.1) gives
\[
u'-u=c(v+v').
\]
Consequently
\[
v'\in\langle q,v\rangle,
\qquad
u'\in\langle q,u,v\rangle,
\]
so \(V\subseteq U\). Since both nets have dimension three,
\[
U=V,
\]
contradicting the residual-triangle setup. The case \(q\mid(v+v')\) is identical.

## Theorem

The case
\[
\dim(U\cap V)=1
\]
 cannot occur in the residual-32 triangle. Hence, together with the common-pencil bound,
\[
\boxed{U\cap V=0.}
\]

The proof does not use the weak-even weight classification, a contact-plane/cubic case split, or a Hilbert-defect enumeration. The previous plane--cubic outlet arose only because the reducible quartic factorization was stopped too early; transversality of the determinant complete intersection closes it directly.

## Paper implication

The residual-32 branch is now genuinely reduced to the single
\[
\boxed{k=0}
\]
six-quartic comparison. Abstract/Introduction/Remaining-outlets language may safely be upgraded from “k=1 reduction” to “k=1 exclusion” after one final formal proof audit.
