from Products.CMFCore.utils import getToolByName

def install(portal):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-eea.reports:default')
    setup_tool.runAllImportSteps()
    return "Ran all import steps."
