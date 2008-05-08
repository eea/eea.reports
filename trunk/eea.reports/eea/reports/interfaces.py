""" Interfaces
"""
from zope.interface import Interface, alsoProvides
from zope.app.content import interfaces as contentifaces

class IAnyReportCapable(Interface):
    """Any aspect of report/content capable.
    """
    
class IPossibleReport(IAnyReportCapable):
    """ All objects that should have the ability to be converted to some
        form of report should implement this interface.
    """

class IReportEnhanced(Interface):
    """ Marker interface for reports
    """

alsoProvides(IReportEnhanced, contentifaces.IContentType)
class IReport(Interface):
    """ Objects which have report information.
    """
