""" Migrate old zope reports to plone.
"""
from pprint import pformat
from urllib import urlencode, unquote
from p4a.subtyper.interfaces import ISubtyper
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from zope.app.annotation.interfaces import IAnnotations
from ZODB.PersistentList import PersistentList
from eea.reports.pdf.interfaces import IPDFMetadataUpdater
from eea.reports.adapter.events import add_image_file
from eea.reports.migration.zReports.parser import (
    get_reports,
    grab_file_from_url,
    get_file_upload,
    cleanup_id
)
from eea.reports.config import PUBLICATIONS_SUBOBJECTS
from config import (
    DEFAULT_FILE, REPORTS_XML,
    ANNOTATION_ISREPLACED, ANNOTATION_REPLACES,
    ANNOTATION_HASPART, ANNOTATION_ISPARTOF,
    REPORTS_CONTAINER
)
import logging
logger = logging.getLogger('eea.reports.migration')
info = logger.info

class MigrateReports(object):
    """ Class used to migrate reports.
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.xmlfile = REPORTS_XML
        if request:
            query = {}
            year = self.request.get('year', None)
            if year:
                query['report_year'] = year
            start = self.request.get('start', None)
            if start:
                query['report_from'] = start
            stop = self.request.get('stop', None)
            if stop:
                query['report_to'] = stop
            if query:
                self.xmlfile = '?'.join((self.xmlfile, urlencode(query)))

    def _redirect(self, msg):
        """ Set status message and redirect to context absolute_url
        """
        if not self.request:
            return msg
        context = getattr(self.context, REPORTS_CONTAINER, self.context)
        url = context.absolute_url()
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(url)
    #
    # Getters
    #
    def _get_container(self, *args, **kwargs):
        """ Creates folder structure to import old reports
        """
        site = getattr(self.context, 'SITE', self.context)
        # Add publications folder
        if REPORTS_CONTAINER not in site.objectIds():
            info('Create folder %s/%s', site.absolute_url(1), REPORTS_CONTAINER)
            site.invokeFactory('Folder',
                id=REPORTS_CONTAINER, title=REPORTS_CONTAINER.title())
        publications = getattr(site, REPORTS_CONTAINER)
        publications.setConstrainTypesMode(1)
        publications.setImmediatelyAddableTypes(PUBLICATIONS_SUBOBJECTS)
        publications.setLocallyAllowedTypes(PUBLICATIONS_SUBOBJECTS)

        # Add translation folders for publications
        langs = publications.portal_languages.getSupportedLanguages()
        for lang in langs:
            if lang == 'en':
                continue
            if not publications.getTranslation(lang):
                info('Add %s translation for %s', lang,
                     publications.absolute_url(1))
                publications.addTranslation(lang)
            translated = publications.getTranslation(lang)
            self._publish(translated)

        publications.invalidateTranslationCache()

        # Publish folders
        self._publish(publications)

        # Returns
        return publications

    def _get_file_url(self, datamodel):
        """ Returns default file url for given datamodel.
        """
        file_urls = datamodel.get('file', {}).keys()
        # Handle empty list
        if not file_urls:
            text = pformat(file_urls)
            logger.warn('No file property for %s, lang %s: files = %s',
                        datamodel.getId(), datamodel.get('lang'), text)
            return None
        # Handle one file
        if len(file_urls) == 1:
            return file_urls[0]
        # More than one file
        # Check for mapping
        default_url = DEFAULT_FILE.get('%s/%s' % (
            datamodel.get('lang'), datamodel.getId()), None)
        if not default_url:
            text = pformat(file_urls)
            logger.warn('No default file defined for %s, lang %s: file = %s',
                        datamodel.getId(), datamodel.get('lang'), text)
            return None

        file_urls = [url for url in file_urls if url.endswith(default_url)]
        if not file_urls:
            return None
        return file_urls[0]
    #
    # Handlers
    #
    def _reindex(self, doc):
        """ Reindex document
        """
        ctool = getToolByName(self.context, 'portal_catalog')
        ctool.reindexObject(doc)

    def _publish(self, doc):
        """ Try to publish given document
        """
        wftool = getToolByName(self.context, 'portal_workflow')
        state = wftool.getInfoFor(doc, 'review_state', '(Unknown)')
        if state == 'published':
            return
        try:
            wftool.doActionFor(doc, 'publish',
                               comment='Auto published by migration script.')
        except Exception, err:
            logger.warn('Could not publish %s, state: %s, error: %s',
                        doc.absolute_url(1), state, err)

    def _process_datamodel(self, datamodel):
        """ Process datamodel properties before adding new file
        """
        # Handle datamodel file property
        file_url = self._get_file_url(datamodel)
        if not file_url:
            return datamodel

        ctype = 'application/pdf'
        filename = file_url.split('/')[-1]
        filename = unquote(filename)
        # Get pdf file
        data = grab_file_from_url(file_url, ctype, zope=False)
        # Update pdf metadata
        mupdater = getUtility(IPDFMetadataUpdater)
        data = mupdater.update(data, datamodel(all=True))
        datamodel.set('report_file', get_file_upload(data, filename, ctype))

        # Return
        return datamodel
    #
    # Update methods
    #
    def add_report(self, context, datamodel):
        """ Add new report
        """
        report_id = datamodel.getId()
        report_id = cleanup_id(report_id)
        lang = datamodel.get('lang')

        # Add translation for existing reports
        langs = context.portal_languages.getSupportedLanguages()

        if lang not in langs:
            logger.warn('Skip report id: %s, lang: %s. Language not available.',
                        report_id, lang)
            return

        canonical = None
        for portal_lang in langs:
            pub_tr = context.getTranslation(portal_lang)
            if report_id in pub_tr.objectIds():
                canonical = getattr(pub_tr, report_id).getCanonical()
                break
        if canonical:
            return self.add_translation(canonical, datamodel)

        # Add report if it doesn't exists
        context = context.getTranslation(lang)

        if report_id not in context.objectIds():
            info('Adding report id: %s lang: %s', report_id, lang)
            report_id = context.invokeFactory('Folder', id=report_id)
        report = getattr(context, report_id)
        report.setLanguage(lang)
        subtyper = getUtility(ISubtyper)
        if not subtyper.existing_type(report) or \
           subtyper.existing_type(report).name != 'eea.reports.FolderReport':
            subtyper.change_type(report, 'eea.reports.FolderReport')
        # Add cover image only in canonical report
        cover_image_file = grab_file_from_url(
            datamodel.get('cover_image_file'), zope=False)
        add_image_file(report, cover_image_file)
        self.update_properties(report, datamodel)
        self.update_group_relations(report, datamodel)
        self.update_inclusion_relations(report, datamodel)
        return report_id

    def add_translation(self, report, datamodel):
        """ Add a new language for an existing report
        """
        lang = datamodel.get('lang')
        if not report.hasTranslation(lang):
            info('Adding report %s translation: %s', datamodel.getId(), lang)
            report.addTranslation(lang)

        translated = report.getTranslation(lang)
        subtyper = getUtility(ISubtyper)
        if not subtyper.existing_type(translated) or \
        subtyper.existing_type(translated).name != 'eea.reports.FolderReport':
            subtyper.change_type(translated, 'eea.reports.FolderReport')
        self.update_properties(translated, datamodel)

    def update_properties(self, report, datamodel):
        """ Update report properties
        """
        info('Update report %s properties', report.absolute_url(1))
        report.setExcludeFromNav(True)
        datamodel = self._process_datamodel(datamodel)
        form = datamodel()
        report.processForm(data=1, metadata=1, values=form)
        report.setTitle(datamodel.get('title', ''))
        report_file = datamodel.get('report_file', None)
        if report_file:
            file_field = report.getField('file')
            kwargs = {
                'field': file_field.__name__,
                '_migration_': True
            }
            file_field.getMutator(report)(report_file, **kwargs)

        # Publish
        self._publish(report)

        # Update additional content
        self.update_additional_files_content(report, datamodel)
        self.update_chapters(report, datamodel)
        self.update_images(report, datamodel)

        # Reindex
        self._reindex(report)
        self._reindex(report.getParentNode())

    def update_additional_files_content(self, report, datamodel):
        """ Add additional files
        """
        file_urls = datamodel.get('file', {})
        default = self._get_file_url(datamodel)
        for file_url, file_title in file_urls.items():
            # Skip default file
            if file_url == default:
                continue
            # Add/Edit
            file_obj = grab_file_from_url(file_url, ctype='')
            filename = file_obj.filename

            doc_id = cleanup_id(filename)
            if doc_id not in report.objectIds():
                info('Add report: %s additional file: %s',
                            report.absolute_url(1), doc_id)
                doc_id = report.invokeFactory('File', id=doc_id)
            doc = getattr(report, doc_id)
            info('Update additional file %s properties', doc.absolute_url(1))
            doc.processForm(data=1, metadata=1, values={'file_file': file_obj})
            doc.setTitle(file_title)

            # Publish
            self._publish(doc)

            # Reindex
            self._reindex(doc)

    def update_chapters(self, report, datamodel):
        """ Add additional chapters
        """
        chapters = datamodel.get('chapters', {})
        chapter_keys = chapters.keys()
        chapter_keys.sort()
        for doc_id in chapter_keys:
            value = chapters[doc_id]

            doc_id = cleanup_id(doc_id)
            if doc_id not in report.objectIds():
                logger.debug('Add report: %s chapter: %s',
                             report.absolute_url(1), doc_id)
                doc_id = report.invokeFactory('Document', id=doc_id)
            doc = getattr(report, doc_id)
            logger.debug('Update chapter %s properties', doc.absolute_url(1))
            # Update content
            content = len(value) > 1 and value[1] or ''
            if content:
                doc.processForm(data=1, metadata=1, values={'text': content})
            # Update title
            title = len(value) > 0 and value[0] or doc_id
            if title:
                doc.setTitle(title)

            # Publish
            self._publish(doc)

            # Reindex
            self._reindex(doc)

    def update_images(self, report, datamodel):
        """ Add additional chapters
        """
        images = datamodel.get('images', {})
        for img_id, img_url in images.items():
            logger.debug('Add report: %s image: %s',
                         report.absolute_url(1), img_id)
            img = grab_file_from_url(img_url, zope=False)
            add_image_file(report, img, img_id, '')

    def update_group_relations(self, report, datamodel):
        """ Update publication groups property
        """
        annotations = IAnnotations(report)

        replaces = tuple(datamodel.get('replaces', ()))
        if replaces:
            annotations[ANNOTATION_REPLACES] = PersistentList(replaces)

        is_replaced_by = tuple(datamodel.get('is_replaced_by', ()))
        if is_replaced_by:
            annotations[ANNOTATION_ISREPLACED] = PersistentList(is_replaced_by)

    def update_inclusion_relations(self, report, datamodel):
        """ Update publication related items property
        """
        annotations = IAnnotations(report)

        has_part = tuple(datamodel.get('has_part', ()))
        if has_part:
            annotations[ANNOTATION_HASPART] = PersistentList(has_part)

        is_part_of = tuple(datamodel.get('is_part_of', ()))
        if is_part_of:
            annotations[ANNOTATION_ISPARTOF] = PersistentList(is_part_of)
    #
    # Browser interface
    #
    def __call__(self):
        container = self._get_container()
        index = 0
        info('Import reports using xml file: %s', self.xmlfile)
        for index, report in enumerate(get_reports(self.xmlfile)):
            self.add_report(container, report)
        msg = '%d language reports imported !' % (index + 1)
        info(msg)
        return self._redirect(msg)
