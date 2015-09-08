""" PDF handlers
"""
import logging
from subprocess import Popen, PIPE, STDOUT

logger = logging.getLogger('eea.reports.pdf')

def can_generate_cover_image():
    """ Check if ImageMagik is installed
    """
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

CAN_GENERATE_COVER_IMAGE = can_generate_cover_image()
