""" PDF Syncronizer
"""
from Products.statusmessages.interfaces import IStatusMessage
from zope.component import getUtility
from eea.reports.pdf.interfaces import IPDFMetadataUpdater
from eea.reports.vocabulary import ReportThemesVocabulary

class SyncronizerSupport(object):
    """ PDF Syncronizer support
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def __call__(self):
        """ Check if object can be syncronized
        """
        field = self.context.getField('file')
        if not field:
            return False

        value = field.getAccessor(self.context)()
        if not value:
            return False

        updater = getUtility(IPDFMetadataUpdater)
        return updater._can_convert()

class Syncronizer(object):
    """ Class used to syncronize attached pdf publication with zodb metadata
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def _redirect(self, msg):
        """ Set status message and redirect to context absolute_url
        """
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(self.context.absolute_url())
        return msg

    def _get_themes_labels(self, themes):
        """ Get themes labels
        """
        vocab = ReportThemesVocabulary()
        all_themes = vocab.getDisplayList(self.context)
        return [value for key, value in all_themes if key in themes]

    def _get_metadata(self):
        """ Return context metadata to syncronize with pdf file
        """
        keys = self.context.Schema().keys()
        metadata = {}
        for key in keys:
            field = self.context.getField(key)
            if not field:
                continue

            value = field.getAccessor(self.context)()
            # Fix some metadata
            if key == 'subject':
                metadata['keywords'] = value
            elif key == 'creators':
                metadata['creators_keywords'] = value
            elif key == 'publishers':
                metadata['publishers_keywords'] = value
            elif key == 'language':
                metadata['lang'] = value
            elif key == 'themes':
                metadata['themes'] = self._get_themes_labels(value)
            else:
                metadata[key] = value
        return metadata

    def __call__(self):
        updater = getUtility(IPDFMetadataUpdater)
        metadata = self._get_metadata()

        field = self.context.getField('file')
        if not field:
            self._redirect('There is no PDF publication file attached to syncronize')

        value = field.getAccessor(self.context)()
        if not value:
            self._redirect('There is no PDF publication file attached to syncronize')

        filename = getattr(value, 'filename', self.context.getId())
        pdf = updater.update(str(value), metadata)
        kwargs = {'_migration_': True, 'filename': filename}
        field.getMutator(self.context)(pdf, **kwargs)
        self._redirect('PDF publication file metadata updated')
