import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from cStringIO import StringIO

from extractors.util import safe_text
from extractors.tesseract import extract_image_pdf


log = logging.getLogger(__name__)


def raw_pdf_convert(path):
    with open(path, 'rb') as fh:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp=StringIO(), laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        parser = PDFParser(fh)
        doc = PDFDocument(parser, '')
        pages = []
        if doc.is_extractable:
            for page in PDFPage.create_pages(doc):
                device.outfp.seek(0)
                device.outfp.truncate(0)
                interpreter.process_page(page)
                pages.append(device.outfp.getvalue())
        device.close()
        info = {}
        if len(doc.info):
            info = doc.info.pop()
        return info, pages


def extract_pdf(path, languages=None):
    """ Extract content from a PDF file. This will attempt to use PyPDF2
    to extract textual content first. If none is found, it'll send the file
    through OCR. """
    info, pages = raw_pdf_convert(path)
    data = {'pages': pages, 'ocr': False}
    for k, v in info.items():
        data[k.lower()] = safe_text(v)

    text = ''.join(data['pages']).strip()
    # FIXME: this should be smarter
    if not len(text):
        data['ocr'] = True
        for page in extract_image_pdf(path, languages=languages):
            data['pages'].append(page)
    return data


# convert in.png -gravity center -page A4 out.pdf
def image_to_pdf(path):
    pass
