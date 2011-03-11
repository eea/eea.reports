""" Displayes
"""
from zope import interface
from zope import component
from eea.reports import interfaces
from eea.reports.relations.interfaces import IGroupRelations
from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces

class ReportContainerView(object):
    """ Default report view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_replaced_by(self):
        """ Is this report replaced by?
        """
        return IGroupRelations(self.context).forward()

    def does_replace(self):
        """ Does this report replace other reports?
        """
        return IGroupRelations(self.context).backward()

class ReportContainerDynamicViews(object):
    """ Dynamic views for Report
    """
    interface.implements(cmfdynifaces.IDynamicallyViewable)
    component.adapts(interfaces.IReportContainerEnhanced)

    def __init__(self, context):
        self.context = context # Actually ignored...

    def getAvailableViewMethods(self):
        """Get a list of registered view method names
        """
        return [view[0] for view in self.getAvailableLayouts()]

    def getDefaultViewMethod(self):
        """Get the default view method name
        """
        return "report_view"

    def getAvailableLayouts(self):
        """Get the layouts registered for this object.
        """
        return (("report_view", "Report view"),)
