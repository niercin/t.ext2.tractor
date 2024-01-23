# t.ext2.tractor
PDF to Text Extractor

I got the idea and available code from here, then modified it according to my needs

https://towardsdatascience.com/extracting-text-from-pdf-files-with-python-a-comprehensive-guide-9fc4003d517

His github repository: https://github.com/g-stavrakis/PDF_Text_Extraction

Install these before running the code
- pip install PyPDF2
- pip install pdfminer.six
- pip install pdfplumber
- pip install pdf2image
- pip install Pillow
- apt install tesseract
- pip install pytesseract

How to run it
- $> cd path_to_t.ext2.tractor_directory
- $> python3 main.py some_path/some_file.pdf

Output
- A directory will be created in the same directory with input pdf file such as some_path/some_file
- The text from each page of the PDF will be printed on seperate .txt files like page_n.txt




