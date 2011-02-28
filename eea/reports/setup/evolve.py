""" Portal migration scripts
"""
import logging
import transaction
from zLOG import INFO
from StringIO import StringIO
from OFS.Image import File as ZFile
from Products.CMFPlone.setup.SetupBase import SetupWidget
from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('eea.reports.setup')

def evolve1(self, portal):
    """ Update Reports portal_type
    """
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

def evolve2(self, portal):
    """ Migrate Reports files to blobs
    """
    ctool = getToolByName(portal, 'portal_catalog')
    query = {
        'object_provides': 'eea.reports.interfaces.IReportContainerEnhanced',
        'show_inactive': True,
        'Language': 'all'
    }
    brains = ctool(**query)
    logger.info('Migrating %s Publications Files to Blobs ... STARTED',
        len(brains))
    counter = 0
    for brain in brains:
        doc = brain.getObject()

        zfile = getattr(doc, 'file', None)
        if not zfile:
            continue

        if not isinstance(zfile, ZFile):
            continue

        data = StringIO(zfile.data)
        filename = getattr(zfile, 'filename', brain.getId)
        if isinstance(filename, unicode):
            filename = filename.encode('utf-8')
        data.filename = filename

        field = doc.getField('file')
        mutator = field.getMutator(doc)
        kwargs = {'_migration_': True}

        logger.info('Updateing File to Blob for %s', brain.getURL())
        mutator(data, **kwargs)

        counter += 1
        if counter % 25 == 0:
            logger.info('Transaction commit: %s', counter)
            transaction.commit()
        data.close()
    logger.info('Migrating %s Publications Files to Blobs ... DONE', counter)

functions = {
    'Update publications portal_type from Folder to Report': evolve1,
    "Update Publications Files to Blobs": evolve2,
}

class Evolve(SetupWidget):
    """ Portal migration setup category
    """
    type = "EEA Reports"
    description = "EEA Reports updates"

    functions = functions

    def setup(self):
        """ Setup
        """
        pass

    def delItems(self, fns):
        """ Delete upgrade scripts
        """
        out = []
        out.append(('Currently there is no way to remove a function', INFO))
        return out

    def addItems(self, fns):
        """ Add upgrade scripts
        """
        out = []
        for fn in fns:
            self.functions[fn](self, self.portal)
            out.append(('Function %s has been applied' % fn, INFO))
        return out

    def installed(self):
        """ Applied upgrades
        """
        return []

    def available(self):
        """ Go get the functions """
        return self.functions.keys()
