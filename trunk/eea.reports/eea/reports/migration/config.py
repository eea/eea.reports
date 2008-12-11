""" Migration constants
"""
#
# If an old report has more than one attached file, you can define the main
# file for it.
# @param key: <lang>/<report_id>
# @param value: <report_id>/<lang>/<report_file_id>
#
# For example:
# DEFAULT_FILE = {
#    'en/technical_report': 'technical_report/en/report_6.pdf',
#    'fr/the_report': 'the_report/fr/the_report_345.pdf',
# }
#
DEFAULT_FILE = {}
#
# Link to XML file that exports reports to migrate
#
REPORTS_XML = 'http://reports.eea.europa.eu/export_ZReports'
#
# Relations
#
ANNOTATION_REPLACES = '_replaces_'
ANNOTATION_ISREPLACED = '_is_replaced_by_'
ANNOTATION_HASPART = '_haspart_'
ANNOTATION_ISPARTOF = '_is_part_of_'
#
# English version of the folder where reports will be imported
#
REPORTS_CONTAINER = 'publications'
