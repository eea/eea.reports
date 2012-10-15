"""eea.rdfmarshaller customizations for eea.reports
"""

from eea.rdfmarshaller.archetypes.fields import ATField2Surf
from eea.rdfmarshaller.interfaces import ISurfSession
from eea.reports.subtypes.field import SerialTitleField
from zope.component import adapts
from zope.interface import Interface


class SerialTitle2Surf(ATField2Surf):
    """Base implementation of IATField2Surf"""

    adapts(SerialTitleField, Interface, ISurfSession)

    def value(self):
        """returns the value"""

        v = self.field.getAccessor(self.context)()
        if v:
            return " - ".join(str(x).strip() for x in v if x is not None)
        else:
            return None
