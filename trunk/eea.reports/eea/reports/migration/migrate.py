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

class MigrateReports(object):
    """ Class used to migrate reports.
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request
    #
    # Getters
    #
    def get_old_reports(self):
        """ Yields old reports
        """
        for report in range(2):
            for lang in ['en', 'fr']:
                yield ReportDataModel(
                    'myreport-%d' % report, lang,
                    title='My report %s %s' % (report, lang),
                    isbn='32234543',
                    serial_title_type='Briefing',
                    serial_title_number=134,
                    serial_title_year=1990)
    
    def _get_container(self, *args, **kwargs):
        """ Creates folder structure to import old reports
        """
        wftool = getToolByName(self.context, 'portal_workflow')
        site = getattr(self.context, 'SITE', self.context)
        # Add publications folder
        if 'publications' not in site.objectIds():
            site.invokeFactory('Folder', id='publications', title='Publications')
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
                ob = _createObjectByType(en.portal_type, publications, lang, *args, **kwargs)
            except BadRequest:
                continue
            
            ob.setExcludeFromNav(True)
            wftool.doActionFor(ob, 'publish')
            
            if ob.getCanonical() != canonical:
                ob.addTranslationReference(canonical)
            en.invalidateTranslationCache()

        # Publish folders
        wftool.doActionFor(en, 'publish')
        wftool.doActionFor(publications, 'publish')
        
        # Returns
        return publications
    #
    # Update methods
    #
    def add_report(self, context, datamodel):
        """ Add new report
        """
        report_id = datamodel.getId()
        lang = datamodel.language()
        
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
        context.invokeFactory('File', id=report_id)
        report = getattr(context, report_id)
        report.setLanguage(lang)
        subtyper = getUtility(ISubtyper)
        subtyper.change_type(report, 'eea.reports.Report')
        self.update_properties(report, datamodel)
        return report_id
    
    def add_translation(self, report, datamodel):
        """ Add a new language for an existing report
        """
        lang = datamodel.language()
        if not report.hasTranslation(lang):
            report.addTranslation(lang)
        
        translated = report.getTranslation(lang)
        subtyper = getUtility(ISubtyper)
        subtyper.change_type(translated, 'eea.reports.Report')
        self.update_properties(translated, datamodel)
    
    def update_properties(self, report, datamodel):
        """ Update report properties
        """
        wftool = getToolByName(self.context, 'portal_workflow')
        form = datamodel()
        report.processForm(values=form)
        report.setTitle(datamodel.get('title', ''))
        wftool.doActionFor(report, 'publish')
    #
    # Browser interface
    #
    def __call__(self):
        container = self._get_container()
        for report in self.get_old_reports():
            self.add_report(container, report)
