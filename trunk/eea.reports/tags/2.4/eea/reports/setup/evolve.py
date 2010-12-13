import logging
import transaction
from zLOG import INFO
from Products.CMFPlone.setup.SetupBase import SetupWidget
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('eea.reports.setup')

def evolve1(self, portal):
    ctool = getToolByName(portal, 'portal_catalog')
    query = {
        'object_provides': 'eea.reports.interfaces.IReportContainerEnhanced',
        'show_inactive': True,
        'Language': 'all'
    }

    brains = ctool(**query)
    logger.info('Updating %s publications portal_type ...', len(brains))
    counter = 0
    for brain in brains:
        if brain.portal_type == 'Report':
            continue

        doc = brain.getObject()
        logger.info('Changing portal_type for: %s', brain.getURL())
        doc.portal_type = 'Report'
        doc.reindexObject(idxs=['portal_type'])

        counter += 1
        if counter % 25 == 0:
            logger.info('Transaction commit: %s', counter)
            transaction.commit()
    logger.info('Updating publications portal_type ... DONE')

functions = {
    'Update publications portal_type from Folder to Report': evolve1
}

class Evolve(SetupWidget):
    type = "EEA Reports"
    description = "EEA Reports updates"

    functions = functions

    def setup(self):
        pass

    def delItems(self, fns):
        out = []
        out.append(('Currently there is no way to remove a function', INFO))
        return out

    def addItems(self, fns):
        out = []
        for fn in fns:
            self.functions[fn](self, self.portal)
            out.append(('Function %s has been applied' % fn, INFO))
        return out

    def installed(self):
        return []

    def available(self):
        """ Go get the functions """
        return self.functions.keys()
