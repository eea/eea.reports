""" Reports custom widgets.
"""
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

class SerialTitleWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "widgets/serial_title",
    })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker='',
                     emptyReturnsMarker=False, validating=True):
        """ process form """
        name = field.getName()
        report_type = form.get('%s_type' % name, empty_marker)
        report_number = form.get('%s_number' % name, empty_marker)
        report_year = form.get('%s_year' % name, empty_marker)
        report_alt = form.get('%s_alt' % name, empty_marker)
        if report_alt:
            return (u'N/A', 0, -1, report_alt), {}
        return (report_type, report_number, report_year, u''), {}

registerWidget(
    SerialTitleWidget,
    title='Serial Title',
    description=('Renders report serial title'),
    used_for=('eea.reports.field.SerialTitleField',)
)
