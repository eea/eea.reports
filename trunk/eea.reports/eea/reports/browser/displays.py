from zope import interface
from zope import component
from eea.reports import interfaces

import p4a.z2utils #Patch CMFDynamicViewFTI
from Products.CMFDynamicViewFTI import interfaces as cmfdynifaces
from Products.Five.browser import BrowserView
try:
    from Products.PloneFlashUpload.browser import DisplayUploadView as FlashView
except ImportError:
    class FlashView(BrowserView):
        @property
        def can_upload(self):
            return False

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

class DisplayUploadView(FlashView):
    """Returns True or False depending on whether the upload tab is allowed
    to be displayed on the current context.
    """
    @property
    def os_can_upload(self):
        """ PloneFlashUpload product crash browser
        """
        can_upload = self.can_upload
        if not can_upload:
            return False

        # PloneFlashUpload works only on windows, so disable it on Linux/Mac
        user_agent = self.request.get('HTTP_USER_AGENT', '')
        if 'windows' not in user_agent.lower():
            return False

        return can_upload

    def __call__(self):
        return self.os_can_upload
