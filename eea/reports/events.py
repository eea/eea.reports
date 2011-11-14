""" New events
"""
from zope.component.interfaces import IObjectEvent
from zope.interface import Attribute, implements

class IFileUploadedEvent(IObjectEvent):
    """ New file uploaded
    """
    object = Attribute("Report object.")

class FileUploadedEvent(object):
    """Sent if a new file was uploaded."""
    implements(IFileUploadedEvent)

    def __init__(self, context, data, update_main=False):
        self.object = context
        self.data = data
        self.update_main = update_main
