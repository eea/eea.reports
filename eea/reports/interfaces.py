""" Interfaces
"""

from zope.interface import Interface

class IAnyReportCapable(Interface):
    """Any aspect of report/content capable.
    """

class IPossibleReportContainer(IAnyReportCapable):
    """ All objects that should have the ability to be converted to some
        form of report should implement this interface.
    """

class IReportContainerEnhanced(Interface):
    """ Marker interface for reports
    """
