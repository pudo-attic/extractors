import os
import logging
import subprocess
from tempfile import mkstemp


log = logging.getLogger(__name__)
CONVERT_BIN = os.environ.get('CONVERT_BIN', 'convert')


def image_to_pdf(path):
    """Turn an image into an A4 PDF file."""
    fh, out_path = mkstemp(suffix='.pdf')
    os.close(fh)
    try:
        args = [CONVERT_BIN, path, '-density', '300', '-define',
                'pdf:fit-page=A4', out_path]
        subprocess.call(args)
        return out_path
    except Exception as ex:
        log.exception(ex)
