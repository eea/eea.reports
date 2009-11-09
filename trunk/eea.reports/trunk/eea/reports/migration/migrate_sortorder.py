""" Migrate old zope reports to plone.
"""
import config
from Products.statusmessages.interfaces import IStatusMessage
from eea.reports.migration.zReports.parser import get_reports, cleanup_id

import logging
logger = logging.getLogger('eea.reports.migration')
info = logger.info

class MigrateSortOrder(object):
    """ Class used to migrate reports.
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.order_xml = config.REPORTS_ORDER_XML

    def _redirect(self, msg):
        """ Set status message and redirect to context absolute_url
        """
        context = getattr(self.context, config.REPORTS_CONTAINER, self.context)
        url = context.absolute_url()
        if self.request:
            IStatusMessage(self.request).addStatusMessage(msg, type='info')
            return self.request.response.redirect(url)
        return msg

    def _reindex(self, container):
        """ Reindex container
        """
        container.plone_utils.reindexOnReorder(container)
    #
    # Get reports from XML
    #
    @property
    def reports(self):
        """ Returns a list of report objects (
            eea.reports.migration.zReports.parser.Report).
        """
        return get_reports(self.order_xml)
    #
    # Group relations
    #
    def _update_sortorder(self, datamodel, container):
        """ Update documents relations
        """
        file_order = [cleanup_id(x) for x in datamodel.get('file_order', [])]
        lang = datamodel.get('lang')
        report_id = cleanup_id(datamodel.getId())

        container = container.getTranslation(lang)
        if report_id not in container.objectIds():
            logger.warn("Missing report id: %s in %s",
                        report_id, container.absolute_url(1))
            return

        report = getattr(container, report_id)
        ordered_files = [x for x in file_order if x in report.objectIds()]

        # Log missing files
        diff = set(file_order).difference(ordered_files)
        main_file = cleanup_id(report.getField('file').getFilename(report))
        diff = [x for x in diff if x != main_file]
        if diff:
            logger.warn('Missing file ids %s in report %s', ', '.join(diff),
                        report.absolute_url(1))

        report.moveObjectsByDelta(ordered_files, -len(report._objects))
        self._reindex(report)
    #
    # Browser interface
    #
    def __call__(self):
        container = getattr(self.context, config.REPORTS_CONTAINER, None)
        if not container:
            msg = 'You should run @@migrate_reports script first !!!'
            info(msg)
            return self._redirect(msg)

        info('Update reports files order using xml file: %s', self.order_xml)
        index = 0
        for index, report in enumerate(self.reports):
            self._update_sortorder(report, container)

        msg = '%d publications sortorder updated !' % index
        info(msg)
        return self._redirect(msg)
