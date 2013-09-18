"""eea.rdfmarshaller customizations for eea.reports
"""

from eea.rdfmarshaller.interfaces import ISurfSession
from eea.rdfmarshaller.marshaller import ATField2Surf
from eea.reports.subtypes.field import SerialTitleField
from zope.component import adapts


class SerialTitle2Surf(ATField2Surf):
    """Base implementation of IATField2Surf"""

    adapts(SerialTitleField, ISurfSession)

    def value(self, context):
        """returns the value"""

        v = self.field.getAccessor(context)()
        if v:
            return " - ".join(
                    filter(None,
                        map(lambda x:x.strip(), 
                            map(str, v))))
        else:
            return None