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
DEFAULT_FILE = {
    'en/technical_report_2007_15': 'technical_report_2007_15/en/%20NEC_Directive_status_report_2006.pdf',
    'en/technical_report_2007_14': 'technical_report_2007_14/en/Tech_report_14_2007_Annual%20EC_LRTAP.pdf',
    'en/eea_report_2006_9': 'eea_report_2006_9/en/annex_ghg2006_1-7.pdf',
    'de/water_assmnt07': 'water_assmnt07/de/water_assmnt07.pdf',
    'en/Technical_report_No_60': 'Technical_report_No_60/en/tech60.pdf',
    'en/technical_report_2008_6': 'technical_report_2008_6/en/Annex%2013%20Description%20of%20the%20EC__s%20national%20registry%20v2.1.pdf',
    'en/Technical_report_No_54': 'Technical_report_No_54/en/tech54.pdf',
    'en/technical_report_2004_2': 'technical_report_2004_2/en/Annex3-Status_reports.pdf',
    'is/water_assmnt07': 'water_assmnt07/is/water_assmnt07is.pdf',
    'en/Technical_report_No_52': 'Technical_report_No_52/en/tech52.pdf',
    'en/technical_report_2006_10': 'technical_report_2006_10/en/Annex_1_-%20EC_GHG_Inventory_report_2006.pdf',
    # 2008
    'en/briefing_2008_1': 'briefing_2008_1/en/EN_Briefing_01-2008.pdf',
    'en/technical_report_2008_7': 'technical_report_2008_7/en/LRTAP-Convention-final_for_www.pdf',
    'en/technical_report_2008_9': 'technical_report_2008_9/en/NEC_Tech-9-2008_final.pdf',
    'en/eea_report_2008_6': 'eea_report_2008_6/en/Energyandenvironmentreport2008.pdf',
    # 2007
    'en/technical_report_2007_6': 'technical_report_2007_6/en/eea_technical_report_6_2007.pdf',
    'en/technical_report_2007_8': 'technical_report_2007_8/en/technical_report_8_2007.pdf',
    'en/technical_report_2007_7': 'technical_report_2007_7/en/Full%20report%20Annual%20European%20Community%20greenhouse%20gas%20inventory%201990-2005%20and%20inventory%20report%202007.pdf',
    'en/state_of_environment_report_2007_1': 'state_of_environment_report_2007_1/en/Belgrade_EN_all_chapters_incl_cover.pdf',
    'en/eea_report_2007_5': 'eea_report_2007_5/en/Greenhouse_gas_emission_trends_and_projections_in_Europe_2007.pdf',
}
#
# Link to XML file that exports reports to migrate
#
REPORTS_XML = 'http://reports-old.eea.europa.eu/export_ZReports'
#
# Link to XML file that exports reports files order
REPORTS_ORDER_XML = 'http://reports-old.eea.europa.eu/export_ZReportsSortOrder'
#
# Link to XML file that exports reports report type, report number and report year
REPORTS_SERIALTITLE_XML = 'http://reports-old.eea.europa.eu/export_ZReportsSortOrder'
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
