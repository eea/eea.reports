""" Various setup
"""
from Products.CMFCore.utils import getToolByName
from eea.reports.config import VOCABULARIES
from Products.ATVocabularyManager.utils.vocabs import createSimpleVocabs

def installVocabularies(context):
    """creates/imports the atvm vocabs."""
    if context.readDataFile('eea.reports.txt') is None:
        return

    site = context.getSite()
    atvm = getToolByName(site, 'portal_vocabularies')
    createSimpleVocabs(atvm, VOCABULARIES)
