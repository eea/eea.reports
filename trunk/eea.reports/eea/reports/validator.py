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
        request = kwargs.get('REQUEST', None)
        form = getattr(request, 'form', None)
        if not form:
            return 1

        file_uploaded = form.get('_file_already_uploaded', False)
        if isinstance(value, FileUpload) and not file_uploaded:
            notify(FileUploadedEvent(instance, value))
            request.form['_file_already_uploaded'] = True
        return 1

validation.register(NewFileUploadValidator('newFileUpload'))
