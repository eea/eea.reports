from eea.rdfmarshaller.interfaces import ISurfSession
from eea.rdfmarshaller.marshaller import ATField2Surf
from zope.component import adapts                                                                                                                                
from eea.reports.subtypes.field import SerialTitleField


class SerialTitle2Surf(ATField2Surf):
    """Base implementation of IATField2Surf"""
    adapts(SerialTitleField, ISurfSession)

    def value(self, context):
        v = self.field.getAccessor(context)()
        if v:
            return " - ".join(v)
        else:
            return None
