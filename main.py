# You need to have Inkscape installed
# @author Jan Plischke

import os
import shutil
from PyPDF2 import PdfFileMerger


def createCalendarWeek(baseSvg: str, date: str, lessons: list, pageNum: int, filenamePrefix="Week"):
    ''' Create a Pdf file for one week with the date and the lessons

        Parameters:
                baseSvg (str): The read BaseSvg.svg file
                date (str): The date of the week (e.g. 1.1. - 7.1. Januar 2022)
                lessons (list): A 7x6 Matrix with the subject for each lesson 
                pageNum (int): A number for naming the current week
                fileNamePrefix (str): Filename is mad of 'tmp/' + filenamePrefix + pageNup + '.pdf' 

        Returns:
                path (str): relative path of the created file
                    '''

    # Replace the 'Date' placehholder with to date
    newSvg = baseSvg.replace(">Date<", f">{date}<")

    # Iterate over each day of the week (1-6 incl.)
    for day in range(1, 7):

        # Iterate over each lesson of a day (1-7 incl.)
        for lesson in range(1, 8):

            newSvg = newSvg.replace(

                # Each lesson/ day has a unique number (e.g. Mo, 3rd lesson => 13)
                f">{day}{lesson}<",

                # Replace it with the value from the matrix
                f">{lessons[day-1][lesson-1]}<")

    # Write new svg file to tmp folder
    with open("./tmp/CurrentPage.svg", "w") as f:
        f.write(newSvg)
        f.close()

    # Convert the created svg file to a pdf file using Inkscape CLI
    os.system(
        f'inkscape --export-type="pdf" --export-filename="tmp/Week{pageNum}.pdf" ./tmp/CurrentPage.svg')

    # Remove temporary svg file
    os.remove("./tmp/CurrentPage.svg")

    # Return filename of the created pdf file
    return f"tmp/{filenamePrefix}{pageNum}.pdf"


# Clears/ creates tmp folder
if os.path.exists("./tmp"):
    shutil.rmtree("./tmp")
os.mkdir("./tmp")


# Read BaseSvg File
f = open("BaseSvg.svg", "r")
baseSvg = f.read()
f.close()


lessons = [["kR", "kR", "F", "F", "D", "D", "ITG"],
           ["M", "M", "E", "E", "BK", "BK", " "],
           ["Mu", "Mu", "D", "D", "E", "E", " "],
           ["Ek", "Nw", "M", "M", "F", "F", "INS"],
           ["Nw", "Nw", "Sp", "Klt", "Swi", "Swi", " "],
           ["N", "O", "T", "I", "Z", "E", "N"]]


filesToMerge = []

filesToMerge.append(createCalendarWeek(
    baseSvg, "04. - 08. August 2022", lessons, 1))
filesToMerge.append(createCalendarWeek(
    baseSvg, "10. - 14. August 2022", lessons, 2))
filesToMerge.append(createCalendarWeek(
    baseSvg, "16. - 20. August 2022", lessons, 3))

# Create the PdfFileMerger class for merging the weeks to one calendar pdf
merger = PdfFileMerger()

# Iterate over the list of file names
for pdf_file in filesToMerge:
    # Append PDF files
    merger.append(pdf_file)

# Write out the merged PDF
merger.write("Calendar.pdf")
merger.close()

# Remove the tmp directory and all its contents
shutil.rmtree("./tmp")
