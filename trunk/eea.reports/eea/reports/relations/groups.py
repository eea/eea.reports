""" Relations by group
"""
from Products.CMFCore.utils import getToolByName
from DateTime import DateTime

from interfaces import IGroupRelations
from zope.interface import implements

class GroupRelations(object):
    """ Relations by group
    """
    implements(IGroupRelations)

    def __init__(self, context, group_field='publication_groups'):
        self.context = context
        self.group = group_field
        effective = self.context.getEffectiveDate()
        if not effective or effective.lessThan(DateTime('1990/01/01')):
            effective = self.context.created()
        self.effective = effective

    def backward(self):
        """ Get older references """
        membershipTool = getToolByName(self.context, 'portal_membership')
        anon = membershipTool.isAnonymousUser()
        refs = []
        for ref in self.references():
            state = ref.review_state
            if (anon and state == 'published') or (not anon):
                ref_effective = ref.effective
                if ref_effective.lessThan(DateTime('1990/01/01')):
                    ref_effective = ref.created
                if ref_effective.lessThan(self.effective):
                    refs.append(ref)
        return refs

    def forward(self):
        """ Get newer references """
        membershipTool = getToolByName(self.context, 'portal_membership')
        anon = membershipTool.isAnonymousUser()
        refs = []
        for ref in self.references():
            state = ref.review_state
            if (anon and state == 'published') or (not anon):
                ref_effective = ref.effective
                if ref_effective.lessThan(DateTime('1990/01/01')):
                    ref_effective = ref.created
                if ref_effective.greaterThan(self.effective):
                    refs.append(ref)
        return refs

    def references(self):
        """ Gets both forward and backward references. """
        gfield = self.context.getField(self.group)
        if not gfield:
            return []

        groups = gfield.getAccessor(self.context)()
        if not groups:
            return []

        mtool = getToolByName(self.context, 'portal_membership')
        show_inactive = mtool.checkPermission('Access inactive portal content',
                                              self.context)

        catalog = getToolByName(self.context, 'portal_catalog')
        query = {
            'object_provides': 'eea.reports.interfaces.IReportContainerEnhanced',
            'portal_type' : self.context.portal_type,
            self.group: groups,
            'sort_on': 'effective',
            'sort_order': 'reverse',
            'Language': self.context.getLanguage(),
            'effectiveRange': DateTime(),
            'show_inactive': show_inactive,
        }

        return catalog.searchResults(**query)
