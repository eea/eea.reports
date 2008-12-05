""" Migrate old zope reports to plone.
"""
import config
from zope.app.annotation.interfaces import IAnnotations
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage

import logging
logger = logging.getLogger('eea.reports.migration')

class MigrateGroupRelations(object):
    """ Class used to migrate reports.
    """
    def __init__(self, context, request=None):
        self.context = context
        self.request = request
        self.already_updated = []

    def _redirect(self, msg):
        """ Set status message and redirect to context absolute_url
        """
        context = getattr(self.context, config.REPORTS_CONTAINER, self.context)
        url = context.absolute_url()
        if self.request:
            IStatusMessage(self.request).addStatusMessage(msg, type='info')
            return self.request.response.redirect(url)
        return msg

    def _update_relations(self, container):
        """ Update documents relations
        """
        for doc in container.objectValues():
            if doc.getId() in self.already_updated:
                continue
            doc_relations = self._get_doc_relations(doc, container)
            self._update_doc_relations(doc_relations)
            self.already_updated += [x.getId() for x in doc_relations]

    def _get_doc_relations(self, doc, parent):
        """ Return all doc relations and related doc relations
        """
        res = set([doc,])
        anno = IAnnotations(doc)

        replaces = set(anno.pop(config.ANNOTATION_REPLACES, []))
        is_replaced = set(anno.pop(config.ANNOTATION_ISREPLACED, []))
        replaces.update(is_replaced)
        if not replaces:
            return res

        for rep in replaces:
            related = getattr(parent, rep, None)
            if not related:
                continue
            res.update(self._get_doc_relations(related, parent))
        return res

    def _update_doc_relations(self, docs):
        """ Update document relations
        """
        # A relation should contain at least 2 elements
        if len(docs) <= 1:
            return

        # Add item in vocabulary
        vtool = getToolByName(self.context, 'portal_vocabularies')
        vocab = vtool['publications_groups']
        terms = [doc.getId() for doc in docs]
        terms.sort()
        term = terms[0]
        try:
            vocab.createTerm(term, title=term)
        except Exception, err:
            logger.error('COULD NOT add %s to publications_groups vocabulary: %s', term, err)
        else:
            logger.info('Added %s to publications_groups vocabulary', term)

        term = (term,)
        for doc in docs:
            logger.info('Update %s publications_groups with %s', doc.getId(), term)
            doc.getField('publication_groups').getMutator(doc)(term)
    #
    # Browser interface
    #
    def __call__(self):
        container = getattr(self.context, config.REPORTS_CONTAINER, None)
        if not container:
            msg = 'You should run @@migrate_reports script first !!!'
            logger.info(msg)
            return self._redirect(msg)
        self._update_relations(container)

        msg = 'Publications relations updated !'
        logger.info(msg)
        return self._redirect(msg)
