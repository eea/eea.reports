""" Adapters
"""
from zope import interface
from zope import component
from Products.ATContentTypes import interface as atctifaces

from eea.reports import interfaces
from eea.reports.config import REPORT_SUBOBJECTS

@interface.implementer(interfaces.IReport)
@component.adapter(atctifaces.IATFolder)
def ATCTReport(context):
    if not interfaces.IPossibleReportContainer.providedBy(context):
        return None
    return _ATCTReport(context)

class _ATCTReport(object):
    """ Report
    """
    interface.implements(interfaces.IReport)
    component.adapts(atctifaces.IATFolder)

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return '<eea.report %s title="%s">' % (
            self.__class__.__name__, self.context.title)
    __repr__ = __str__

    def restrictSubObjects(self, restriction_type=-1):
        """ Restrict report addable sub-objects to File and Link
        """
        self.context.setConstrainTypesMode(restriction_type)
        if restriction_type != 1:
            return
        self.context.setImmediatelyAddableTypes(REPORT_SUBOBJECTS)
        self.context.setLocallyAllowedTypes(REPORT_SUBOBJECTS)
