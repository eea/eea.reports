from zope import interface
from zope import component
from eea.reports import interfaces

import p4a.z2utils #Patch CMFDynamicViewFTI
from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces

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
