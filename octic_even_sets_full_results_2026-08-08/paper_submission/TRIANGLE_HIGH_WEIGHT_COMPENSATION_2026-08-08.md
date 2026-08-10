# Residual-32 triangle: high-weight compensation route

Date: 2026-08-08

## 1. Correct target

The weights 88,96,104,112 cannot be globally forbidden for strict even sets on octic surfaces.  The earlier attempt to read such a prohibition from Endraß, Cor. 1.11, was a table-column error: the degree-8 strict gap is weight 56, while 88,96,104,112 occur in the degree-10 column.  Moreover, the known degree-8 existence range includes strict even sets of these weights.

Therefore the viable target is not

\[
A_{88}=A_{96}=A_{104}=A_{112}=0
\]

for every octic.  The correct problem is to exploit the *residual-triangle environment* and the high-node/minimum-64 hypotheses.

## 2. Full split state space

Let

\[
H=\langle c_1,c_2\rangle,
\qquad
\operatorname{wt}(c_1)=\operatorname{wt}(c_2)=\operatorname{wt}(c_1+c_2)=64.
\]

The four coordinate blocks have sizes

\[
(73,32,32,32).
\]

Using the complete allowed weight set

\[
\{0,64,72,80,88,96,104,112,120,128,136,144,152,160,168\},
\]

inverting the four orbit-weight equations and quotienting by translation by H leaves exactly 1594 nonzero H-coset split states.

The old 122-state certificate is recovered only after deleting 88,96,104,112 and remains a correct *conditional* certificate.

## 3. New unconditional exact coding theorems

All the following use the complete weight set and exact integer split-MacWilliams certificates of total split degree at most 8.

### Theorem A: total high-weight compensation

If a residual-32 triangle exists, then

\[
\boxed{A_{88}+A_{96}\ge65.}
\]

The exact dual lower bound before integrality is

\[
\frac{640241160775953104}{10^{16}}
=64.0241160775953104\ldots.
\]

Verifier:

`paper_submission/scripts/verify_triangle_A88_A96_abundance.py`.

### Theorem B: weighted compensation

One also has

\[
\boxed{A_{88}+3A_{96}\ge185.}
\]

The exact rational lower bound is

\[
\frac{184184146429569024}{10^{15}}
=184.184146429569024\ldots.
\]

Consequently

\[
\boxed{\max\{A_{88},A_{96}\}\ge47}
\]

and, in a form useful for geometry,

\[
\boxed{A_{96}\ge41\quad\text{or}\quad A_{88}\ge65.}
\]

Verifier:

`paper_submission/scripts/verify_triangle_A88_3A96_abundance.py`.

### Theorem C: mixed-coset / abundance dichotomy

Call a nonzero H-coset *mixed* if its four orbit words include both a weight-64 word and a word of weight 88 or 96.  Then

\[
\boxed{
\text{mixed H-coset exists}
\quad\text{or}\quad
A_{88}+A_{96}\ge471.
}
\]

Indeed, after removing only the 199 mixed split states, 1395 states remain; the exact dual lower bound is

\[
\frac{470440954987064448}{10^{15}}
=470.440954987064448\ldots.
\]

Verifier:

`paper_submission/scripts/verify_triangle_mixed_or_471.py`.

This theorem is important because it gives two qualitatively different geometric targets:

1. a **small 3-dimensional code configuration** \(\langle H,x\rangle\) containing the triangle, an additional weight-64 word, and a weight-88/96 word; or
2. an **extreme abundance branch** with at least 471 high-weight strict even sets.

## 4. Weight-88 contact-sextic lemma

Let W be a strict even set of weight 88 on an octic surface, let \(\widetilde X\) be the resolution, let H be the pullback of a hyperplane, and write

\[
2L=\sum_{p\in W}E_p.
\]

Then

\[
H^2=8,
\qquad K_{\widetilde X}=4H,
\qquad L^2=-44,
\qquad H\cdot L=0,
\qquad \chi(\mathcal O_{\widetilde X})=36.
\]

Riemann--Roch gives

\[
\chi(3H-L)
=36+\frac12(3H-L)(-H-L)
=2.
\]

In the minimum-64 branch, \(H^0(H-L)=0\): a nonzero section would produce a degree-2 contact surface cutting the strict even set, which is the weight-48 contact-quadric situation and is incompatible with weight 88.

Serre duality gives

\[
H^2(3H-L)^\vee\cong H^0(H+L).
\]

For an effective divisor in \(|H+L|\), its intersection with every exceptional curve belonging to W is negative; hence every such exceptional curve is fixed.  Subtracting the complete exceptional divisor \(2L\) identifies the effective system with \(|H-L|\).  Thus

\[
h^0(H+L)=h^0(H-L)=0,
\]

so

\[
h^2(3H-L)=0.
\]

Therefore

\[
\boxed{h^0(3H-L)-h^1(3H-L)=2}
\]

and in particular

\[
\boxed{h^0(3H-L)\ge2.}
\]

Thus every weight-88 strict even set in the minimum-64 octic environment carries at least a pencil of sextic contact surfaces.

This is a structural lemma, not a contradiction: weight-88 strict even sets exist on some octics.

## 5. Weight-96 comparison

For weight 96 the same Riemann--Roch calculation gives

\[
\chi(3H-L)=0,
\qquad
\chi(2H-L)=-4.
\]

Hence there is no automatic sextic-pencil lower bound analogous to weight 88.  Weight 96 should therefore be attacked through its residual/split configuration rather than by trying to clone the weight-88 argument.

A particularly rigid mixed state is

\[
(64,64,64,96).
\]

Adjoining such a coset representative to H gives a three-dimensional subcode with six weight-64 words and one weight-96 word.  Relative to the weight-96 word, the residual code has parameters

\[
[73,18],\qquad d=16,
\]

and contains a residual triangle of three weight-16 words with four split blocks

\[
(49,8,8,8).
\]

A degree-8 split-MacWilliams LP on this second residual remains feasible, so this residual alone does not close the configuration.  The extra lift data / simultaneous six determinant presentations must be used.

## 6. Recommended next attack

The most efficient route is now:

### Branch M: mixed coset

Classify the mixed 3-dimensional subcodes \(\langle H,x\rangle\) up to the full affine automorphism group of H.  There are only 51 unordered orbit-weight multisets containing both 64 and 88/96.  The key subfamilies are those with multiple new 64-words, because each new minimum word supplies an additional reduced transverse \(CI(4,4,4)\) determinant presentation of the same octic.

Try to prove that every mixed pattern forces one of:

- a fourth determinant presentation incompatible with the k=0 low-rank pencil;
- a relative Smith/contact divisor of degree 1 or 2;
- the special \((64,64,64,88)\) or \((64,64,64,96)\) configurations, which can be attacked separately.

### Branch A: no mixed coset

Then \(A_{88}+A_{96}\ge471\).  Combine the weighted certificate with this large abundance and use:

- weight-88 sextic contact pencils;
- incidence among 88/96 supports;
- the 533 weight-64 determinant presentations;
- finite-dimensional bounds on common fixed contact carriers / Smith components.

This branch should be much more rigid than the mere existence of a single high-weight word.

## 7. Current conclusion

The attempt to globally delete 88,96,104,112 is impossible.  Nevertheless the failed 122-state certificate has led to a stronger and correct replacement: a residual triangle can survive the full allowed weight spectrum only by producing a large, explicitly certified population of weights 88 and 96, with an additional mixed-coset/abundance dichotomy.

The residual-32 problem is therefore no longer simply “the four forbidden weights are missing”.  Its new coding-geometric interface is

\[
\boxed{
\text{triangle}
\Longrightarrow
\begin{cases}
\text{small mixed 3D configuration},\\
\text{or at least 471 high-weight even sets}.
\end{cases}}
\]

This is the recommended route for the next closure attempt.
