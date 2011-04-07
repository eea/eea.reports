""" Displayes
"""
from zope.component import getAdapter
from eea.reports.relations.interfaces import IGroupRelations

class ReportContainerView(object):
    """ Default report view
    """
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def is_replaced_by(self):
        """ Is this report replaced by?
        """
        relations = getAdapter(self.context, IGroupRelations)
        return relations.forward()

    def does_replace(self):
        """ Does this report replace other reports?
        """
        relations = getAdapter(self.context, IGroupRelations)
        return relations.backward()
