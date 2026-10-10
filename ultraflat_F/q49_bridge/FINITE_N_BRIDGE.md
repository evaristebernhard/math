# What the certified d=49 auxiliary q does, and does not, give

## Confirmed q certificate

For the quartic recursion with p1=cos(theta1), a 41st-order exact rational Bernstein positivity test gives a contraction factor below 9031/10000. A positive Jackson smoothing operator at d=49 then gives an implicitly defined real trigonometric polynomial q with

- mean zero and nonparallel nonzero Fourier sign-pairs;
- ||q||_infty <= 1;
- 1-||q||_2^2 <= 0.004780351831704404 + 0.004994448565542868 < 0.009774801.

The filtered **rectangular Fourier bounding box** contains fewer than 2^730.235 lattice points. This is neither the true support count nor an explicitly available coefficient table.

## A new rigorous observation: q already suppresses Fourier autocorrelation

Because 0 <= q^2 <= 1, pointwise (1-q^2)^2 <= 1-q^2. Hence

    ||q^2-1||_2^2 <= 1-||q||_2^2 < 0.009774801.

Writing M = ||q||_2^2 and r_h = Fourier(q^2)(h), Parseval yields

    sum_{h != 0} |r_h|^2 = ||q^2||_2^2 - M^2
                           <= M-M^2 <= 0.009774801.

Thus q has the same type of strong additive-cancellation structure that previous direct-F gradient experiments struggled to find. The *missing* property is not autocorrelation energy; it is a **single common linear weight** v giving |b_s|^2 approximately |s dot v|, with manageable support. q itself is NOT the F of Proposition 4.1.

## q -> F -> N: existence, not feasibility at N=200

OpenAI's Section 4 takes precisely such bounded, high-energy seed polynomials and spreads each original frequency using a product of balanced spreading factors. Hence this q does imply existence of an appropriate F **in principle**. But the exact support D and coefficient L1 norm are unavailable at useful computational scale, and the proof's factor-approximation budget contains sum_s |b_s| * D * alpha * (1+alpha)^(D-1).

After a valid F is fixed, Sections 5 and 6 generate real Littlewood signs for **sufficiently large** N. No finite bound obtained here proves that 200 is sufficiently large.

## A necessary scale for the *individual-wave* stationary-phase argument

A balanced F has 2D Fourier frequencies a, positive weights w_a=|a dot v|, and total weight <1. The Section 5 construction assigns each mode and packing group h an arc of length w_a/H, and places inside it a wave of constant amplitude m_a=|c_a|/sqrt(w_a).

By the triangle inequality,

    sqrt(N)*|integral_{I_(a,h)} B_N(t) exp(-2pi i k t)dt|
      <= sqrt(N)*m_a*(w_a/H)
      = |c_a|*sqrt(N*w_a)/H.

At an interior normalized index where chi_h=1, the formal stationary-phase main term has magnitude |c_a|. Therefore approximating **each individual stationary-phase term** to relative amplitude 1-eta requires

    N*w_a/H^2 >= (1-eta)^2.

If this is to hold for all 2D frequencies, sum_a w_a < 1 implies

    N > 2D*(1-eta)^2*H^2.

In the ideal eta -> 0 limit and N=200 this is D<100 for H=1; D<25 for H=2; D<6.25 for H=4. This is a **necessary amplitude-resolution check for the paper's per-wave asymptotic**, not a universal obstruction against better finite-N wave designs. For reliably small stationary-phase errors one needs the stronger scale N*w_min/H^2 >> 1.

## 99%-energy q may not be accurate enough

Section 6's qualitative rounding error includes O(sqrt(delta) log(1/delta)) with hidden constants and an unspecified N0(delta). Thus 99%-energy q does not certify 5% or 10% flatness at N=200. More quantitatively, if a compressed surrogate G obeys ||G-q||_infty<=tau, its guaranteed squared energy is only (sqrt(M)-tau)^2. Using merely M>=0.9902251996, retaining energy >=0.99 by this bound demands tau approximately <=0.0001132. There is almost no energy margin for learned compression.

## Decision

Do not discard q or train its raw 49-variable values again. q is already a good teacher for the **autocorrelation cancellation** structure.

Before investing in a deep-learning model for F, select explicit targets delta, D, H, min w and N and solve a small-support/weight-feasibility problem. A valid candidate needs uniform ||F||_infty control, near-unit weight mass, small maximum relative coefficient-weight error, and nonparallel frequencies. Certify these separately; optimize the wave/packing phases only afterward. No preference for powers of two exists in the existence theorem.
