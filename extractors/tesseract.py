import os
import logging
import threading
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

from PIL import Image
from tesserwrap import Tesseract, PageSegMode

from extractors.constants import _get_languages

# https://tesserwrap.readthedocs.org/en/latest/#
# https://pillow.readthedocs.org/en/3.0.x/reference/Image.html
log = logging.getLogger(__name__)
tess = threading.local()
TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')


def _get_tesseract():
    # FIXME: not currently loading small language sets.
    languages = _get_languages(None)
    if not hasattr(tess, 'instance'):
        tess.instance = Tesseract(TESSDATA_PREFIX, languages)
        tess.instance.set_page_seg_mode(PageSegMode.PSM_AUTO_OSD)
    return tess.instance


def extract_image(path, languages=None):
    """ Use tesseract to extract text in the given ``languages`` from an
    image file. Tesseract should support a wide range of formats, including
    PNG, TIFF and JPG. """
    if TESSDATA_PREFIX is None:
        raise ValueError('Env TESSDATA_PREFIX is not set, OCR will not work.')
    img = Image.open(path)
    # TODO: play with contrast and sharpening the images.
    try:
        extractor = _get_tesseract()
        extractor.set_image(img)
        text = extractor.get_utf8_text()
        extractor.clear()
        return text
    except Exception as ex:
        log.exception(ex)
        return ''


def extract_image_data(data, languages=None):
    """ Extract text from a binary string of data containing an image in
    a commonly-used format. """
    return extract_image(StringIO(data))


# if __name__ == '__main__':
#     import os
#     import thready

#     dir_name = '/Users/fl/Code/extractors/test/img'

#     def get_files():
#         for fn in os.listdir(dir_name):
#             if fn.endswith('.png'):
#                 yield os.path.join(dir_name, fn)

#     def parse(fn):
#         print [extract_image(fn)]

#     import time
#     begin = time.time()
#     thready.threaded(get_files(), parse)
#     print time.time(), time.time() - begin
