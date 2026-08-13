# Referee-style audit — 2026-08-13

## Verdict

The manuscript should use the **strong graph-structured theorem**, not the earlier conditional or all-loose formulation.

The audited general statement is

\[
\boxed{
N_X(k,M)\le \Theta_k\,k!(4M)^k\mathsf L_{2k},
}
\]

for a prescribed cyclic \(k\)-flight itinerary of a real scalar periodic piecewise-linear equation with constant slope on each visited region and real trigonometric forcing of Fourier degree at most \(M\ge1\).  Here

\[
C_0(N)=2^{N(N-1)/2},
\]

\[
C_j(N)=
2^{((j-1)(j-2)+(N-j)(N-j-1))/2}
(2^{j-1}+1)^{N-j},
\]

and

\[
\Theta_N=C_0(N)+\frac12\sum_{j=1}^{N}C_j(N).
\]

The Lucas factor \(\mathsf L_{2k}\) comes from the exact matching-partition-function formula for the flight--phase incidence cycle \(C_{2k}\).

## Mathematical seams audited

### [P] Flight algebraization

For \(a_j\ne0\), variation of constants gives a Laurent matching equation in \(q_j=e^{it_j}\), \(q_{j+1}\), and \(R_j=e^{a_j\tau_j}\).  The denominator \(im-a_j\) cannot vanish for real nonzero \(a_j\).  For \(a_j=0\), introducing \(T_j=\tau_j\) gives a polynomial--Laurent relation.

### [P] Support preservation, including zero slopes

Use the mixed coframe \(d\arg q_j\), \(d\log R_j\) on nonzero-slope flights, and \(dT_j\) on zero-slope flights.  Logarithmic differentiation preserves Laurent exponents; ordinary differentiation in \(T_j\) lowers its nonnegative exponent.  Hence the adopted box supersupports are preserved.

### [P] Simultaneous rigid-level regularization

For an arbitrary finite collection of nondegenerate transition roots, one can choose one arbitrarily small \(b\in\mathbb R^k\) that is simultaneously a regular value of \(Q|_{\Gamma_r}\) for every partial physical leaf \(\Gamma_r\), while preserving one continued root near every selected root.  On \(V_b=Q^{-1}(b)\), the chain \(V_b\cap\Gamma_r\) is separating.  The proof is a finite Sard argument plus the rank test on successive partial leaves.

### [P] Uniform covering

On the cyclic crossing chamber,

\[
\rho_k=
\prod_j
\left(2-\frac{q_{j+1}}{q_j}-\frac{q_j}{q_{j+1}}\right)
\frac{y_j}{(1+y_j)^2}
\]

is positive and tends to zero on every escaping sequence.  The only phase-boundary mechanism is crossing collision; the remaining noncompact directions are \(y_j\to0\) or \(y_j\to\infty\).  Clearing denominators gives a Laurent polynomial whose Newton polytope lies in the common box \(S\).

### [P] Relative Khovanskii--Rolle reduction

Running the one-dimensional Rolle argument on the regular level \(V_b\) gives

\[
N\le B_0+\frac12\sum_{j=1}^{k}B_j.
\]

Once a covering level is inserted, subsequent intersections are compact and no further boundary term appears.  Regular contact levels are chosen recursively, so no genericity of the zero contact level is assumed.

### [P] Compatible volume-form normalization

The induced volume forms on successive regular rigid levels can be chosen compatibly.  With this normalization, every relative contact function is represented by the ambient polynomial--Laurent wedge determinant itself, rather than by that determinant times an uncontrolled smooth positive factor.  This is essential for applying Newton-polytope/BKK counting to nonzero regular contact levels.

### [P] Contact-support recurrence

With

\[
S=[-2M,2M]^k_q\times[0,2]^k_y,
\]

the all-contact supports satisfy

\[
\Newt(H_r)\subseteq2^{r-1}S.
\]

If the covering equation is inserted at step \(j\), the later dilation factors obey

\[
a_r=1+\sum_{\ell<r}a_\ell
=2^{r-j-1}(2^{j-1}+1),
\qquad r>j,
\]

which gives the stated \(C_j(k)\).

### [P] Graph mixed volume

The local boxes retain the cyclic incidence graph.  Their BKK mixed volume with \(k\) copies of \(S\) is exactly

\[
\operatorname{MV}(L_1,\ldots,L_k,S^k)
=k!(4M)^k\mathsf L_{2k}.
\]

This follows from the permanent formula for axis-parallel boxes; admissible permanent terms are in bijection with matchings of \(C_{2k}\).

### [P] Degenerate isolated crossing cycles

The additive-bias perturbation used by Bravo--Trinidad-Forte changes only zero Fourier coefficients, so it preserves constant slopes and all adopted support boxes.  It reduces the isolated crossing-cycle count to the nondegenerate transition count without losing the prescribed transversal itinerary locally.

### [P] Global constant-slope corollary

Combining the fixed-itinerary theorem with the existing crossing bound \(k\le2Mn\) and the bound of \(2Mn\) crossing sequences gives the stated Hilbert-type estimate for the constant-slope subclass.  The final \(+2\) and, in the continuous case, tangency removal are inherited from the global bookkeeping of Bravo--Trinidad-Forte rather than reinterpreted as a new dynamical classification.

## Three-zone application retained

The model-specific result remains substantially sharper:

\[
N^{+}_{\mathrm{reg},3z}\le8216,
\qquad
L^*\le16437,
\]

and independently

\[
\text{no positive genuine three-zone branch}\Longrightarrow L\le3.
\]

The conjectural sharp value \(L^*=5\) is still open; the missing ingredient is a global real-oscillation/no-valley theorem for the genuine three-zone singular graph, not a missing step in the toric mixed-volume argument.

## Presentation changes made

- The title now advertises the constant-slope scalar theorem rather than presenting the manuscript as only a three-zone model paper.
- The abstract states the strong unconditional fixed-itinerary theorem.
- The Introduction explicitly presents two principal results: the general sparse theorem and the sharper three-zone application.
- Zero-slope flights are described accurately as polynomial--Laurent, not purely Laurent.
- The Discussion now treats the general theorem as a proved contribution rather than a conditional framework.
- The Bravo--Trinidad-Forte bibliography entry was corrected to arXiv primary class `math.CA` and given its arXiv DOI.
- The general theorem cites the relevant Khovanskii--Rolle and Bravo--Trinidad-Forte reduction steps explicitly.
- The literature review now covers piecewise-smooth dynamics, first-order Ambrosetti--Prodi response theory, nearby scalar Hilbert/center results, the original Pfaffian sources, sparse polynomial systems, and mixed-volume conventions.
- The active bibliography increased from 8 to 18 entries; every entry is cited, and every citation key resolves.
- Inactive duplicate material and obsolete `\iffalse` blocks were removed from `main.tex`, leaving one document body, one bibliography, and one `\end{document}`.

## Reference/build audit completed

1. A clean `latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex` rebuild completes with no undefined citations, undefined cross-references, duplicate-label warnings, or layout warnings.
2. Static audit of `main.tex` together with `general_toric_unconditional_graph.tex` finds 127 unique labels, no duplicate labels, 18 unique citation keys, and no missing or uncited bibliography entries.
3. Text extraction from the rebuilt PDF contains no literal `???` marker.
4. `python3 verification/verify_certificate.py --check verification/mixed_volume_certificate.json` passes byte-for-byte and reproduces the mixed volumes `6808`, `1568`, and `1248`.

Further reduction of \(\Theta_k\), or replacement of box supersupports by exact contact Newton polytopes, remains optional sharpening and is not needed for correctness of the theorem above.

No remaining mathematical gap was identified in the strong graph-structured theorem during this audit.
