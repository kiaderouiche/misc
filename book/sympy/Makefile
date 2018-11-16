.PHONY:all clean


all:main.pdf

clean:
	rm -f *.aux *.bcf *.log  *.xml  *.toc */*.aux *.bbl *.blg


%.pdf: %.tex %.bib #contenu/*.tex inclure/*.tex
	pdflatex $*.tex

	@echo "Citations indéfinies:" 
	@grep -i "Citation .* undefined" $*.log || echo "Aucune"
	@echo "Erreurs de label" 
	@egrep -i "multiply defined" $*.log || echo "Pas de label multiple" 
	@egrep -i "Reference .* undefined" $*.log || echo "Pas de label indéfini"
