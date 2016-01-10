# extractors

Re-usable wrapper scripts for text document extractors. Principally, this supports the following operations:

* Use ``pdfminer`` to extract text from text-based PDF files
* Use ``tesseract`` to extract text from image files
* Split PDF files into image files using ``pdftoppm``
* Call on ``soffice`` (i.e. libreoffice) to convert other text document formats to PDF

## Example

```python
from extractors import extract_pdf, document_to_pdf, image_to_pdf, extract_image

# Unholy, make PDF from various office formats (doc, OO):
pdf_path = document_to_pdf('/path/to/a_word_document.docx')

# Unholy II, make PDF from various image fromats (png, jpg):
pdf_path = image_to_pfg('/path/to/an_image.png')
# or, do OCR:
text = extract_image('/path/to/an_image.png', languages=['en'])

# Chooses the best PDF extraction method (image or text):
data = extract_pdf('/path/to/my.pdf')
for page in data['pages']:
    print page

```

## Configuration

The binaries to be used can be configured using the following environment variables: ``TESSERACT_BIN``, ``SOFFICE_BIN``, ``PDFTOPPM_BIN`` and ``CONVERT_BIN``.

