# extractors

Re-usable wrapper scripts for text document extractors. Principally, this supports the following operations:

* Use ``pdfminer`` to extract text from text-based PDF files; uses ``libtesseract`` (i.e. in-process ``tesseract``) to extract text from images in image-only PDF pages.
* Call on ``soffice`` (i.e. libreoffice) to convert other text document formats to PDF.
* Call on ``imagemagick`` to convert images to PDF upon request.


## Example

```python
from extractors import extract_pdf, document_to_pdf, image_to_pdf, extract_image

# Unholy, make PDF from various office formats (doc, OO):
pdf_path = document_to_pdf('/path/to/a_word_document.docx')
# Unholy II, make PDF from various image fromats (png, jpg):
pdf_path = image_to_pdf('/path/to/an_image.png')

# or, do OCR:
text = extract_image('/path/to/an_image.png', languages=['en'])

# Chooses the best PDF extraction method (image or text):
data = extract_pdf('/path/to/my.pdf')
for page in data['pages']:
    print page

```

## Installation

The package is available on the Python cheese shop:

```bash
$ pip install extractors
```

``extractors`` depends heavily upon external applications, which must be installed. Install the equivalents of the following Ubuntu/Debian packages, depending on your use case:

### Image and PDF text recognition (tesseract)

The following packages are required: ``tesseract-ocr``, ``tesseract-ocr-osd``, ``libtesseract-dev``,
``tesseract-ocr-eng`` (and any other language training data needed).

**Important:** for OCR to work, the ``TESSDATA_PREFIX`` environment variable needs to be set and point at the directory containing ``tessdata/`` (i.e. the ``tesseract`` training files).

If the environment variable ``EXTRACTORS_CACHE_DIR`` is set, content-addressed caches of all converted image files will be stored there to accelerate repeated operations.

### Document to PDF conversion

The following packages are required: ``libreoffice``, ``default-jdk``.

### Image to PDF conversion

The following packages are required: ``imagemagick-common``, ``imagemagick``

After these have been installed, the paths to the binaries can be configured using the following environment variables: ``SOFFICE_BIN`` and ``CONVERT_BIN``.
