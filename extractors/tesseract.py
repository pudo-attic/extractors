import os
import shutil
import logging
import subprocess
from tempfile import mkstemp, mkdtemp


log = logging.getLogger(__name__)

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


def extract_image(path, languages=None):
    """ Use tesseract to extract text in the given ``languages`` from an
    image file. Tesseract should support a wide range of formats, including
    PNG, TIFF and JPG. """
    # TODO: find out how to keep tesseract running so it won't need to
    #       reload for each page.
    # TODO: play with contrast and sharpening the images.
    sysfd, page_dest = mkstemp()
    page_out = '%s.txt' % page_dest
    try:
        if languages is not None or not len(languages):
            languages = LANGUAGES.keys()
        languages = [l[:2].lower() for l in languages]
        languages = [LANGUAGES.get(l) for l in languages]
        languages = [l for l in languages if l is not None]
        languages = '+'.join(languages)
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


def extract_image_pdf(path, languages=None):
    """ Split up a PDF into pages and process each page through tesseract. """
    file_name = os.path.basename(path)
    work_dir = mkdtemp()
    work_prefix = os.path.join(work_dir, file_name)
    try:
        bin_path = os.environ.get('PDFTOPPM_BIN', 'pdftoppm')
        args = [bin_path, '-png', path, work_prefix]
        subprocess.call(args)
        for image_file in os.listdir(work_dir):
            image_path = os.path.join(work_dir, image_file)
            yield extract_image(image_path, languages=languages)
    except Exception as ex:
        log.exception(ex)
    finally:
        if os.path.isdir(work_dir):
            shutil.rmtree(work_dir)
