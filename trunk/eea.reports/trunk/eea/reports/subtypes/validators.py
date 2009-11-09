from Products.validation.config import validation
from Products.validation.interfaces import ivalidator

class SerialTitle(object):
    """ Validator for report serial title field.
    """
    __implements__ = (ivalidator,)

    def __init__( self, name, title='', description=''):
        self.name = name
        self.title = title or name
        self.description = description

    def __call__(self, value, instance, *args, **kwargs):
        """ Validate
        """
        report_type = len(value) > 0 and value[0] or 'N/A'
        report_num = len(value) > 1 and value[1] or 0
        report_year = len(value) > 2 and value[2] or -1
        report_alt = len(value) > 3 and value[3] or ''

        # if no report_type then we ignore other fields
        # and the valdation is always true.
        if report_type == 'N/A':
            return 1

        if report_num <= 0:
            return "Please provide a valid value for 'Report number' field"

        if report_year < 1990:
            return "Please provide a valid value for 'Report year' field"

        return 1

validation.register(SerialTitle('serialTitle'))
