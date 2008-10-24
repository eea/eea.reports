""" Migrate old zope reports to plone.
"""
from zope.event import notify
from p4a.subtyper.interfaces import ISubtyper
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from Products.LinguaPlone import config
from Products.CMFPlone.utils import _createObjectByType
from Products.LinguaPlone import events
from zExceptions import BadRequest
from Products.statusmessages.interfaces import IStatusMessage
from eea.reports.pdf.interfaces import IPDFMetadataUpdater
from eea.reports.adapter.events import add_image_file
from eea.reports.migration.zReports.parser import (
    get_reports,
    grab_file_from_url,
    get_file_upload
)
from config import DEFAULT_FILE, REPORTS_XML
import logging
logger = logging.getLogger('eea.reports.migration')

class MigrateReports(object):
    """ Class used to migrate reports.
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request

    def _redirect(self, msg):
        """ Set status message and redirect to context absolute_url
        """
        context = getattr(self.context, 'publications', self.context)
        context = getattr(context, 'en', context)
        url = context.absolute_url()
        IStatusMessage(self.request).addStatusMessage(msg, type='info')
        self.request.response.redirect(url)
        return ''
    #
    # Getters
    #
    def _get_container(self, *args, **kwargs):
        """ Creates folder structure to import old reports
        """
        wftool = getToolByName(self.context, 'portal_workflow')
        ctool = getToolByName(self.context, 'portal_catalog')
        site = getattr(self.context, 'SITE', self.context)
        # Add publications folder
        if 'publications' not in site.objectIds():
            site.invokeFactory('Folder',
                               id='publications', title='Publications')
        publications = getattr(site, 'publications')

        # Add default language folder: en
        if 'en' not in publications.objectIds():
            publications.invokeFactory('Folder', id='en', title='Publications')
        en = getattr(publications, 'en')
        canonical = en.getCanonical()

        # Add translation folders for en
        langs = publications.portal_languages.getSupportedLanguages()
        for lang in langs:
            beforeevent = events.ObjectWillBeTranslatedEvent(en, lang)
            notify(beforeevent)
            kwargs[config.KWARGS_TRANSLATION_KEY] = canonical
            kwargs['language'] = lang
            kwargs['title'] = en.Title()
            try:
                ob = _createObjectByType(en.portal_type, publications,
                                         lang, *args, **kwargs)
            except BadRequest:
                continue

            ob.setExcludeFromNav(True)
            try:
                wftool.doActionFor(ob, 'publish')
            except Exception, err:
                logger.warn('Could not publish %s: %s', ob.absolute_url(1), err)

            if ob.getCanonical() != canonical:
                ob.addTranslationReference(canonical)
            ctool.reindexObject(ob)

        en.invalidateTranslationCache()
        # Publish folders
        try:
            wftool.doActionFor(en, 'publish')
        except Exception, err:
            logger.warn('Could not publish %s: %s', en.absolute_url(1), err)
        try:
            wftool.doActionFor(publications, 'publish')
        except Exception, err:
            logger.warn('Could not publish %s: %s',
                        publications.absolute_url(1), err)
        # Reindex objects
        ctool.reindexObject(en)
        ctool.reindexObject(publications)
        # Returns
        return publications
    #
    # Handlers
    #
    def _get_file_url(self, datamodel):
        """ Returns default file url for given datamodel.
        """
        file_urls = datamodel.get('file', {}).keys()
        # Handle empty list
        if not file_urls:
            logger.warn('Skip file property for %s, lang %s: files = %s',
                        datamodel.getId(), datamodel.get('lang'), file_urls)
            return None
        # Handle one file
        if len(file_urls) == 1:
            return file_urls[0]
        # More than one file
        # Check for mapping
        default_url = DEFAULT_FILE.get('%s/%s' % (
            datamodel.get('lang'), datamodel.getId()), None)
        if not default_url:
            logger.warn('Skip file property for %s, lang %s: file = %s',
                        datamodel.getId(), datamodel.get('lang'), file_urls)
            return None

        file_urls = [url for url in file_urls if url.endswith(default_url)]
        if not file_urls:
            return None
        return file_urls[0]

    def _process_datamodel(self, datamodel):
        """ Process datamodel properties before adding new file
        """
        # Handle datamodel file property
        file_url = self._get_file_url(datamodel)
        if not file_url:
            return datamodel

        ctype = 'application/pdf'
        filename = file_url.split('/')[-1]
        # Get pdf file
        data = grab_file_from_url(file_url, ctype, zope=False)
        # Update pdf metadata
        mupdater = getUtility(IPDFMetadataUpdater)
        data = mupdater.update(data, datamodel(all=True))
        datamodel.set('file_file', get_file_upload(data, filename, ctype))

        # Return
        return datamodel
    #
    # Update methods
    #
    def add_report(self, context, datamodel):
        """ Add new report
        """
        report_id = datamodel.getId()
        lang = datamodel.get('lang')

        # Add translation for existing reports
        canonical = None
        for lang_folder in context.objectValues():
            if report_id in lang_folder.objectIds():
                canonical = getattr(lang_folder, report_id).getCanonical()
                break
        if canonical:
            return self.add_translation(canonical, datamodel)

        # Add report if it doesn't exists
        context = getattr(context, lang)
        if report_id not in context.objectIds():
            logger.info('Adding report id: %s lang: %s', report_id, lang)
            report_id = context.invokeFactory('Folder', id=report_id)
        report = getattr(context, report_id)
        report.setLanguage(lang)
        subtyper = getUtility(ISubtyper)
        if not subtyper.existing_type(report) or \
           subtyper.existing_type(report).name != 'eea.reports.FolderReport':
            subtyper.change_type(report, 'eea.reports.FolderReport')
        # Add cover image only in canonical report
        add_image_file(report, datamodel.get('cover_image_file'))
        self.update_properties(report, datamodel)
        return report_id

    def add_translation(self, report, datamodel):
        """ Add a new language for an existing report
        """
        lang = datamodel.get('lang')
        if not report.hasTranslation(lang):
            logger.info('Adding report %s translation: %s',
                        datamodel.getId(), lang)
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
        logger.info('Update report %s properties', report.absolute_url(1))
        datamodel = self._process_datamodel(datamodel)
        form = datamodel()
        report.processForm(data=1, metadata=1, values=form)
        report.setTitle(datamodel.get('title', ''))
        # Publish
        wftool = getToolByName(self.context, 'portal_workflow')
        ctool = getToolByName(self.context, 'portal_catalog')
        try:
            wftool.doActionFor(report, 'publish',
                               comment='Auto published by migration script.')
        except Exception, err:
            logger.warn('Could not publish report %s, lang %s: %s',
                        datamodel.getId(), datamodel.get('lang'), err)
        self.update_additional_files_content(report, datamodel)
        ctool.reindexObject(report)

    def update_additional_files_content(self, report, datamodel):
        """ Add additional files
        """
        file_urls = datamodel.get('file', {})
        default = self._get_file_url(datamodel)
        ctool = getToolByName(self.context, 'portal_catalog')
        wftool = getToolByName(self.context, 'portal_workflow')
        for file_url, file_title in file_urls.items():
            # Skip default file
            if file_url == default:
                continue
            # Add/Edit
            file_obj = grab_file_from_url(file_url, ctype='')
            filename = file_obj.filename
            doc_id = filename.replace('%20', '_')
            if doc_id not in report.objectIds():
                logger.info('Add report: %s additional file: %s',
                            report.absolute_url(1), doc_id)
                doc_id = report.invokeFactory('File', id=doc_id)
            doc = getattr(report, doc_id)
            logger.info('Update additional file %s properties',
                        doc.absolute_url(1))
            doc.processForm(data=1, metadata=1, values={'file_file': file_obj})
            doc.setTitle(file_title)
            # Publish
            try:
                wftool.doActionFor(doc, 'publish',
                    comment='Auto published by migration script.')
            except Exception, err:
                logger.warn('Could not publish file %s: %s',
                            doc.absolute_url(1), err)
            # Reindex
            ctool.reindexObject(doc)
    #
    # Browser interface
    #
    def __call__(self):
        container = self._get_container()
        index = 0
        for index, report in enumerate(get_reports(REPORTS_XML)):
            self.add_report(container, report)
        msg = '%d language reports imported !' % index
        logger.info(msg)
        return self._redirect(msg)
