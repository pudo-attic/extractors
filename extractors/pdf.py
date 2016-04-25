import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser, PDFSyntaxError
from pdfminer.pdfdocument import PDFDocument

from extractors.util import safe_text, text_fragments
from extractors.tesseract import _extract_image_page


log = logging.getLogger(__name__)

OCR_MIN_WIDTH = 200
OCR_MIN_HEIGHT = 50


def _find_objects(objects, cls):
    for lt_obj in objects:
        if isinstance(lt_obj, cls):
            yield lt_obj
        elif isinstance(lt_obj, LTFigure):
            for obj in _find_objects(lt_obj._objs, cls):
                yield obj


def _convert_page(layout, path, page_no, languages):
    text_content = []
    for text_obj in _find_objects(layout._objs, (LTTextBox, LTTextLine)):
        text_content.append(text_obj.get_text())

    text = text_fragments(text_content)
    if len(text) < 2:
        if len(list(_find_objects(layout._objs, LTImage))):
            log.debug("Defaulting to OCR: %r, pg. %s", path, page_no)
            text = _extract_image_page(path, page_no, languages)
    return text


def extract_pdf(path, languages=None):
    """
    Extract content from a PDF file.

    This will attempt to use pdfminer to extract textual content from
    each page. If none is found, it'll send the images through OCR.
    """
    with open(path, 'rb') as fh:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        parser = PDFParser(fh)
        try:
            doc = PDFDocument(parser, '')
        except PDFSyntaxError as pse:
            if 'No /Root object!' in pse.message:
                log.info("Invalid PDF file: %r", path)
                return None
            raise

        result = {'pages': []}
        if len(doc.info):
            for k, v in doc.info[-1].items():
                k = k.lower().strip()
                if k != 'pages':
                    result[k] = safe_text(v)

        if not doc.is_extractable:
            log.warning("PDF not extractable: %s", path)
            return result

        for i, page in enumerate(PDFPage.create_pages(doc)):
            text = None
            try:
                interpreter.process_page(page)
                layout = device.get_result()
                text = _convert_page(layout, path, i + 1, languages)
            except Exception as ex:
                log.warning("Failed to parse PDF page: %r", ex)
            text = text or ''
            result['pages'].append(text)
        device.close()
        return result
