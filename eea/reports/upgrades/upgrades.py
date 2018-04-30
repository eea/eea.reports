""" Upgrade steps
"""

import logging

logger = logging.getLogger('eea.reports')

def upgrade_to_85(context):
    """ Manual step for plone.app.caching in order to reimport the profiles
    """
    logger.info('Reimporting steps for plone.app.caching')
    context.runAllImportStepsFromProfile('profile-plone.app.caching:default')
    logger.info('Finished reimporting steps for plone.app.caching')