from zope.event import notify

from ZPublisher.HTTPRequest import FileUpload
from Products.validation.interfaces import ivalidator
from Products.validation.config import validation
from eea.reports.events import FileUploadedEvent


class NewFileUploadValidator:
    __implements__ = (ivalidator,)

    def __init__( self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, instance, *args, **kwargs):
        if isinstance(value, FileUpload):
            notify(FileUploadedEvent(instance, value))
        return 1

validation.register(NewFileUploadValidator('newFileUpload'))
