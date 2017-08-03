""" eea.reports viewlets
"""
from eea.versions.browser.viewlets import CanonicalURL as ViewletBase
from zope.component import getMultiAdapter
from zope.component import queryAdapter


class CanonicalURL(ViewletBase):
    """ Override to set canonical url for archived objects
    """

    def render(self):
        """ render canonical url
        """

        if self.context.getField('publication_groups').getAccessor(self.context)():
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
