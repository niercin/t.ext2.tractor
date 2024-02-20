# To read the PDF
from pageextractor import process_pdf_file
import utils
import sys

# Find the PDF path
PDF_FILE_PATH = sys.argv[1]
process_pdf_file(PDF_FILE_PATH)
