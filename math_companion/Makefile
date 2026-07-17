.PHONY: all clean

all: main.pdf

main.pdf: main.tex macro.tex prelim.tex fri.tex whir.tex hypercube.tex swirl.tex lookup.tex references.bib
	pdflatex -interaction=nonstopmode main.tex
	bibtex main
	pdflatex -interaction=nonstopmode main.tex
	pdflatex -interaction=nonstopmode main.tex

clean:
	rm -f main.aux main.bbl main.blg main.log main.out main.toc main.pdf
