DATA := $(wildcard *.tsv)
SOURCES := $(filter-out global._include_.gpi template.gpi, $(wildcard *.gpi))
PNGOBJECTS := $(SOURCES:.gpi=.png)
GNUPLOT := $(shell command -v gnuplot)
LATEX := $(shell command -v pdflatex)
CONVERT := $(shell command -v convert)

all: png

png: $(PNGOBJECTS)

%.png: %.tex %-inc.eps
	$(LATEX) $<
	$(CONVERT) $(@:.png=.pdf) -depth 300 -units pixelsperinch -flatten $@

%.tex %-inc.eps: %.gpi global._include_.gpi $(DATA) 
	$(GNUPLOT) -e 'set output "$(<:.gpi=.tex)"' $<

clean:
	-rm -rf *.aux *.log *.dvi *-inc.eps *-inc-eps-converted-to.pdf

very-clean: clean
	-rm -rf $(PNGOBJECTS)

.PHONY: all png clean very-clean
