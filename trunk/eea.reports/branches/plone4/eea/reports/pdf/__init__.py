""" PDF handlers
"""
import logging
from subprocess import Popen, PIPE, STDOUT

logger = logging.getLogger('eea.reports.pdf')

def can_generate_cover_image():
    """ Check if pdftk is installed
    """
    # Test for pdftk
    process = Popen('pdftk --version', shell=True,
                    stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    res = process.stdout.read()
    if 'handy tool' not in res.lower():
        logger.warn(
            ("pdftk NOT FOUND: "
             "Automatic generation of report's cover image is not supported."))
        return False

    # Test for ImageMagik
    process = Popen('convert --version', shell=True,
                    stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    res = process.stdout.read()
    if 'imagemagick' not in res.lower():
        logger.warn(
            ("ImageMagick NOT FOUND: "
             "Automatic generation of report's cover image is not supported."))
        return False
    return True

def can_update_pdf_metadata():
    """ Check if pdftk is installed
    """
    process = Popen('pdftk --version', shell=True,
                    stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
    res = process.stdout.read()
    if 'handy tool' not in res.lower():
        logger.warn("pdftk NOT FOUND: PDF metadata syncronize is not supported")
        return False
    return True

CAN_GENERATE_COVER_IMAGE = can_generate_cover_image()
CAN_UPDATE_PDF_METADATA = can_update_pdf_metadata()
