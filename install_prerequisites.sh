#!/bin/bash

sudo apt install -y tesseract-ocr \
                    python3-pip

pip install PyPDF2 --break-system-packages
pip install pdfminer.six --break-system-packages
pip install pdfplumber --break-system-packages
pip install pdf2image --break-system-packages
pip install Pillow --break-system-packages
pip install pytesseract --break-system-packages
