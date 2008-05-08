from zope import interface
from p4a.subtyper import interfaces as stifaces
from eea.reports import interfaces

class ReportDescriptor(object):
    interface.implements(stifaces.IPortalTypedDescriptor)

    title = u'Report'
    description = u'Report file type'
    type_interface = interfaces.IReportEnhanced
    for_portal_type = 'File'
