echo "Generating Calendar (runs twice)"
latexmk -pdf  -lualatex variante2.tex | grep -E '\[[0-9]+\]'
echo "Converting to Book" 
latexmk -pdf -lualatex variante2-buch.tex  | grep -E '\[[0-9]+\]'
echo "Converting to A4"
latexmk -pdf -lualatex variante2-buch-a4.tex  | grep -E '\[[0-9]+\]'
echo "Cleaning up"
latexmk -c  | grep -E '\[[0-9]+\]'
echo "Moving to output folder"
mkdir -p output
mv variante2.pdf ./output/variante2.pdf
mv variante2-buch.pdf ./output/variante2-buch.pdf
mv variante2-buch-a4.pdf ./output/variante2-buch-a4.pdf
echo "Finished!"