import os
import logging
import subprocess
from tempfile import mkstemp

log = logging.getLogger(__name__)


# convert in.png -gravity center -page A4 out.pdf
def image_to_pdf(path):
    """ Turn an image into an A4 PDF file. """
    fh, out_path = mkstemp(suffix='.pdf')
    os.close(fh)
    try:
        bin_path = os.environ.get('CONVERT_BIN', 'convert')
        # args = [bin_path, path, '-gravity', 'North', '-page', 'A4', out_path]
        args = [bin_path, path, '-density', '300', '-define',
                'pdf:fit-page=A4', out_path]
        subprocess.call(args)
        return out_path
    except Exception as ex:
        log.exception(ex)
