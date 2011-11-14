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

class PublicationReportContainerDescriptor(AbstractReportContainerDescriptor):
    """ Publication descriptior
    """
    for_portal_type = 'Report'
