""" Report catalog adapter
"""
import logging
from zope.interface import implements
from interfaces import IReportCatalog
from types import StringTypes, TupleType, ListType, DictType

ListTypes = (TupleType, ListType)
logger = logging.getLogger('eea.reports.search.catalog')

REPORT_INTERFACE = 'eea.reports.interfaces.IReportContainerEnhanced'
REPORT_PORTAL_TYPE = 'Report'

class ReportCatalog(object):
    """ Custom search utility
    """
    implements(IReportCatalog)

    def __init__(self, context):
        self.context = context
    #
    # Private
    #
    def _sort_results(self, brains, sort_on=None, sort_order=None):
        """ Sort results
        """
        sort_on = sort_on and self.context.Indexes.get(sort_on, None)
        if not sort_on:
            return list(brains)

        reverse = 0
        if (isinstance(sort_order, StringTypes) and sort_order.lower() in (
            'reverse', 'descending', u'reverse', u'descending')):
            reverse = 1

        rs = set(brain.getRID() for brain in brains)
        brains = self.context._catalog.sortResults(rs, sort_on, reverse)
        return brains

    def _search_non_report(self, **kwargs):
        """ Search catalog for non reports queries
        """
        query = kwargs.copy()
        portal_type = query.get('portal_type', {})
        portal_type_query = portal_type.get('query', [])

        object_provides = query.get('object_provides', {})
        object_provides_query = object_provides.get('query', [])
        if not portal_type_query:
            query.pop('portal_type', '')
        if not object_provides_query:
            query.pop('object_provides', '')
        brains = self.context.searchResults(**query)

        # Remove reports from Folder query
        if 'Folder' in portal_type_query:
            if REPORT_INTERFACE not in object_provides_query:
                brains = set(
                    brain for brain in brains if REPORT_INTERFACE not in
                    getattr(brain, 'object_provides', [])
                )
        return brains

    def _search_report(self, **kwargs):
        """ Search catalog for reports queries
        """
        brains = set()
        query = kwargs.copy()
        portal_type = query.get('portal_type', {})
        portal_type_query = portal_type.get('query', [])
        portal_type_operator = portal_type.get('operator', 'or').lower()

        # There is no object with more than one portal type
        if portal_type_operator == 'and' and len(portal_type_query) > 1:
            return []
        portal_type_query.remove(REPORT_PORTAL_TYPE)

        object_provides = query.get('object_provides', {})
        object_provides_query = object_provides.get('query', [])

        if REPORT_INTERFACE in object_provides_query:
            if 'Folder' not in portal_type_query:
                portal_type_query.append('Folder')
            return self._search_non_report(**query)

        # Remove empty query
        if not portal_type_query:
            query.pop('portal_type', None)
        if not object_provides_query:
            query.pop('object_provides', None)

        # Search for other portal types
        if portal_type_query:
            brains = set(self._search_non_report(**query))

        # Search for reports
        if not object_provides_query:
            query.pop('portal_type', None)
            query['object_provides'] = REPORT_INTERFACE
            brains.update(set(self.context.searchResults(**query)))

        return brains

    def _index2dict(self, index):
        """ Convert index to search dict
        """
        if isinstance(index, StringTypes):
            return {'query': [index], 'operator': 'or'}
        if isinstance(index, ListTypes):
            return {'query': list(index), 'operator': 'or'}
        if isinstance(index, DictType):
            index.setdefault('operator', 'or')
            query = index.get('query', [])
            query = self._index2list(query)
            index['query'] = query
            return index

        logger.warn('Unknown index type: %s', index)
        return {'query': [], 'operator': 'or'}

    def _index2list(self, index):
        """ Convert index to list
        """
        if not index:
            return []
        if isinstance(index, StringTypes):
            return [index]
        if isinstance(index, TupleType):
            return list(index)
        if isinstance(index, DictType):
            return index.keys()
        return index
    #
    # Public interface
    #
    def searchResults(self, **query):
        """ See interface
        """
        # No sort, will sort manually at end
        sort_on = query.pop('sort_on', None)
        sort_order = query.pop('sort_order', None)

        portal_type = query.pop('portal_type', {})
        portal_type = self._index2dict(portal_type)

        object_provides = query.pop('object_provides', {})
        object_provides = self._index2dict(object_provides)

        search = self._search_non_report
        if REPORT_PORTAL_TYPE in portal_type.get('query', []):
            search = self._search_report

        brains = search(
            portal_type=portal_type, object_provides=object_provides, **query)
        return self._sort_results(brains, sort_on, sort_order)

    __call__ = searchResults
