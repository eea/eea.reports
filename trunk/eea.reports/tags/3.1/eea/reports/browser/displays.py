from zope import interface
from zope import component
from eea.reports import interfaces
from eea.reports.relations.interfaces import IGroupRelations

import p4a.z2utils #Patch CMFDynamicViewFTI
from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces
from Products.Five.browser import BrowserView


class ReportContainerView(object):
    """ Default report view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_replaced_by(self):
        return IGroupRelations(self.context).forward()

    def does_replace(self):
        return IGroupRelations(self.context).backward()

class ReportContainerDynamicViews(object):

    interface.implements(cmfdynifaces.IDynamicallyViewable)
    component.adapts(interfaces.IReportContainerEnhanced)

    def __init__(self, context):
        self.context = context # Actually ignored...

    def getAvailableViewMethods(self):
        """Get a list of registered view method names
        """
        return [view for view, name in self.getAvailableLayouts()]

    def getDefaultViewMethod(self):
        """Get the default view method name
        """
        return "report_view"

    def getAvailableLayouts(self):
        """Get the layouts registered for this object.
        """
        return (("report_view", "Report view"),)
