
OUT_FILENAME=HA_Heft

all: generateCalendar convertToBook convertToA4 cleanUp moveToOutput

generateCalendar:
	@echo "Generating Calendar (runs twice)"
	latexmk -pdf  -lualatex -interaction=nonstopmode variante2.tex #| grep -E '\[[0-9]+\]'
convertToBook:
	@echo "Converting to Book" 
	latexmk -pdf -lualatex -interaction=nonstopmode variante2-buch.tex  #| grep -E '\[[0-9]+\]'
convertToA4:
	@echo "Converting to A4"
	latexmk -pdf -lualatex -interaction=nonstopmode variante2-buch-a4.tex #| grep -E '\[[0-9]+\]'
cleanUp:
	@echo "Cleaning up"
	latexmk -c #| grep -E '\[[0-9]+\]'
moveToOutput:
	@echo "Moving to output folder"
	mkdir -p output
	mv variante2.pdf ./output/${OUT_FILENAME}.pdf
	mv variante2-buch.pdf ./output/${OUT_FILENAME}-buch.pdf
	mv variante2-buch-a4.pdf ./output/${OUT_FILENAME}-buch-a4.pdf