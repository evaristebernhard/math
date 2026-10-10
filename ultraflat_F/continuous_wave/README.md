# Continuous waveform research, N=200

The mathematical target is the complex one-circle function **B_N**, not the mean-zero real torus polynomial F; see [WAVEFORM_MATHEMATICS.md](WAVEFORM_MATHEMATICS.md).

This branch tests a conjugate-zero-pair *finite Blaschke product*, an analytically unit-modulus real-Fourier waveform. It is a **negative baseline**, not an OpenAI Section 5 reproduction or a q49-trained F. In particular we have NOT solved Section 4 coefficient spreading or produced improved Littlewood signs.

Run:

\`\`\`bash
pip install numpy torch
python train_blaschke.py --n 200 --pairs 24 --mesh 2048 --steps 700 --restarts 2 --out run24.json
python train_blaschke.py --n 200 --pairs 48 --mesh 2048 --steps 550 --restarts 1 --out run48.json
python p49_independent_control.py
\`\`\`

The new code enforces b0=1/sqrt(N) exactly by root radii and estimates phase speed, cap, and tail separately. In prior experiments, after independent high-density recomputation, the 24-pair baseline had min/max coefficient magnitudes 0.0024/2.0072 and tail L2 ≈0.00145; the 48-pair baseline had 0.0052/2.0027 and tail ≈0.06853. These **floating-point numerical** results are not certificates. The compact script is an independently reproducible version of the experiment; exact optimizer trajectories may differ across Torch versions.

Math priority: prove useful coefficient-cap and exterior ℓ1 tail bounds for a learned B_N and connect its phase to the *structured* q49/F stationary-phase orbit rather than independent teacher labels.
