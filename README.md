# extractors

Re-usable wrapper scripts for text document extractors. Principally, this supports the following operations:

* Use ``pdfminer`` to extract text from text-based PDF files
* Use ``tesseract`` to extract text from image files
* Split PDF files into image files using ``pdftoppm``
* Call on ``soffice`` (i.e. libreoffice) to convert other text document formats to PDF

## Configuration

The binaries to be used can be configured using the following environment variables: ``TESSERACT_BIN``, ``SOFFICE_BIN``, ``PDFTOPPM_BIN``.

