import os
import logging
import threading
import subprocess
try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO
from tempfile import mkstemp

from PIL import Image
import tesserwrap


log = logging.getLogger(__name__)
tess = threading.local()

# https://tesserwrap.readthedocs.org/en/latest/#
# https://pillow.readthedocs.org/en/3.0.x/reference/Image.html

TESSDATA_PREFIX = os.environ.get('TESSDATA_PREFIX')
LANGUAGES = {
    'en': 'eng',
    'de': 'deu',
    'be': 'bel',
    'az': 'aze',
    'cs': 'ces',
    'hr': 'hrv',
    'hu': 'hun',
    'ru': 'rus',
    'pl': 'pol',
    'sk': 'slk',
    'sl': 'slv',
    'sq': 'sqi',
    'sr': 'srp',
    'tr': 'tur',
    'uk': 'ukr'
}


def _get_tesseract():
    languages = '+'.join(LANGUAGES.values())
    if not hasattr(tess, 'instance'):
        tess.instance = tesserwrap.Tesseract(TESSDATA_PREFIX, languages)
        tess.instance.set_page_seg_mode(tesserwrap.PageSegMode.PSM_AUTO_OSD)
    return tess.instance


def _get_languages(languages):
    if languages is None or not len(languages):
        languages = LANGUAGES.values()

    supported = []
    for lang in languages:
        if lang is None or len(lang.strip()) not in [2, 3]:
            continue
        lang = lang.lower().strip()
        if len(lang) == 2:
            if lang not in LANGUAGES:
                continue
            lang = LANGUAGES.get(lang)

        supported.append(lang)

    return '+'.join(sorted(supported))


def _extract_image_wrap(img, languages):
    """ Use an in-instance version of tesseract to extract the OCR
    content. """
    try:
        extractor = _get_tesseract()
        extractor.set_image(img)
        text = extractor.get_utf8_text()
        extractor.clear()
        return text
    except Exception as ex:
        log.exception(ex)
        return ''


def extract_image(path, languages=None):
    """ Use tesseract to extract text in the given ``languages`` from an
    image file. Tesseract should support a wide range of formats, including
    PNG, TIFF and JPG. """
    # TODO: play with contrast and sharpening the images.
    if TESSDATA_PREFIX:
        img = Image.open(path)
        return _extract_image_wrap(img, languages)
    # TODO: find out how to keep tesseract running so it won't need to
    #       reload for each page.

    sysfd, page_dest = mkstemp()
    page_out = '%s.txt' % page_dest
    try:
        languages = _get_languages(languages)
        bin_path = os.environ.get('TESSERACT_BIN', 'tesseract')
        args = [bin_path, path, page_dest, '-l', languages, '-psm', '1']
        subprocess.call(args)
        with open(page_out, 'rb') as fh:
            return fh.read()
    except Exception as ex:
        log.exception(ex)
        return ''
    finally:
        os.close(sysfd)
        if os.path.isfile(page_dest):
            os.unlink(page_dest)
        if os.path.isfile(page_out):
            os.unlink(page_out)


def extract_image_data(data, languages=None):
    """ Extract text from a binary string of data containing an image in
    a commonly-used format. """
    img = Image.open(StringIO(data))
    if TESSDATA_PREFIX:
        return _extract_image_wrap(img, languages)
    else:
        fh, file_path = mkstemp(suffix='.png')
        fh = os.fdopen(fh, 'w')
        img.save(fh, 'PNG')
        fh.close()
        return extract_image(file_path)


if __name__ == '__main__':
    import os
    import thready

    dir_name = '/Users/fl/Code/extractors/test/img'
    # os.environ['TESSDATA_PREFIX'] = '/usr/local/share/tessdata/'
    # os.environ['TESSERACT_BINDINGS'] = 'true'

    def get_files():
        for fn in os.listdir(dir_name):
            if fn.endswith('.png'):
                yield os.path.join(dir_name, fn)

    #for fn in get_files():
    #   print len(extract_image(fn))

    def parse(fn):
        print fn
        print [extract_image(fn)]
        # print [extract_image(fn, force_fork=True)]

    import time
    begin = time.time()
    thready.threaded(get_files(), parse)
    print time.time(), time.time() - begin
