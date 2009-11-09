""" Reports custom widgets.
"""
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Registry import registerWidget

class SerialTitleWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "widgets/serial_title_widget",
    })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker='',
                     emptyReturnsMarker=False, validating=True):
        """ process form """
        name = field.getName()
        report_type = form.get('%s_type' % name, None)
        report_number = form.get('%s_number' % name, None)
        report_year = form.get('%s_year' % name, None)
        report_alt = form.get('%s_alt' % name, None)

        if not (report_type or report_number or report_year or report_alt):
            return empty_marker

        return (report_type, report_number, report_year, report_alt), {}

registerWidget(
    SerialTitleWidget,
    title='Serial Title',
    description=('Renders report serial title'),
    used_for=('eea.reports.subtypes.field.SerialTitleField',)
)
