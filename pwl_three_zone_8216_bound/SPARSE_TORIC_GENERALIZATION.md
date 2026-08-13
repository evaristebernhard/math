# Sparse toric flight generalization — status audit

## Integrated into the manuscript as proved results

1. **Laurent flight relation for constant slopes.** For
   \[
   x'=a_jx+\sum_{m=-M}^{M}\beta_{j,m}e^{imt},\qquad a_j\neq0,
   \]
   a flight from \(t_j\) to \(t_{j+1}\) becomes a Laurent matching equation in
   \(q_j=e^{it_j}\), \(q_{j+1}=e^{it_{j+1}}\), and
   \(R_j=e^{a_j(t_{j+1}-t_j)}\).

2. **Four-extreme-point Newton containment.** The single-flight Newton polytope is contained in
   \[
   \operatorname{conv}\{\pm M e_{q_{j+1}},\ e_{R_j}\pm M e_{q_j}\}.
   \]

3. **Logarithmic support preservation.** Constant-coefficient logarithmic vector fields act diagonally on Laurent monomials, hence
   \[
   \operatorname{Newt}(DF)\subseteq\operatorname{Newt}(F).
   \]
   Contact determinants therefore acquire support only through Minkowski sums, not through differentiation itself.

4. **Interaction-graph mixed-volume theorem.** For local axis boxes indexed by a bipartite flight--phase graph \(\mathcal B\), the mixed volume with \(k\) copies of a global box is exactly a weighted matching (monomer--dimer) partition function of \(\mathcal B\).

5. **Cycle corollary.** For a cyclic \(k\)-flight itinerary, the incidence graph is \(C_{2k}\); with the natural coarse boxes used in the manuscript,
   \[
   \operatorname{MV}(L_1,\ldots,L_k,S^k)=k!(4M)^k\mathsf L_{2k},
   \]
   where \(\mathsf L_n\) is the Lucas sequence.

6. **Zero-slope extension.** If \(a_j=0\), introducing \(T_j=t_{j+1}-t_j\) gives a polynomial--Laurent flight relation.  In the mixed coframe using \(dT_j\) on zero-slope flights, ordinary differentiation only lowers the nonnegative \(T_j\)-exponent, so the adopted box supersupport is still preserved; no separate asymptotic penalty is needed.

## Newly closed: unconditional fixed-itinerary theorem

The conditional admissibility hypothesis can be removed by using Kaloshin's **all-loose** formulation rather than treating the matching equations as rigid equations.  The physical flight relations form a global separating chain on the cyclic crossing configuration space, and
\[
\rho_k=\prod_j\left(2-\frac{q_{j+1}}{q_j}-\frac{q_j}{q_{j+1}}\right)\frac{y_j}{(1+y_j)^2}
\]
is an explicit covering function.  The \(k\) matching equations are taken as loose equations.  After Kaloshin's standard conversion they contribute \(dQ_1,\ldots,dQ_k\), so the reduction eliminates \(2k\) forms in total.

Define
\[
A_0(N)=2^{N(N-1)/2},
\]
\[
A_j(N)=2^{((j-1)(j-2)+(N-j)(N-j-1))/2}(2^{j-1}+1)^{N-j},
\]
and
\[
\Theta_N=A_0(N)+\frac12\sum_{j=1}^N A_j(N).
\]
Then the clean unconditional fixed-itinerary estimate is
\[
\boxed{N_X(k,M)\le \Theta_{2k}(2k)!(8M)^k.}
\]
This includes zero slopes and isolated degenerate crossing cycles, the latter via the additive-bias perturbation used by Bravo--Trinidad-Forte.  A clean standalone proof is in `general_toric_unconditional.tex`.

Summing over the at most \(2Mn\) crossing sequences and using the crossing bound \(k\le2Mn\) gives an unconditional Hilbert-type bound for the constant-slope subclass; for continuous piecewise vector fields the same additive-bias argument also removes tangencies.

## Stronger graph-structured theorem: now closed modulo final typesetting audit

A simultaneous Sard regularization closes the former rigid-level seam.  For an arbitrary finite collection of nondegenerate transition roots, shift the matching equations to one small common level \(Q=b\).  The value \(b\) can be chosen to be regular for \(Q\) restricted to every partial physical leaf \(\Gamma_r\).  Hence the intersections \(V_b\cap\Gamma_r\) form a genuine separating chain on the smooth algebraic level \(V_b=Q^{-1}(b)\).  Running the one-dimensional relative Khovanskii--Rolle induction on this level retains all \(k\) local flight equations as rigid equations, and therefore retains the interaction-graph mixed volume.

The stronger unconditional candidate, with a complete proof written in `general_toric_unconditional_graph.tex`, is
\[
\boxed{N_X(k,M)\le \Theta_k\,k!(4M)^k\mathsf L_{2k}.}
\]
The proof also fixes the volume-form normalization: induced volume forms are chosen compatibly so that every relative contact function is represented by the ambient polynomial--Laurent wedge determinant, not merely by that determinant times an uncontrolled positive function.  The cleared covering polynomial is used as the rigid equation after the covering step.

The all-loose theorem
\[
N_X(k,M)\le \Theta_{2k}(2k)!(8M)^k
\]
remains as a conservative backup that follows directly from Kaloshin's formal all-loose mixed-system framework.

## Still open / sharpening only

1. Optimizing the KR dilation constant \(\Theta_k\) or exploiting the exact contact supports rather than box supersupports.
2. Extending the graph formula beyond cyclic scalar itineraries to more general sparse interaction graphs in a dynamical setting.
3. Any claim that the wider general theorem improves the sharp three-zone conjecture \(L^*=5\); the sharp five-cycle problem remains a separate real-oscillation question.

## Current paper narrative

- Specific dynamics: global response curve, residence identity, amplitude transversality, and no-three-zone rigidity.
- Concrete sparse application: exact Laurent supports, two Khovanskii--Rolle reductions, BKK values \(6808,1568,1248\), hence \(8216\).
- General method extracted from that application: sparse toric flight encoding and graph-structured mixed volume.
- Global three-zone conclusion: \(L^*\le16437\), while \(L^*=5\) remains open and requires a global one-turning/no-valley theorem for the genuine three-zone singular graph.
