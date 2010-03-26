""" Report descriptors
"""
from zope import interface
from eea.reports import interfaces
from p4a.subtyper import interfaces as stifaces

class AbstractReportContainerDescriptor(object):
    """ Abstract report descriptor
    """
    interface.implements(stifaces.IPortalTypedFolderishDescriptor)
    title = u'Report'
    description = u'Report file type'
    type_interface = interfaces.IReportContainerEnhanced

class FolderReportContainerDescriptor(AbstractReportContainerDescriptor):
    """ Folder descriptor
    """
    for_portal_type = 'Folder'
