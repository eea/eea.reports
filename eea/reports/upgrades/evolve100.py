""" Upgrade to version 10.0
"""
import logging
import transaction
from cStringIO import StringIO
from Products.CMFCore.utils import getToolByName
from eea.reports.events import FileUploadedEvent
from eea.reports.adapter.events import generate_image

logger = logging.getLogger("eea.facetednavigation")


def upgrade_cover(context):
    """ Re-generate all Publication's cover images at a higher resolution
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='Report')
    to_do = len(brains)
    logger.info("Fixing %s Publication's cover image", to_do)
    for idx, brain in enumerate(brains):
        doc = brain.getObject()
        data = StringIO(doc.file.data)
        evt = FileUploadedEvent(doc, data)
        generate_image(doc, evt)
        if idx % 100 == 0:
            logger.info("Fixed %s/%s Publication's cover images", idx, to_do)
            transaction.savepoint(optimistic=True)
    logger.info("Done fixing %s Publications's cover images", to_do)
