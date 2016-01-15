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
from extractors.cache import set_cache, get_cache

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
    with open(path, 'rb') as fh:
        return extract_image_data(fh.read())


def extract_image_data(data, languages=None):
    """ Extract text from a binary string of data containing an image in
    a commonly-used format. """
    if TESSDATA_PREFIX is None:
        raise ValueError('Env TESSDATA_PREFIX is not set, OCR will not work.')
    key, text = get_cache(data)
    if text is not None:
        return text
    img = Image.open(StringIO(data))
    # TODO: play with contrast and sharpening the images.
    try:
        extractor = _get_tesseract()
        extractor.set_image(img)
        text = extractor.get_utf8_text()
        extractor.clear()
        set_cache(key, text)
        return text
    except Exception as ex:
        log.exception(ex)
        set_cache(key, '')
        return ''


# if __name__ == '__main__':
#     import os
#     import thready
#     import hashlib

#     dir_name = '/Users/fl/Code/extractors/test/img'

#     def get_files():
#         for fn in os.listdir(dir_name):
#             if fn.endswith('.png'):
#                 yield os.path.join(dir_name, fn)

#     def parse(fn):
#         # with open(fn, 'rb') as fh:
#         #     print hashlib.sha1(fh.read()).hexdigest()
#         # # img = Image.open(fn)
#         # img.tobytes()
#         print [extract_image(fn)]

#     import time
#     begin = time.time()
#     # thready.threaded(get_files(), parse)
#     for fn in get_files():
#         parse(fn)
#     print time.time(), time.time() - begin
