import pytesseract

# Create a function to read text from images
def image_to_text(image_path):
    # Extract the text from the image
    text = pytesseract.image_to_string(str(image_path), lang='eng')
    return text