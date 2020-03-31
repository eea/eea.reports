""" Displayes
"""
from zope.annotation import IAnnotations
from zope.component import getAdapter
from eea.reports.relations.interfaces import IGroupRelations
from Products.Five import BrowserView

class ReportContainerView(BrowserView):
    """ Default report view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_replaced_by(self):
        """ Is this report replaced by?
        """
        relations = getAdapter(self.context, IGroupRelations)
        return relations.forward()

    def does_replace(self):
        """ Does this report replace other reports?
        """
        relations = getAdapter(self.context, IGroupRelations)
        return relations.backward()

    @property
    def serial_title(self):
        """ Compute serial title for display
        """
        field = self.context.getField('serial_title')
        if field.is_empty(self.context):
            return ''

        value = field.getAccessor(self.context)()

        alt = value[3] if len(value) > 3 else ''
        if alt:
            return alt

        vocab = field.Vocabulary(self.context)
        rtype = vocab.getValue(value[0]) if value else ''
        number = value[1] if len(value) > 1 else 0
        year = value[2] if len(value) > 2 else -1

        text = rtype

        if text is None:
            text = value[0]

        if number:
            text += " No %s" % number

        if year != -1:
            text += "/%s" % year

        return text

    @property
    def publishers(self):
        """ Compute publishers to be displayed
        """
        field = self.context.getField('publishers')
        value = field.getAccessor(self.context)()
        vocab = field.Vocabulary(self.context)

        for publisher in value:
            yield vocab.getValue(publisher, publisher)

    @property
    def report(self):
        """ Report file
        """
        field = self.context.getField('file')
        return field.getAccessor(self.context)()

    @property
    def filename(self):
        """ Report filename
        """
        size = self.report.get_size()
        if not size:
            return ''

        field = self.context.getField('file')
        filename = field.getFilename(self.context)
        return filename if filename else self.context.pretty_title_or_id()

    @property
    def size(self):
        """ Report file size
        """
        return self.report.getObjSize(self.report)

    @property
    def items(self):
        """ Files children
        """
        return self.context.getFolderContents({
            'portal_type': ['Document', 'File', 'Link', 'Folder']
        })

    @property
    def has_children(self):
        """ Report has children?
        """
        return self.size or self.items

    def is_pdf(self):
        """ Report file is pdf?
        """
        if hasattr(self.context, 'getFile'):
            file = self.context.getFile()
        else:
            file = self.context.file
        return file.getContentType() in ['application/pdf']

    def check_pdf_metadata(self):
        """ Verify if the PDF metadata title is equal with the one from Plone
        """
        anno = IAnnotations(self.context)
        metadata_title = anno.get('pdf.metadata.title', None)

        if metadata_title and metadata_title != self.context.Title():
            return metadata_title
        else:
            return None


class ReportContainerDownload(BrowserView):
    """ Report download
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """ Download
        """
        field = self.context.getField('file')
        return field.download(self.context, self.request, self.request.response)


class ReportContainerViewPdf(BrowserView):
    """ Report View Pdf File
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        """ View
        """
        field = self.context.getField('file')
        file = self.context.file
        fname = field.getFilename(self.context)
        resp = self.request.RESPONSE

        resp.setHeader('Filename', fname)
        resp.setHeader('Content-Disposition', 'inline; filename="%s"' % fname)
        if 'isFirstRequest' in self.request.form.keys():
            return resp        

        resp.setHeader('Content-Type', 'application/pdf')
        return file
