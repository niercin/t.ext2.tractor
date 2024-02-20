# To read the PDF
import PyPDF2
# To analyze the PDF layout and extract text
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTRect, LTFigure
# To extract text from tables in PDF
import pdfplumber

import os
import sys

import pdfcontent
import imgcontent
import utils

def extract_page_content(page, page_obj, page_tables, page_no):
    # Initialize the variables needed for the text extraction from the page
    page_text = []
    line_format = []
    text_from_images = []
    text_from_tables = []
    page_content = []

    # Initialize the number of the examined tables
    table_no = 0
    table_first_element = True
    table_extraction_flag = False
    table_lower_side = -1
    table_upper_side = -1
    
    tables = page_tables.find_tables()

    # Find all the elements
    page_elements = [(element, element.x1, element.y1) for element in page._objs]
    # Sort all the elements as they appear in the page

    # niercin: Sorting the elements makes a huge difference for the output
    # We should find out a way to analyze whether the page consists of one or more
    # columns, which will alter the sorting method, thus the final output.
    page_elements.sort(key=lambda a: a[2], reverse = True)

    # Find the elements that composed a page
    for i, component in enumerate(page_elements):
        # Extract the position of the top side of the element in the PDF
        # pos= component[0]
        # Extract the element of the page layout
        element = component[0]
        
        # Check if the element is a text element
        if isinstance(element, LTTextContainer):
            # Check if the text appeared in a table
            if table_extraction_flag == False:
                # Use the function to extract the text and format for each text element
                (line_text, format_per_line) = pdfcontent.extract_text_from(element)
                # Append the text of each line to the page text
                page_text.append(line_text)
                # Append the format for each line containing text
                line_format.append(format_per_line)
                page_content.append(line_text)
            else:
                # Omit the text that appeared in a table
                pass

        # Check the elements for images
        elif isinstance(element, LTFigure):
            # Crop the image from the PDF
            pdfcontent.crop_image_and_saveas_pdf(element, page_obj, TEMP_PDF_FILE_PATH)
            # Convert the cropped pdf to an image
            pdfcontent.convert_first_page_to_png(TEMP_PDF_FILE_PATH, TEMP_IMG_FILE_PATH)
            # Extract the text from the image
            image_text = imgcontent.image_to_text(TEMP_IMG_FILE_PATH)
            text_from_images.append(image_text)
            page_content.append(image_text)
            # Add a placeholder in the text and format lists
            page_text.append('image')
            line_format.append('image')
        
        # Check the elements for tables
        elif isinstance(element, LTRect):
            # If the first rectangular element
            if table_first_element == True and (table_no + 1) <= len(tables):
                # Find the bounding box of the table
                table_lower_side = page.bbox[3] - tables[table_no].bbox[3]
                table_upper_side = element.y1 
                # Extract the information from the table
                table = pdfcontent.extract_table_from(page_tables, table_no)
                # Convert the table information in structured string format
                table_string = utils.convert_table_to_text(table)
                # Append the table string into a list
                text_from_tables.append(table_string)
                page_content.append(table_string)
                # Set the flag as True to avoid the content again
                table_extraction_flag = True
                # Make it another element
                table_first_element = False
                # Add a placeholder in the text and format lists
                page_text.append('table')
                line_format.append('table')

            # Check if we already extracted the tables from the page
            if table_lower_side >= 0 and table_upper_side >= 0 \
                and element.y0 >= table_lower_side and element.y1 <= table_upper_side:
                pass
            elif not isinstance(page_elements[i + 1][0], LTRect):
                table_extraction_flag = False
                table_first_element = True
                table_lower_side = -1
                table_upper_side = -1
                table_no += 1
                
    return [page_text, line_format, text_from_images, text_from_tables, page_content]

def process_pdf_file(pdf_path):
    # create a PDF file object
    pdf_file_obj = open(pdf_path, 'rb')
    # create a PDF reader object
    pdf_reader_result_obj = PyPDF2.PdfReader(pdf_file_obj)
    # Open the pdf file
    pdf_plmb_result_obj = pdfplumber.open(pdf_path)

    # We extract the pages from the PDF 
    for page_no, page in enumerate(extract_pages(pdf_path)):
        page_obj = pdf_reader_result_obj.pages[page_no]
        # Find the examined page
        page_tables = pdf_plmb_result_obj.pages[page_no]
        # Extract content
        content = extract_page_content(page, page_obj, page_tables, page_no)

        with open(OUT_DIR / ("page_" + str(page_no).zfill(5) + ".txt"), 'w') as text_file:
            text_file.write(''.join(content[4]))

    # Closing the pdf file object
    pdf_file_obj.close()

# Find the PDF path
PDF_FILE_PATH = sys.argv[1]
# Output folder path
OUT_DIR = utils.get_parent_directory(PDF_FILE_PATH) / utils.get_filename_wo_ext(PDF_FILE_PATH)
if not os.path.exists(OUT_DIR):
    os.makedirs(OUT_DIR)

TEMP_PDF_FILE_PATH = OUT_DIR / 'temp_pdf.pdf'
TEMP_IMG_FILE_PATH = OUT_DIR / 'temp_img.png'

process_pdf_file(PDF_FILE_PATH)

# Clean up
os.remove(TEMP_PDF_FILE_PATH)
os.remove(TEMP_IMG_FILE_PATH)
