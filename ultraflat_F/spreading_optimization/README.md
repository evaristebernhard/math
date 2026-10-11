# Grouped and anisotropic OpenAI spreading — feasibility audit

**Status:** partial mathematical optimization **not** a usable Proposition 4.1 auxiliary polynomial F.  All numerical estimates refer to finite small seeds and are not a new ultraflat construction.

This research follows `openai/math`, October 5, 2026, `build/sections/balanced.tex` and our previous `ultraflat_F/freiman_lift/` work.

## Exact theorem: grouped hyperplane spreading

Let `S={±s_1,...,±s_D}` be a finite frequency set with no nonparallel duplicates, and all Fourier coefficients `b_s≠0`. Partition the sign pairs into groups `G_j` such that each group is linearly independent, has span dimension <d, and **none of the other support frequencies lies in that span**. (For singleton groups this is always true by pairwise nonparallelity.)

For each group there is `W_j^0` annihilating exactly that group (among S) but no other frequency. Let `gamma` satisfy `rho_s=|s·gamma|>0`. Because members of each group are independent, solve the linear equations

```
s·W_j^1 = |b_s|^2 / [rho_s * product_{ell!=j}|s·W_ell^0|]
```

for every representative `s∈G_j`. Put `W_j=W_j^0+tau W_j^1`. Every support frequency has exactly one factor vanishing at tau=0, so

```
product_j |s·W_j| = tau * |b_s|^2/rho_s * (1+O(tau))
```

uniformly for the finite support. This is the same product fitting used in the original proof, but **one direction per group**, not necessarily per sign pair. The remaining equal-modulus factor approximation and sup-norm proof work verbatim (r factors instead of D), once constructed at sufficiently large widths. This is an exact asymptotic theorem; it provides no practical finite T bound by itself.

## Explicit degree-two original recursion at d=3

The rational Fourier expansion from `seed_fourier.generate(3)` contains D=27 sign-pairs. A maximum matching among *clean* 2D support-spans in three-dimensional frequency space pairs 12 of these and leaves 3 singleton groups, producing **r=15** spreading directions. Cross products provide exact integer `W_j^0` with no unwanted zero projections; rational linear algebra gives exact `W_j^1` for the chosen `gamma=(1,13,169)`.

With `tau=1/100`, the exact-rational product fit has maximum relative error 0.0003125. But the smallest `|s·W_j|` is around `2.61×10^-23`. Requiring even a nominal minimum `T_j|s·W_j|≥100` makes the **smallest** attainable sample box around `10^283` coefficients and the largest about `10^291` in this particular construction. These figures use an extremely optimistic width criterion; no uniform factor error claim follows. The constructed F therefore is **not usable**.

Choosing independent chirp scales `T_j` instead of a common T is mathematically legitimate. The ideal target is `g(z_j)e(T_j(s·W_j)z_j²/2)`; box size is asymptotic to `product_j(T_j|s·W_j|)` and the final weight vector rescales by `1/(tau*product_j T_j)`. `N` need not be a power of two. The anisotropic choice reduces `log10 product_j T_j` from about 368.74 to 293.23 for this example, but leaves an enormous cost.

## A hard factor-training feasibility gate

For `h_beta(z)=g(z)exp(pi*i*T*beta*z²)` and its coefficients `I_u`, any `L`-term factor with exactly equal Fourier coefficient magnitudes `1/sqrt(L)` satisfies

```
||f-h||_infty >= ||f-h||_2 >= E_*(T,beta,g)
E_*^2 = sum_{u in box}(|I_u|-1/sqrt(L))^2 + sum_{u outside box}|I_u|^2.
```

The **equality for the best L2 error** follows by choosing each Fourier phase to agree with the target coefficient. The factor magnitude constraint is exact. The numerical `E_*` values below are computed by FFT quadrature on a dense grid and **are not rigorous continuum lower-bound certificates**; the formula itself is exact. For the same C-infinity taper (`edge=.025`) as the earlier Adam trial: `T=63` -> `E_*≈.2078`; `T=127` -> `.1768`, `T=255` -> `.1510`, `T=1023` -> `.1215`. Optimizing taper width in a discrete candidate set improves these numbers modestly but still does not approach the tiny per-factor budgets a 99%-flat q would require.

This demonstrates that improving the phase optimizer alone is insufficient at modest T: the desired *coefficient magnitudes themselves* are too far from a flat spectrum.

## Certified pruning bound

For any seed q with real Fourier coefficients, deleting modes in symmetric pairs with sum of **both** coefficient absolute values `epsilon` yields a new finite polynomial `q_keep` with `||q_keep||∞≤||q||∞+epsilon` and energy deficit exactly equal to the sum of the deleted squared magnitudes. This permits preprocessing tiny modes without sampling. For the original d=3 seed, dropping four smallest pairs costs `L1≈0.0078125`, while the support falls to D=23 and regrouping gives r=12. For q49, the needed `L1` tail and support cannot presently be computed efficiently, so this reduction is not claimed there.

## Run

```bash
pip install numpy sympy networkx
python test_spreading.py
python hyperplane_groups.py
python factor_gate.py --T 63 127 255 1023
```

Next: design and certify a *small-support q-surrogate* with full Fourier coefficients, then optimize **the total output box size and the smallest output weight** (not merely r). Reject all candidates that cannot meet the uniform factor budget and finite-N stationary-phase resolution.
