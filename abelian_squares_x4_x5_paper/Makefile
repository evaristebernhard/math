PYTHON ?= python3
LATEX ?= xelatex
BIBTEX ?= bibtex

.PHONY: test pdf clean

test:
	$(PYTHON) test_verifier.py

pdf:
	$(LATEX) -interaction=nonstopmode -halt-on-error main.tex
	$(BIBTEX) main
	$(LATEX) -interaction=nonstopmode -halt-on-error main.tex
	$(LATEX) -interaction=nonstopmode -halt-on-error main.tex

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.pdf
