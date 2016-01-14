import logging

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage

from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument

from extractors.util import safe_text
from extractors.tesseract import extract_image_data


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


def _convert_page(layout, languages):
    text_content = []
    for text_obj in _find_objects(layout._objs, (LTTextBox, LTTextLine)):
        text_content.append(text_obj.get_text())

    text = ' '.join([t.strip() for t in text_content
                     if t is not None and len(t)])

    # TODO: invent a smarter way to decide whether to do OCR.
    if len(text.strip()) > 3:
        return text

    for img_obj in _find_objects(layout._objs, LTImage):
        try:
            if img_obj.width < OCR_MIN_WIDTH or \
                    img_obj.height < OCR_MIN_HEIGHT:
                continue
            data = img_obj.stream.get_rawdata()
            img_text = extract_image_data(data, languages=languages)
            text_content.append(img_text)
        except Exception as ex:
            log.debug(ex)

    return ' '.join([t.strip() for t in text_content
                     if t is not None and len(t)])


def extract_pdf(path, languages=None):
    """ Extract content from a PDF file. This will attempt to use PyPDF2
    to extract textual content first. If none is found, it'll send the file
    through OCR. """
    with open(path, 'rb') as fh:
        rsrcmgr = PDFResourceManager()
        laparams = LAParams()
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        parser = PDFParser(fh)
        doc = PDFDocument(parser, '')
        result = {'pages': []}
        if len(doc.info):
            for k, v in doc.info[-1].items():
                k = k.lower().strip()
                if k != 'pages':
                    result[k] = safe_text(v)

        if not doc.is_extractable:
            log.warning("PDF not extractable: %s", path)
            return result

        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
            layout = device.get_result()
            text = _convert_page(layout, languages)
            result['pages'].append(text)
        device.close()
        return result


# if __name__ == '__main__':
#     import os
#     import thready

#     dir_name = '/Users/fl/Code/extractors/test/pdf'

#     def get_files():
#         for fn in os.listdir(dir_name):
#             if fn.endswith('.pdf'):
#                 yield os.path.join(dir_name, fn)

#     def parse(fn):
#         print fn
#         extract_pdf(fn)
#         # print []
#         # print [extract_image(fn, force_fork=True)]

#     # import time
#     # begin = time.time()
#     # thready.threaded(get_files(), parse)
#     # print time.time(), time.time() - begin
#     for pdf_file in get_files():
#         extract_pdf(pdf_file)
