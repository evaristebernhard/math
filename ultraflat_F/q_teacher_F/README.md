# q49-guided F research (negative baselines + an exact obstruction)

Read `MATHEMATICAL_ANALYSIS.md` for the proofs and warnings. `q49` is an implicit, strictly bounded high-dimensional Fourier polynomial, **not** an enumerated F. None of the trained candidates here meet Proposition 4.1.

Requirements: `numpy scipy torch` for training; exact obstruction uses Python standard library and the adjacent repository `q49_bridge/certified_jackson_cutoffs.py`.

```
python certified_symmetry_obstruction.py --out obstruction_certificate.json
python q_martingale.py --samples 32768 --repeats 4 --out teacher_moments.json
python teacher_spectrum.py --samples 65536 --out teacher_projection.json
python distill_q49.py --steps 700 --out q49_distillation.json
python train_F_pilot.py --steps 1200 --out pilot_results.json
python train_spreading_factor.py --T 63 --steps 650 --out factor_results_T63.json
python -m unittest test_research.py
```

What these scripts demonstrate:
- rigorous violation of direct common-linear-weight balance for three surviving q49 Fourier coefficients;
- parity/conditional-expectation restrictions on q49 distillation;
- sampled Fourier projection losses and unsuccessful q49 teacher-student training;
- unsuccessful small p2 exactly-balanced model;
- explicit equal-Fourier-magnitude (by parametrization) chirp factor training, the actual OpenAI Lemma 4.2-shaped target.

The q49 energy certificate is reproduced separately in `../q49_bridge/`.
