import pytesseract
from pathlib import Path
import os

def remove_files_with_ext(directory, ext):
    for filename in os.listdir(directory):
        if filename.endswith(ext):
            os.remove(Path(directory) / filename)

# Given '/some/path/here/somefile.ext' as parameter
# this function returns '/some/path/here'
def get_parent_directory(file_path):
    return Path(file_path).parent.absolute()

# Given '/some/path/here/somefile.ext' as parameter
# this function returns 'somefile.ext'
def get_filename_with_ext(file_path):
    return Path(file_path).name

# Given '/some/path/here/somefile.ext' as parameter
# this function returns 'somefile'
def get_filename_wo_ext(file_path):
    return Path(file_path).stem

# Given '/some/path/here/somefile.ext' as parameter
# this function returns '.ext'
def get_file_ext(file_path):
    return Path(file_path).suffix

# Create a function to read text from images
def image_to_text(image_path):
    # Extract the text from the image
    text = pytesseract.image_to_string(str(image_path), lang='eng')
    return text

# Convert table into the appropriate format
def convert_table_to_text(table):
    table_string = ''
    # Iterate through each row of the table
    for row_num in range(len(table)):
        row = table[row_num]
        # Remove the line breaker from the wrapped texts
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        # Convert the table into a string 
        table_string+=('|'+'|'.join(cleaned_row)+'|'+'\n')
    # Removing the last line break
    table_string = table_string[:-1]
    return table_string
    