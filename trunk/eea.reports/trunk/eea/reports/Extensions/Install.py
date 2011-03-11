""" Plone 2 installer
"""
from Products.CMFCore.utils import getToolByName

def install(portal):
    """ Plone 2 installer
    """
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-eea.reports:default')
    setup_tool.runAllImportSteps()
    return "Ran all import steps."
