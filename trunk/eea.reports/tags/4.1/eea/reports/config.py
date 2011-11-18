""" Config
"""
__author__ = """European Environment Agency <alin.voinea@eaudeweb.ro>"""
__docformat__ = 'plaintext'

PROJECTNAME = "eea.reports"
product_globals = globals()

AUTHOR = u"European Environment Agency"
DEFAULT_ADD_CONTENT_PERMISSION = "Add portal content"
COPYRIGHTS = u'(c) Copyrights - EEA (European Environment Agency)'

STARTING_YEAR = 1990

VOCABULARIES = {
  'publications_groups': (
    ('airpollutionbyozone', 'Air pollution by ozone'),
    ('climate_report_2_2004', 'Climate impacts and trends'),
    ('corporate_document_2007_5', 'EEA accounts'),
    ('technical_report_2002_75', 'EC Greenhouse Gas Inventory'),
    ('Emissions_trading_directive', 'Emissions Trading Directive'),
    ('EMEPCORINAIR', 'EMEP/CORINAIR Emission Inventory Guidebook'),
    ('energyandenvironment', 'Energy and environment'),
    ('Eionetprioritydataflows', 'Eionet priority data flows'),
    ('eea_report_2007_5', 'Greenhouse gas emission trends and projections'),
    ('technical_report_2006_8', 'LRTAP Convention Emission Inventory'),
    ('LandCoverAnnualtopicupdates', 'Land Cover - Annual topic updates'),
    ('eea_report_2006_4', 'Mediterranean environment'),
    ('nature_conservation', 'Nature Conservation'),
    ('NEC_directive_status', 'NEC directive status'),
    ('92-826-5409-5', 'Pan-European state of the environment reports'),
    ('qualityofbathingwater', 'Quality of bathing water'),
    ('state_of_the_environment_reports_soer',
        'State of the environment reports'),
    ('environmental_assessment_report_2002_9', 'Signals'),
    ('ENVISSUENo12', 'TERM reports'),
  ),
  'publications_groups_active': (
      ('airpollutionbyozone', 'Air pollution by ozone'),
      ('climate_report_2_2004', 'Climate impacts and trends'),
      ('technical_report_2002_75', 'EU Greenhouse Gas Inventory'),
      ('Emissions_trading_directive', 'Emissions Trading Directive'),
      ('EMEPCORINAIR', 'EMEP/EEA Emission Inventory Guidebook'),
      ('energyandenvironment', 'Energy and environment'),
      ('Eionetprioritydataflows', 'Eionet priority data flows'),
      ('eea_report_2007_5', 'Greenhouse gas emission trends and projections'),
      ('technical_report_2006_8', 'EU LRTAP Convention Emission Inventory'),
      ('eea_report_2006_4', 'Mediterranean environment'),
      ('NEC_directive_status', 'NEC directive status'),
      ('92-826-5409-5', 'Pan-European state of the environment reports'),
      ('qualityofbathingwater', 'Quality of bathing water'),
      ('environmental_assessment_report_2002_9', 'Signals'),
      ('state_of_the_environment_reports_soer',
       'State of the environment reports'),
      ('ENVISSUENo12', 'TERM reports'),
  ),
  'report_creators': (
    ("term.eea_european_environment_agency",
     "EEA (European Environment Agency)"),
    ("term.who_world_health_organization",
     "WHO (World Health Organization)"),
    ("term.unep_united_nations_environment_programme",
     "UNEP (United Nations Environment Programme)"),
    ("term.eurostat_the_eu_statistical_office",
     "Eurostat (the EU statistical office)"),
    ("term.dg_tren_eu_directorate_general_on_energy_and_transport",
     "DG TREN (EU Directorate General on Energy and Transport)"),
    ("term.dg_env_eu_directorate_general_on_environment",
     "DG ENV (EU Directorate General on Environment)"),
    ("term.etc_acc_european_topic_centre_on_air_and_climate_change",
     "ETC/ACC (European Topic Centre on Air and Climate Change)"),
    ("term.etc_ae_european_topic_centre_on_air_emissions",
     "ETC/AE (European Topic Centre on Air Emissions)"),
    ("term.etc_aq_european_topic_centre_on_air_quality",
     "ETC/AQ (European Topic Centre on Air Quality)"),
    ("term.etc_cds_european_topic_centre_on_catalogue_of_data_sources",
     "ETC/CDS (European Topic Centre on Catalogue of Data Sources)"),
    ("term.etc_iw_european_topic_centre_on_inland_waters",
     "ETC/IW (European Topic Centre on Inland Waters)"),
    ("term.etc_lc_european_topic_centre_on_land_cover",
     "ETC/LC (European Topic Centre on Land Cover)"),
    ("term.etc_mce_european_topic_centre_on_marine_and_coastal_environment",
     "ETC/MCE (European Topic Centre on Marine and Coastal Environment)"),
    ("term.etc_nc_european_topic_centre_on_nature_conservation",
     "ETC/NC (European Topic Centre on Nature Conservation)"),
    ("term.etc_w_european_topic_centre_on_waste",
     "ETC/W (European Topic Centre on Waste)"),
    ("term.etc_te_european_topic_centre_on_terrestrial_environment",
     "ETC/TE (European Topic Centre on Terrestrial Environment)"),
    ("term.etc_npb_european_topic_centre_on_nature_protection_and_biodiversity",
     "ETC/NPB (European Topic Centre on Nature Protection and Biodiversity)"),
    ("term.etc_wmf_european_topic_centre_on_waste_and_material_flows",
     "ETC/WMF (European Topic Centre on Waste and Material Flows)"),
    ("term.ecnc_european_centre_for_nature_conservation",
     "ECNC (European Centre for Nature Conservation)"),
    ("term.efi_european_forest_institute",
     "EFI (European Forest Institute)"),
    ("term.enea", "ENEA"),
    ("term.eionet", "EIONET"),
    ("term.emep_task_force",
     "EMEP Task Force"),
    ("term.european_commission_joint_research_center",
     "European Commission Joint Research Center"),
  ),
  'report_publishers': (
    ("term.eea_european_environment_agency",
     "EEA (European Environment Agency)"),
    ("term.opoce_office_for_official_publications_of_the_european_communities",
     "OPOCE (Office for Official Publications of the European Communities)"),
    ("term.unep_united_nations_environment_programme",
     "UNEP (United Nations Environment Programme)"),
    ("term.who_world_health_organization",
     "WHO (World Health Organization)"),
  ),
  'report_types': (
    ("term.briefing", "Briefing"),
    ("term.brochure", "Brochure"),
    ("term.corporate_document", "Corporate document"),
    ("term.technical_report", "Technical report"),
    ("term.topic_report", "Topic report"),
    ("term.eea_report", "EEA Report"),
    ("term.environmental_issue_report", "Environmental issue report"),
    ("term.environmental_assessment_report", "Environmental assessment report"),
    ("term.environmental_monograph", "Environmental monograph"),
    ("term.experts_corner", "Expert's corner"),
    ("vdexterm.2009-03-13.4432975636", "Administrative document"),
    ("term.state_of_the_environment_report", "State of the environment report"),
  ),
  'report_types_active': (
      ('Briefing', 'Briefing'),
      ('Brochure', 'Brochure'),
      ('Corporate document', 'Corporate document'),
      ('EEA Report', 'EEA Report'),
      ('Technical report', 'Technical report'),
  ),
}
