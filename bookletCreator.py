from pypdf import PageObject, PdfReader, PdfWriter, Transformation
import copy
from tqdm import trange


def readPages(pdfFilePath: str) -> list[PageObject]:
    """ Reads a pdf file and returns it pages as [PageObject] """
    # Opens the files that has to be read
    pdfFileObj = open(pdfFilePath, 'rb')

    # Reads the files that was opened
    reader = PdfReader(pdfFileObj)

    # Make sa list of all pages
    pages: list[PageObject] = []
    for pageNum in range(len(reader.pages)):
        pageObj = reader.pages[pageNum]
        pages.append(pageObj)

    return pages


def writePages(pdfFilePath: str, pdfPages: list[PageObject]) -> None:
    """ Writes a list of [PageObject] to the given path """

    # Creates the writer
    writer = PdfWriter()

    for page in pdfPages:
        # Adds pages to the write
        writer.add_page(page)

    with open(pdfFilePath, 'wb') as f:
        writer.write(f)  # type: ignore

    writer.close()


def createBooklet(pdfPages: list[PageObject]) -> list[PageObject]:

    # Making a copy of each page
    pdfPages = [copy.copy(page) for page in copy.copy(pdfPages)]

    # Creates result list
    result: list[PageObject] = []

    # Get the page size (assuming all pages are of the same size)
    pageWidth = pdfPages[0].mediabox.width
    pageHeight = pdfPages[0].mediabox.height

    # Make paggenum even
    if len(pdfPages) % 2 != 0:
        pdfPages.append(PageObject.create_blank_page(
            None, pageWidth, pageHeight))

    # Gets amount of pages
    pageNum = len(pdfPages)

    # Iterate over each half of the pages from both sides
    for i in trange(0, int(pageNum/2), desc="Creating booklet"):

        # Swap the left and right page at each iteration
        if (i % 2 == 0):
            leftPage = pdfPages[pageNum-i-1]
            rightPage = pdfPages[i]
        else:
            leftPage = pdfPages[i]
            rightPage = pdfPages[pageNum-i-1]

        # Moves the right page to the right end of the left page
        rightPage.add_transformation(
            Transformation().translate(float(pageWidth), 0), True)

        # Merge pages to a new one
        leftPage.merge_page(rightPage, True)

        # Create final file with one page
        result.append(leftPage)

    return result


def createBookletUsingLargeFormat(pdfPages: list[PageObject]) -> list[PageObject]:

    # Creates the booklet
    pdfPages = createBooklet(pdfPages)

    # Creates result list
    result: list[PageObject] = []

    # Get the page size (assuming all pages are of the same size)
    pageWidth = pdfPages[0].mediabox.width
    pageHeight = pdfPages[0].mediabox.height

    # Make paggenum a multiple of 4
    insertingPosition = 0
    while len(pdfPages) % 4 != 0:
        pdfPages.insert(insertingPosition, PageObject.create_blank_page(
            None, pageWidth, pageHeight))
        insertingPosition = 2 if insertingPosition == 0 else 0

    # Gets amount of pages
    pageNum = len(pdfPages)

    # Iterate over all pages
    for i in trange(0, pageNum, 4, desc="Creating larger pages"):

        for j in range(0, 2):
            # Use page 1 and 3 at the front and 2 and 4 at the back
            upperPage = pdfPages[i+j]
            lowerPage = pdfPages[i+j+2]

            # Moves the lower page to the lower end of the left page
            lowerPage.add_transformation(
                Transformation().translate(0, -float(pageHeight)), True)

            # Merge pages to a new one
            upperPage.merge_page(lowerPage, True)

            # Create final file with one page
            result.append(upperPage)

    return result

# ******************** Example ********************

# filePages = readPages("input/a.pdf")

# convertedPages = createBooklet(filePages)

# writePages("output/a_merged.pdf", convertedPages)

# largePages = createBookletUsingLargeFormat(filePages)

# writePages("output/a_large.pdf", largePages)
