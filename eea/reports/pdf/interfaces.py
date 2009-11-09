from zope.interface import Interface

class IReportPDFParser(Interface):
    """Parser Utility to parse pdf files
    """

    def parse(pdf):
        """ parses the given pdf file and returns a mapping of attributes """

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

class IPDFCoverImage(Interface):
    """ Utility to genrate pdf cover image
    """

    def generate(pdf, width, height):
        """ Generate a cover image from given pdf data stream and return it.

        @param pdf: pdf data stream
        @param width: output image width
        @param height: output image height
        """
