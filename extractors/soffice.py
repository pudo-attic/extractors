import os
import logging
import threading
import subprocess
from tempfile import mkdtemp, mkstemp

log = logging.getLogger(__name__)

instances = threading.local()


# other formats: http://opengrok.libreoffice.org/s?n=25&start=0&q=PreferredFilter&sort=relevancy&project=core,
def document_to_pdf(path):
    """ OK, this is weird. Converting LibreOffice-supported documents to
    PDF to then use that extractor. """
    work_dir = mkdtemp()
    if not hasattr(instances, 'dir'):
        instances.dir = mkdtemp()
    try:
        bin_path = os.environ.get('SOFFICE_BIN', 'soffice')
        instance_path = '"-env:UserInstallation=file://%s"' % instances.dir
        args = [bin_path, '--convert-to', 'pdf:writer_pdf_Export',
                '--nofirststartwizard', instance_path,
                '--outdir', work_dir,
                '--headless', path]
        subprocess.call(args)
        for out_file in os.listdir(work_dir):
            return os.path.join(work_dir, out_file)
    except Exception as ex:
        log.exception(ex)


def html_to_pdf(path):
    """ OK, this is weirder. Converting HTML to PDF via WebKit. """
    fh, out_path = mkstemp(suffix='.pdf')
    os.close(fh)
    try:
        bin_path = os.environ.get('WKHTMLTOPDF_BIN', 'wkhtmltopdf')
        args = [bin_path, '--disable-javascript', '--no-outline',
                '--no-images', '--quiet', path, out_path]
        subprocess.call(args)
        return out_path
    except Exception as ex:
        log.exception(ex)
