.PHONY: verify test experiments paper
verify:
	python3 proof/certify_seven.py
	python3 -m unittest discover -s tests -v
test: verify
experiments:
	python3 experiments/independent_ode.py
	python3 experiments/high_precision_roots.py
	python3 experiments/plot_mechanism.py
paper:
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
	cd paper && pdflatex -interaction=nonstopmode -halt-on-error main.tex
