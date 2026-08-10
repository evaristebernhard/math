# QT / Smith comparison material removed from the submission PDF

Date: 2026-08-09

Status: **research-supplementary, not part of the submission theorem chain.**

The source of `main.tex` still contains the former sections

- `A conditional QT identity inside residual distance 36`,
- the QT-lift theorem,
- the auxiliary-quadric calculation,
- the conditional exclusion of an irreducible normal nodal quartic Smith carrier,

inside a TeX `\iffalse ... \fi` block.  They are therefore preserved verbatim in the research source but omitted from the compiled submission PDF.

## Why they were removed from the submission narrative

The arguments are mathematically useful but depend on a long Smith-border input chain.  In particular the application requires an irreducible quartic carrier, a square-divisor relation, a quadratic free lift, a bordered matrix whose corank-two scheme is the residual 72-point set, and a reduced transverse eight-point scheme `Delta=V(a,b,c)`.  These assumptions are much more specialized than the global residual-36 theorem now proved in the submission.

The current paper no longer needs QT/Smith to obtain its main residual-36 result.  The disjoint-net six-quartic map gives

\[
D^3=36,\qquad g(D^2)=33,\qquad me=18,
\]

normal targets reduce to `(m,e)=(2,9)` or `(3,6)`, and the finite `(3,6)` target with isolated singularities is excluded by the K3 Euler argument.  QT/Smith is therefore best viewed as a possible tool for the remaining degenerate/nonnormal outlets, not as part of the main theorem chain.

## Mathematical status retained

1. **QT-lift.** Under the stated irreducible-carrier and square-divisor/free-lift hypotheses, the source proves
   \[
   \tau N=QMQ^t,\qquad QM=N\operatorname{adj}(Q)^t.
   \]
   The irreducibility of `tau` is essential in the proof eliminating the constant matrix error.

2. **Auxiliary quadric.** For symmetric
   \[
   Q=\begin{pmatrix}a&b\\b&c\end{pmatrix},\qquad \tau=ac-b^2,
   \]
   QT implies a quadratic `h` satisfying
   \[
   ax+2by+cz=h\tau,\qquad N=hQ-\operatorname{adj}(M).
   \]

3. **Conditional Smith-carrier exclusion.** Under the full Smith-border hypotheses, the normal nodal irreducible quartic carrier is excluded by the auxiliary-quadric instability analysis.  This remains a conditional theorem because the paper does not prove that every nonregular residual-36 comparison produces such a carrier with all required border data.

## Submission policy

Do not cite this hidden source as if it were an unconditional closure of residual 36.  It may be restored in a later methods paper or supplementary appendix if the Smith-border construction is made self-contained and its exhaustiveness is proved.
