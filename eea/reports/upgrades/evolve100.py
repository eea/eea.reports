""" Upgrade to version 10.0
"""
import logging
from Products.CMFCore.utils import getToolByName
from eea.reports.adapter.events import generate_image

logger = logging.getLogger("eea.facetednavigation")


def upgrade_cover(context):
    """ Re-generate all Publication's cover images at a higher resolution
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='Report')

    logger.info("Fixing %s Publication's cover image", len(brains))
    for brain in brains:
        doc = brain.getObject()
        import ipdb; ipdb.set_trace()
        raise NotImplementedError
    logger.info("Done fixing Publications's cover images")
