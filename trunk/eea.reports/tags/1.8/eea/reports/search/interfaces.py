from zope import interface

class IReportCatalog(interface.Interface):
    """
    Custom search adapter that returns report objects when searching for
    portal_type=Report even if all report files are folders subtyped as reports
    (marked with interface eea.reports.interfaces.IReportContainerEnhanced).

    >>> from eea.reports.search.interfaces import IReportCatalog
    >>> from Products.CMFCore.utils import getToolByName
    >>> ctool = getToolByName(portal, 'portal_catalog')
    >>> catalog = IReportCatalog(ctool)
    >>> brains = catalog.searchResults(portal_type='Report')
    """
    def searchResults():
        """
        Use this method instead of portal_catalog.searchResults if you want
        to get reports when searching for portal_type=Report
        """

    def __call__():
        """ Same as searchResults
        """
