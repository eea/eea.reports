""" New events
"""
from zope.app.event.interfaces import IObjectEvent
from zope.interface import Attribute, implements

class IFileUploadedEvent(IObjectEvent):
    """ New file uploaded
    """
    object = Attribute("Report object.")

class FileUploadedEvent(object):
    """Sent if a new file was uploaded."""
    implements(IFileUploadedEvent)

    def __init__(self, context, data):
        self.object = context
        self.data = data

