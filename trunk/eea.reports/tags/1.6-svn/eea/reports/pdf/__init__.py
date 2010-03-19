# empty
import os
import logging

logger = logging.getLogger('eea.reports.pdf')

def can_generate_cover_image():
    """ Check if pdftk is installed
    """
    # Test for pdftk
    f_in, f_out = os.popen4('pdftk --version')
    res = f_out.read()
    if 'handy tool' not in res.lower():
        logger.warn("pdftk NOT FOUND: Automatic generation of report's cover image is not supported.")
        return False

    # Test for ImageMagik
    f_in, f_out = os.popen4('convert --version')
    res = f_out.read()
    if 'imagemagick' not in res.lower():
        logger.warn("ImageMagick NOT FOUND: Automatic generation of report's cover image is not supported.")
        return False

    logger.info("Automatic generation of report's cover image is supported.")
    return True

def can_update_pdf_metadata():
    """ Check if pdftk is installed
    """
    f_in, f_out = os.popen4('pdftk --version')
    res = f_out.read()
    if 'handy tool' in res.lower():
        logger.info('PDF metadata syncronize is supported.')
        return True
    logger.warn("pdftk NOT FOUND: PDF metadata syncronize is not supported.")
    return False

CAN_GENERATE_COVER_IMAGE = can_generate_cover_image()
CAN_UPDATE_PDF_METADATA = can_update_pdf_metadata()
