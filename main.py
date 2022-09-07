# You need to have Inkscape installed
# @author Jan Plischke

import locale
import os
import shutil
from datetime import date, timedelta

from dateutil import parser
from PyPDF2 import PdfFileMerger
from tqdm import tqdm

# Ask for start and end date and convert it to a date object
startDate = parser.parse(
    input("Start date (e.g. 22.5.22): "), dayfirst=True)
endDate = parser.parse(
    input("End date (e.g. 22.5.22): "), dayfirst=True)

# Ask for the lessons file name
lessonsFilename = input(
    "lessons file (Standard: lessons.txt): ") or "lessons.txt"

# Ask for the outout filename
outputFilename = input("Filename: (Standard: Calendar.pdf)") or "Calendar.pdf"

# Ask for the locale
DATE_LOCALE = input("Locale (Standard: de_DE.UTF-8): ") or "de_DE.UTF-8"

# Try to set locale
try:
    locale.setlocale(locale.LC_TIME, DATE_LOCALE)
except:
    print("Cannot set locale! Continue with default locale. If you want to use your locale please check if it is correctly installed!")


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


def formatWeekDate(startDate: date, weekLength=4):
    ''' Return the formatted date range like "25. - 29. April 2022" or "29. Apr - 02. März 2022"

    Parameters:
            startDate (date): The first day of the week
            weekLength (int): How many days are shown in the week (e.g. 4 (workweek) or 6 (week))

    Returns:
            formattedDate (str): The formatted date range
    '''
    # Get the month in long form
    month = startDate.strftime("%B")
    # Get the two digit string representation from the first and the last day of the week
    monday = startDate.strftime('%d')
    friday = (startDate+timedelta(days=weekLength)).strftime("%d")

    # Check if whole the week is within a month
    if (int(monday) < int(friday)):
        # Return formatted string (e.g. "25. - 29. April 2022")
        return f"{monday}. - {friday}. {month} {startDate.year}"
    else:
        # Get the month of the first day in short form
        month = startDate.strftime("%b")
        # Get the month of the last day in long form
        fridayMonth = (startDate+timedelta(days=weekLength)
                       ).strftime("%B")
        # Return formatted string (e.g. "29. Apr. - 02. März 2022")
        return f"{monday}. {month}. - {friday}. {fridayMonth} {startDate.year}"


# Clear/ create tmp folder
if os.path.exists("./tmp"):
    shutil.rmtree("./tmp")
os.mkdir("./tmp")


# Read BaseSvg File
with open("BaseSvg.svg", "r") as f:
    baseSvg = f.read()
    f.close()

# Read lessons file
with open(lessonsFilename, "r") as f:
    lessons = f.read()
    f.close()

# split lessons into a 2d matrix
lessons = lessons.split("\n\n")
for i in range(0, len(lessons)):
    lessons[i] = lessons[i].split("\n")


filesToMerge = []

# Initialize currentWeek
currentWeek = startDate

# Calculate how many weeks to generate
weeksToGenerate = int((endDate-startDate).days/7)+2

# For each week
for i in tqdm(range(1, weeksToGenerate), "Generating week pages"):

    # Create calendar week and append filename to the list
    filesToMerge.append(createCalendarWeek(
        baseSvg, formatWeekDate(currentWeek), lessons, i))

    # Next week
    currentWeek += timedelta(days=7)


# Create the PdfFileMerger class for merging the weeks to one calendar pdf
merger = PdfFileMerger()

# Iterate over the list of file names
for pdf_file in filesToMerge:
    # Append PDF files
    merger.append(pdf_file)

# Write out the merged PDF
print("Merging single pages to one file")
merger.write(outputFilename)
merger.close()

# Remove the tmp directory and all its contents
shutil.rmtree("./tmp")
