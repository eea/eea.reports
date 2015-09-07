""" Interfaces for PDF handlers
"""
from zope.interface import Interface
from eea.converter.interfaces import IPDFCoverImage
from eea.converter.interfaces import IPDFParser as IReportPDFParser

class IPDFMetadataUpdater(Interface):
    """ Metadata updater utility to update pdf files metadata.
    """

    def update(pdf, metadata):
        """ Update pdf file with given metadata and return it.

        @param pdf: pdf data stream
        @param metadata: a properties mapping dictionary propname: propvalue.
            Example: metadata = {
                'title': 'New pdf file',
                'description': 'This is a loong description ...'
            }
        """

# BBB
__all__ = [
    IPDFCoverImage.__name__,
    IReportPDFParser.__name__,
]
