""" Upgrade to version 10.0
"""
import logging
import transaction
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from eea.reports.adapter.events import generate_image
from eea.reports.async import IAsyncService
logger = logging.getLogger("eea.reports")


def upgrade_cover(context):
    """ Re-generate all Publication's cover images at a higher resolution
    """
    ctool = getToolByName(context, 'portal_catalog')
    brains = ctool.unrestrictedSearchResults(portal_type='Report')
    to_do = len(brains)
    logger.info("Fixing %s Publication's cover image", to_do)

    async_service = queryUtility(IAsyncService)
    for idx, brain in enumerate(brains):
        doc = brain.getObject()

        # Recreate Publications cover asynchronously via zc.async
        if async_service:
            async_queue = async_service.getQueues()['']
            async_service.queueJobInQueue(
                async_queue, ('publications',),
                generate_image,
                doc
            )
        else:
            generate_image(doc)

        if idx % 100 == 0:
            logger.info("Fixing %s/%s Publication's cover images", idx, to_do)
            transaction.savepoint(optimistic=True)

    if async_service:
        logger.info("Fixing %s Publications's cover images schedueled. "
                    "See async logs for more details.", idx)
    else:
        logger.info("Done fixing %s Publications's cover images", idx)
