""" Migrate old zope reports to plone.
"""
import config
from Products.statusmessages.interfaces import IStatusMessage
from eea.reports.migration.zReports.parser import get_reports, cleanup_id

import logging
logger = logging.getLogger('eea.reports.migration')
info = logger.info

class MigrateSerialTitle(object):
    """ Class used to migrate reports.
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.order_xml = config.REPORTS_SERIALTITLE_XML

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
    def _update_serialtitle(self, datamodel, container):
        """ Update documents serial title
        """
        lang = datamodel.get('lang')
        if lang == 'en':
            serial_title_type = datamodel.get('serial_title_type')
            serial_title_number = datamodel.get('serial_title_number')
            serial_title_year = datamodel.get('serial_title_year')
            serial_title_alt = datamodel.get('serial_title_alt')
            report_id = cleanup_id(datamodel.getId())
            container = container.getTranslation(lang)

            if report_id not in container.objectIds():
                logger.warn("Missing report id: %s in %s",
                            report_id, container.absolute_url(1))
                return

            report = getattr(container, report_id)
            report.getField('serial_title').getMutator(report)((serial_title_type, serial_title_number, serial_title_year, serial_title_alt))
            self._reindex(report)
            return 1
        return 0
    #
    # Browser interface
    #
    def __call__(self):
        container = getattr(self.context, config.REPORTS_CONTAINER, None)
        if not container:
            msg = 'You should run @@migrate_reports script first !!!'
            info(msg)
            return self._redirect(msg)

        info('Update reports serial title using xml file: %s', self.order_xml)
        index = 0
        index_udp = 0
        for index, report in enumerate(self.reports):
            if self._update_serialtitle(report, container):
                index_udp += 1

        msg = '%d publications serial title updated !' % index_udp
        info(msg)
        return self._redirect(msg)