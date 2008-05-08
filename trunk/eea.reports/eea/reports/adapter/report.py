""" Adapters
"""
from zope import interface
from zope import component
from Products.ATContentTypes import interface as atctifaces

from eea.reports import interfaces

@interface.implementer(interfaces.IReport)
@component.adapter(atctifaces.IATFile)
def ATCTFileReport(context):
    if not interfaces.IReportEnhanced.providedBy(context):
        return None
    return _ATCTReport(context)

_marker=[]

class _ATCTReport(object):
    """ Report
    """
    interface.implements(interfaces.IReport)
    component.adapts(atctifaces.IATFile)

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return '<eea.report %s title="%s">' % (
            self.__class__.__name__, self.context.title)
    __repr__ = __str__
