""" Base test cases
"""
# the special storage setup needs to be imported first to make sure
# the tests run on top of a `BlobStorage`...
import logging
from StringIO import StringIO
from cgi import FieldStorage

import os

from App.Common import package_home
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase.PloneTestCase import FunctionalTestCase
from Products.PloneTestCase.PloneTestCase import setupPloneSite
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc
from ZPublisher.HTTPRequest import FileUpload
from eea.reports.config import product_globals

try:
    from plone.app.blob.tests import db
except ImportError, err:
    db = None
    logger = logging.getLogger("eea.report")
    logger.debug(err)

logger = logging.getLogger("eea.report")

ztc.installProduct('LinguaPlone')
ztc.installProduct('ATVocabularyManager')
ztc.installPackage('eea.reports')

@property
def blobstorage():
    """ Return blobstorage database """
    return db

@onsetup
def setup_eea_reports():
    """Set up the additional products required for the Report Content.

    The @onsetup decorator causes the execution of this body to be deferred
    until the setup of the Plone site testing layer.
    """
    fiveconfigure.debug_mode = True
    import eea.reports
    zcml.load_config('configure.zcml', eea.reports)

    try:
        import eea.rdfmarshaller
        zcml.load_config('configure.zcml', eea.rdfmarshaller)
    except ImportError:
        logger.warning("Could not import eea.rdfmarshaller")

    fiveconfigure.debug_mode = False


setup_eea_reports()
setupPloneSite(extension_profiles=('eea.reports:default',))

class ReportFunctionalTestCase(FunctionalTestCase):
    """Base class for functional integration tests for the 'Report' product.
    """
    def loadfile(self, rel_filename, ctype='application/pdf'):
        """ load a file
        """
        home = package_home(product_globals)
        filename = os.path.sep.join([home, rel_filename])
        data = open(filename, 'r').read()

        fp = StringIO(data)
        fp.seek(0)

        env = {'REQUEST_METHOD':'PUT'}
        headers = {'content-type' : ctype,
                   'content-length': len(data),
                   'content-disposition':'attachment; filename=test.txt'}

        fs = FieldStorage(fp=fp, environ=env, headers=headers)
        ufile = FileUpload(fs)
        ufile.name = None
        return ufile
