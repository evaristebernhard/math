LATEXMK ?= latexmk
LATEXFLAGS := -pdf -interaction=nonstopmode -halt-on-error

.PHONY: all pdf supplement clean verify

all: pdf

pdf:
	$(LATEXMK) $(LATEXFLAGS) main.tex

supplement:
	$(LATEXMK) $(LATEXFLAGS) supplementary_certificate.tex

verify:
	python3 verification/verify_certificate.py --check verification/mixed_volume_certificate.json

clean:
	$(LATEXMK) -C main.tex
	$(LATEXMK) -C supplementary_certificate.tex
