""" Archetypes fields custom validators
"""
from zope.interface import implements
from Products.validation.config import validation
from Products.validation.interfaces.IValidator import IValidator

class SerialTitle(object):
    """ Validator for report serial title field.
    """
    implements(IValidator)

    def __init__(self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, instance, *args, **kwargs):
        """ Validate
        """
        report_type = value[0] if value else 'N/A'
        report_num = value[1] if len(value) > 1 else 0
        report_year = value[2] if len(value) > 2 else - 1

        # if no report_type then we ignore other fields
        # and the valdation is always true.
        if report_type == 'N/A':
            return 1

        if report_num <= 0:
            return "Please provide a valid value for 'Report number' field"

        if report_year < 1990:
            return "Please provide a valid value for 'Report year' field"

        return 1

def register():
    """ Register validators
    """
    validation.register(SerialTitle('serialTitle'))
