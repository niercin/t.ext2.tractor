import PyPDF2
from pdfminer.layout import LTTextContainer, LTChar
from pdf2image import convert_from_path

def extract_text_from(element):
    # Extracting the text from the in-line text element
    line_text = element.get_text()
    
    # Find the formats of the text
    # Initialize the list with all the formats that appeared in the line of text
    line_formats = []
    for text_line in element:
        if isinstance(text_line, LTTextContainer):
            # Iterating through each character in the line of text
            for character in text_line:
                if isinstance(character, LTChar):
                    # Append the font name of the character
                    line_formats.append(character.fontname)
                    # Append the font size of the character
                    line_formats.append(character.size)
    # Find the unique font sizes and names in the line
    format_per_line = list(set(line_formats))
    
    # Return a tuple with the text in each line along with its format
    return (line_text, format_per_line)

def crop_image_and_saveas_pdf(element, page_obj, output_file_path):
    # Get the coordinates to crop the image from the PDF
    [image_left, image_top, image_right, image_bottom] = [element.x0,element.y0,element.x1,element.y1] 
    # Crop the page using coordinates (left, bottom, right, top)
    page_obj.mediabox.lower_left = (image_left, image_bottom)
    page_obj.mediabox.upper_right = (image_right, image_top)
    # Save the cropped page to a new PDF
    cropped_pdf_writer = PyPDF2.PdfWriter()
    cropped_pdf_writer.add_page(page_obj)
    # Save the cropped PDF to a new file
    with open(output_file_path, 'wb') as cropped_pdf_file:
        cropped_pdf_writer.write(cropped_pdf_file)

# Create a function to convert the PDF to images
def convert_first_page_to_png(input_file_path, output_file_path):
    images = convert_from_path(input_file_path)
    image = images[0]
    image.save(output_file_path, "PNG")

# Extracting tables from the page
def extract_table_from(page_tables, table_no):
    # Extract the appropriate table
    table = page_tables.extract_tables()[table_no]
    return table