from zope.interface import Interface

class IReportPDFParser(Interface):
    """Parser Utility to parse pdf files
    """

    def parse(pdf):
        """ parses the given pdf file and returns a mapping of attributes """
