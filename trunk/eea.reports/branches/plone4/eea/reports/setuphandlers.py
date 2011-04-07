""" Various setup
"""
import os
from eea.reports.config import product_globals
from Globals import package_home
from Products.ATVocabularyManager.config import TOOL_NAME as ATVOCABULARYTOOL
from Products.CMFCore.utils import getToolByName
import logging
logger = logging.getLogger('eea.reports: setuphandlers')

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    pass
    if context.readDataFile('eea.reports.txt') is None:
        return

    #TODO Import these from data/vocabularies/
    site = context.getSite()
    vtool = getToolByName(site, 'portal_vocabularies')
    for voc in ['publications_groups', 'report_creators',
                'report_publishers', 'report_types']:
        if voc in vtool.objectIds():
            continue
        vtool.invokeFactory('SortedSimpleVocabulary', id=voc)
