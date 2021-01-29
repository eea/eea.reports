""" eea.reports viewlets
"""
from Products.CMFCore.interfaces import ISiteRoot
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from eea.versions.browser.viewlets import CanonicalURL as ViewletBase
from plone.app.layout.viewlets import common
from plone.memoize.instance import memoize
from zope.component import getAdapter
from eea.reports.relations.interfaces import IGroupRelations


class CanonicalURL(ViewletBase):
    """ Override to set canonical url for archived objects
    """

    def render(self):
        """ render canonical url
        """
        field = self.context.getField('publication_groups')

        if field.getAccessor(self.context)():
            cat = self.context.portal_catalog
            brains = cat.searchResults(
                publication_groups=self.context.publication_groups[0],
                portal_type="Report", sort_on='effective',
                sort_order='descending'
            )

            if brains:
                canonical_url = brains[0].getURL()
                return u'<link rel="canonical" href="%s" />' % canonical_url

        return super(CanonicalURL, self).render()


class NewerReportVersionsViewlet(common.ViewletBase):
    """ Newer reports versions displayed as a Viewlet
    """
    render = ViewPageTemplateFile('zpt/newer_report.pt')

    @property
    def available(self):
        """ Condition for rendering of this viewlet
        """
        request = self.context.REQUEST
        url_hits = ["publications", "soer", "about-us"]
        url = request.ACTUAL_URL
        for term in url_hits:
            if term in url:
                return True
        return False

    @memoize
    def get_report(self):
        """ Get parent Report if found
        """
        context = self.context
        ptype = context.portal_type
        if ptype == "Report":
            return None
        obj = self.context
        found = False
        while True:
            obj = obj.aq_parent
    	    if not ISiteRoot.providedBy(obj):
                if obj.portal_type == "Report":
                    found = True
                    break
            else:
                found = False
                break
        if not found:
            return None
        return obj

    def is_replaced_by(self):
        """ Retrieve newer versions of given Report
        """
        report = self.get_report()
        if not report:
            return []
        relations = getAdapter(report, IGroupRelations)
        return relations.forward()
