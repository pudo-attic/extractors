import os
import logging
import subprocess
from tempfile import mkdtemp

log = logging.getLogger(__name__)


# other formats: http://opengrok.libreoffice.org/s?n=25&start=0&q=PreferredFilter&sort=relevancy&project=core,
def document_to_pdf(path):
    """ OK, this is weird. Converting LibreOffice-supported documents to
    PDF to then use that extractor. """
    work_dir = mkdtemp()
    try:
        bin_path = os.environ.get('SOFFICE_BIN', 'soffice')
        args = [bin_path, '--convert-to', 'pdf:writer_pdf_Export',
                '--outdir', work_dir,
                '--headless', path]
        subprocess.call(args)
        for out_file in os.listdir(work_dir):
            return os.path.join(work_dir, out_file)
    except Exception as ex:
        log.exception(ex)
