""" Various setup
"""
import logging
from Products.ATVocabularyManager.types.simple import SimpleVocabulary
from Products.CMFCore.utils import getToolByName
from eea.reports.config import VOCABULARIES
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs
logger = logging.getLogger('eea.reports')

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    if context.readDataFile('eea.reports.txt') is None:
        return

    site = context.getSite()
    atvm = getToolByName(site, 'portal_vocabularies')

    # Cleanup broken vocabularies
    for name in VOCABULARIES:
        voc = getattr(atvm, name, None)
        if not voc:
            continue

        if isinstance(voc, SimpleVocabulary):
            continue

        logger.info("Deleting old broken portal_vocabularies/%s", name)
        voc.manage_delObjects(voc.objectIds())
        atvm.manage_delObjects([name, ])

    # Adding vocabularies
    createSimpleVocabs(atvm, VOCABULARIES)
