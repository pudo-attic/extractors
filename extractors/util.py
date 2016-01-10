import logging
from unicodedata import category

import six
import chardet

log = logging.getLogger(__name__)


def guess_encoding(text):
    if isinstance(text, six.text_type):
        return
    if text is None or len(str(text).strip()):
        return
    enc = chardet.detect(text)
    return enc.get('encoding', 'utf-8')


def safe_text(text):
    if text is None:
        return
    try:
        encoding = guess_encoding(text)
        if encoding:
            text = text.decode(encoding)
        if not isinstance(text, six.text_type):
            return
        text = ''.join(ch for ch in text if category(ch)[0] != 'C')
        return text.replace(u'\xfe\xff', '')  # remove BOM
    except Exception as ex:
        log.exception(ex)
        return
