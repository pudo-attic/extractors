import os
import logging
import subprocess
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from PIL import Image
from tesserwrap import Tesseract, PageSegMode

from extractors.constants import _get_languages
from extractors.cache import set_cache, get_cache

# https://tesserwrap.readthedocs.org/en/latest/#
# https://pillow.readthedocs.org/en/3.0.x/reference/Image.html
log = logging.getLogger(__name__)
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
PDFTOPPM_BIN = os.environ.get('PDFTOPPM_BIN', 'pdftoppm')


def extract_image(path, languages=None):
    """
    Extract text from an image.

    Use tesseract to extract text in the given ``languages`` from an
    image file. Tesseract should support a wide range of formats, including
    PNG, TIFF and JPG.
    """
    with open(path, 'rb') as fh:
        return extract_image_data(fh.read(), languages=languages)


def extract_image_data(data, languages=None):
    """Extract text from a binary string of data."""
    if TESSDATA_PREFIX is None:
        raise ValueError('Env TESSDATA_PREFIX is not set, OCR will not work.')
    key, text = get_cache(data)
    if text is not None:
        return text
    try:
        img = Image.open(StringIO(data))
    except Exception as ex:
        log.debug('Failed to parse image internally: %r', ex)
        return ''

    # TODO: play with contrast and sharpening the images.
    try:
        extractor = Tesseract(TESSDATA_PREFIX, _get_languages(languages))
        extractor.set_page_seg_mode(PageSegMode.PSM_AUTO_OSD)
        extractor.set_image(img)
        text = extractor.get_utf8_text()
        extractor.clear()
        set_cache(key, text)
        return text
    except Exception as ex:
        log.exception(ex)
        # set_cache(key, '')
        return ''


def _extract_image_page(pdf_file, page, languages=None):
    # This is a somewhat hacky way of working around some of the formats
    # and compression mechanisms not supported in pdfminer. It will
    # generate an image based on the given page in the PDF and then OCR
    # that.
    args = [PDFTOPPM_BIN, pdf_file, '-singlefile', '-gray', '-f', str(page)]
    output = subprocess.check_output(args)
    return extract_image_data(output, languages=languages)
