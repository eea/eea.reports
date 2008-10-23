﻿# -*- coding: utf8 -*-

# Get the HTML request and response objects
request = container.REQUEST
RESPONSE =  request.RESPONSE

# Set content type
RESPONSE.setHeader('content-type', 'text/xml')

root = container.restrictedTraverse('/')
report_metatype = ['Multilingual Report']
#reports_year = [2007, 2008]
reports_year = [2006]

#Reports count
#1995 -> 2
#1996 -> 31
#1997 -> 13
#1998 -> 10
#1999 -> 20
#2000 -> 13
#2001 -> 21
#2002 -> 9

#2003 -> 8
#2004 -> 26
#2005 -> 29
#2006 -> 31

#2007 -> 32
#2008 -> 18

res = []
res_add = res.append

def formatExport(data, skip=0):
    res = data
    if skip == 0:
        data_type = container.getType(data)
        if data_type in ['list', 'tuple']:
            res = '###'.join([str(x) for x in data])
        if data_type in ['int', 'date']:
            res = str(res)
        if len(res) > 5:
            if '%' in res or '&nbsp;' in res or '</p>' in res:
                res = '<![CDATA[%s]]>' % res
            else:
                #CDATA exceptions
                if 'TSD-Environment & Process Department' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'The Head of Department of Environmental Science & Engineering' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Dilip Chandwani' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Bosch & Partner GmbH' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'One of the main objectives of the European Topic Centre on Land Cover has been to develop the CORINE Land Cover Database' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'SW& 2AZ' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Christian Fischer, EPA of Denmark and City of Copenhagen in co-operation with Matthew Crowe' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Serbia&Montenegro' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Dep. Environment, Technology  & Social Studies' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'School of Science & Technology' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Serbia & Montenegro' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'gua&Ambiente"' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Aaqius & Aaqius' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Ingenia Consultants & Engineers' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Traffic-related air pollution is still one of the most pressing problems in urban areas' in res:
                    res = '<![CDATA[%s]]>' % res
                elif 'Coastal & Marine Resources Centre':
                    res = '<![CDATA[%s]]>' % res


    #Other exceptions
    excep1 = 'pollution monitoring (82/459/&quot;E'
    excep2 = 'Values (WHO, 1987) for the listed compounds ('
    excep3 = 'Figure 6.4: SO2 mean values in selected cities ('
    excep4 = 'Figure 6.6: SO2 maximum 24h values in selected cities'
    excep5 = 'Figure 6.7: SO2 trend in Norway 1977-1993 ('
    excep6 = 'Figure 6.3: SO2 median 24h values in selected cities ('
    excep7 = 'Figure 4: Frequency distribution of ozone concentrations in excess of the 180 '
#    excep8 = "mes prioritaires pour l'environnement m"
    if excep1 in res:
        findex = res.find(excep1)
        res = res[:findex+len(excep1)] + '&Oslash;' + res[findex+1+len(excep1):]
    if excep2 in res:
        findex = res.find(excep2)
        res = res[:findex+len(excep2)] + '&micro;' + res[findex+1+len(excep2):]
    for k in [excep3, excep4, excep5, excep6, excep7]:
        if k in res: res = unicode(res, 'ISO-8859-15').encode('utf8')
#    if excep8 in res and len(res) < 70:
#        res = "Problèmes prioritaires pour l’environnement méditerranéen"



    res  = res.replace('&oslash;', 'ø')
    res  = res.replace('&egrave;', 'è')
    res  = res.replace('&eacute;', 'é')
    res  = res.replace('&Egrave;', 'È')
    res  = res.replace('&ouml;', 'ö')
    res  = res.replace('&auml;', 'ä')
    res  = res.replace('&ccedil;', 'ç')
    res  = res.replace('&atilde;', 'ã')
    res  = res.replace('&oacute;', 'ó')

    return res

#Exceptions
tr_reporttitle = "Avrupa’nın çevresi — Dördüncü değerlendirme. İdari özet"
it_reporttitle = "L’ambiente in Europa — La quarta valutazione"
et_reporttitle = "6 Säästev tarbimine ja tootmine"
is_reporttitle = "Umhverfi Evrópu - Fjórða úttekt: 6 Sjálfbær neysla og framleiðsla"
hu_reporttitle = "Európa környezete Negyedik értékelés: 6 Fenntartható fogyasztás és termelés"
fi_reporttitle = "Euroopan ympäristö - Neljäs arviointi: 6 Kestävä kulutus ja tuotanto"
lt_reporttitle = "Europos aplinka - Ketvirtasis ávertinimas: 6 Tausojantis vartojimas ir gamyba"

lang_exceptions = ['http://reports.eea.europa.eu/briefing_2004_2/et', 'http://reports.eea.europa.eu/topic_report_2001_10/fr',
        'http://reports.eea.europa.eu/briefing_2005_3/et', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/et',
        'http://reports.eea.europa.eu/briefing_2005_1/et', 'http://reports.eea.europa.eu/briefing_2004_4/et',
        'http://reports.eea.europa.eu/briefing_2004_3/et', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/da',
        'http://reports.eea.europa.eu/briefing_2004_3/da', 'http://reports.eea.europa.eu/briefing_2004_4/da',
        'http://reports.eea.europa.eu/briefing_2005_1/da', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/da',
        'http://reports.eea.europa.eu/briefing_2005_3/da', 'http://reports.eea.europa.eu/briefing_2004_2/da',
        'http://reports.eea.europa.eu/briefing_2004_2/nl', 'http://reports.eea.europa.eu/briefing_2005_3/nl',
        'http://reports.eea.europa.eu/brochure_2006_0306_112210/fi', 'http://reports.eea.europa.eu/briefing_2004_3/fi',
        'http://reports.eea.europa.eu/briefing_2004_4/fi', 'http://reports.eea.europa.eu/briefing_2005_1/fi',
        'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fi', 'http://reports.eea.europa.eu/briefing_2004_2/fi',
        'http://reports.eea.europa.eu/briefing_2005_3/fi', 'http://reports.eea.europa.eu/briefing_2003_1/fr',
        'http://reports.eea.europa.eu/briefing_2004_3/fr', 'http://reports.eea.europa.eu/briefing_2004_4/fr',
        'http://reports.eea.europa.eu/briefing_2005_1/fr', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr',
        'http://reports.eea.europa.eu/briefing_2004_2/fr', 'http://reports.eea.europa.eu/briefing_2005_3/fr',
        'http://reports.eea.europa.eu/briefing_2004_3/de', 'http://reports.eea.europa.eu/briefing_2004_4/de',
        'http://reports.eea.europa.eu/briefing_2005_1/de', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/de',
        'http://reports.eea.europa.eu/briefing_2004_2/de', 'http://reports.eea.europa.eu/briefing_2005_3/de',
        'http://reports.eea.europa.eu/briefing_2004_2/el', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/hu',
        'http://reports.eea.europa.eu/briefing_2004_3/hu', 'http://reports.eea.europa.eu/briefing_2004_4/hu',
        'http://reports.eea.europa.eu/briefing_2005_1/hu', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu',
        'http://reports.eea.europa.eu/briefing_2005_3/hu', 'http://reports.eea.europa.eu/briefing_2004_2/hu',
        'http://reports.eea.europa.eu/brochure_2006_0306_112210/is', 'http://reports.eea.europa.eu/briefing_2004_3/is',
        'http://reports.eea.europa.eu/briefing_2005_3/is', 'http://reports.eea.europa.eu/briefing_2004_2/is',
        'http://reports.eea.europa.eu/briefing_2003_1/it', 'http://reports.eea.europa.eu/briefing_2004_4/it',
        'http://reports.eea.europa.eu/briefing_2005_1/it', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/it',
        'http://reports.eea.europa.eu/briefing_2004_3/it', 'http://reports.eea.europa.eu/briefing_2004_2/it',
        'http://reports.eea.europa.eu/state_of_environment_report_2005_1/lt', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/no',
        'http://reports.eea.europa.eu/briefing_2005_3/no', 'http://reports.eea.europa.eu/briefing_2004_4/no',
        'http://reports.eea.europa.eu/briefing_2005_1/no', 'http://reports.eea.europa.eu/briefing_2004_3/no',
        'http://reports.eea.europa.eu/briefing_2004_2/no', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/no',
        'http://reports.eea.europa.eu/state_of_environment_report_2005_1/pt', 'http://reports.eea.europa.eu/briefing_2004_2/pt',
        'http://reports.eea.europa.eu/briefing_2004_3/pt', 'http://reports.eea.europa.eu/briefing_2005_1/pt',
        'http://reports.eea.europa.eu/briefing_2004_4/pt', 'http://reports.eea.europa.eu/briefing_2005_3/pt',
        'http://reports.eea.europa.eu/brochure_2006_0306_112210/sk', 'http://reports.eea.europa.eu/briefing_2004_2/sk',
        'http://reports.eea.europa.eu/briefing_2005_3/es', 'http://reports.eea.europa.eu/briefing_2004_4/es',
        'http://reports.eea.europa.eu/briefing_2005_1/es', 'http://reports.eea.europa.eu/briefing_2004_3/es',
        'http://reports.eea.europa.eu/state_of_environment_report_2005_1/es', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/es',
        'http://reports.eea.europa.eu/briefing_2004_2/es', 'http://reports.eea.europa.eu/briefing_2003_1/sv',
        'http://reports.eea.europa.eu/briefing_2005_3/sv', 'http://reports.eea.europa.eu/briefing_2004_4/sv',
        'http://reports.eea.europa.eu/briefing_2005_1/sv', 'http://reports.eea.europa.eu/briefing_2004_3/sv',
        'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sv', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/sv',
        'http://reports.eea.europa.eu/briefing_2004_2/sv', 'http://reports.eea.europa.eu/briefing_2004_3/tr',
        'http://reports.eea.europa.eu/briefing_2005_3/tr', 'http://reports.eea.europa.eu/briefing_2004_2/tr',
        'http://reports.eea.europa.eu/briefing_2004_3/mt',
        
        
        'http://reports.eea.europa.eu/eea_report_2006_2/fr', 'http://reports.eea.europa.eu/eea_report_2006_4/fr',
        'http://reports.eea.europa.eu/briefing_2006_1/de', 'http://reports.eea.europa.eu/briefing_2006_1/fr',
        'http://reports.eea.europa.eu/briefing_2006_1/it', 'http://reports.eea.europa.eu/briefing_2006_1/no',
        'http://reports.eea.europa.eu/briefing_2006_1/sv', 'http://reports.eea.europa.eu/briefing_2006_1/tr',
        'http://reports.eea.europa.eu/briefing_2006_1/da', 'http://reports.eea.europa.eu/briefing_2006_1/es',
        'http://reports.eea.europa.eu/briefing_2006_1/nl', 'http://reports.eea.europa.eu/briefing_2006_1/is',
        'http://reports.eea.europa.eu/briefing_2006_1/pt', 'http://reports.eea.europa.eu/briefing_2006_1/et',
        'http://reports.eea.europa.eu/briefing_2006_1/hu', 'http://reports.eea.europa.eu/briefing_2006_1/ro',
        'http://reports.eea.europa.eu/briefing_2006_1/fi', 'http://reports.eea.europa.eu/briefing_2006_2/fr',
        'http://reports.eea.europa.eu/briefing_2006_3/mt', 'http://reports.eea.europa.eu/briefing_2006_4/da',
        'http://reports.eea.europa.eu/briefing_2006_4/de', 'http://reports.eea.europa.eu/briefing_2006_4/es',
        'http://reports.eea.europa.eu/briefing_2006_4/et', 'http://reports.eea.europa.eu/briefing_2006_4/fr',
        'http://reports.eea.europa.eu/briefing_2006_4/hu', 'http://reports.eea.europa.eu/briefing_2006_4/is',
        'http://reports.eea.europa.eu/briefing_2006_4/it', 'http://reports.eea.europa.eu/briefing_2006_4/no',
        'http://reports.eea.europa.eu/briefing_2006_4/pt', 'http://reports.eea.europa.eu/briefing_2006_4/sv',
        'http://reports.eea.europa.eu/briefing_2006_4/pl', 'http://reports.eea.europa.eu/briefing_2006_4/fi',
        'http://reports.eea.europa.eu/briefing_2006_4/lv']

file_exceptions = [
'http://reports.eea.europa.eu/state_of_environment_report_2005_1/da/DA-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/da/DA_DA-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/cs/CS_CS-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/de/AT_DE-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/de/AT_DE-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/es/ES-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/es/part-b_ES.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/et/ET-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/et/ET-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/et/ET_ET-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fi/FI-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fi/FI_FI-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr/FR-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr/BE_FR-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr/FR_FR-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr/LU_FR-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr/CH_FR-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu/HU-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu/part-b_HU.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu/HU-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu/HU_HU-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/is/IS-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/is/IS-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/is/part-b_IS.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/nl/BE_NL-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/no/NO-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/pl/PL_PL-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/pt/PT-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sk/SK-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sk/part-a_SK.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sv/SV-summary.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sv/part-b_SV.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/tr/TR-countryprofile.pdf'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/tr/TR_TR-ppt.ppt'
,'http://reports.eea.europa.eu/state_of_environment_report_2005_1/tr/part-b_TR.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/es/ES_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/fr/FR_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/tr/TR_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/sk/SK_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/is/IS_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/cs/CS_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/sv/SV_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_2/pt/PT_Briefing-Energy_web.pdf'
]

#Sort reports by year
reports = {}
for report in root.objectValues(report_metatype):
    val = reports.get(report.series_year, [])
    val.append(report)
    reports[report.series_year] = val


# Export content
res_add("""<?xml version="1.0" encoding="utf-8"?>""")
res_add('\n<reports>')

#for report in root.objectValues(report_metatype):
#    if report.series_year in reports_year:


for report in list(reports[int(rep_year)]):
#if 1 == 1:
#    report = reports[int(rep_year)][int(rep_index)]

    res_add('\n<report>')

    #Basic Property Sheet
    res_add('\n<id>%s</id>' % formatExport(report.id))                                                     #string
    res_add('\n<title>%s</title>' % formatExport(report.title))                                            #string
    res_add('\n<categories>%s</categories>' % formatExport(report.categories))                             #lines
    res_add('\n<weighting>%s</weighting>' % formatExport(report.weighting))                                #int
    res_add('\n<author>%s</author>' % formatExport(report.author))                                         #string
    res_add('\n<publisher>%s</publisher>' % formatExport(report.publisher))                                #string
    res_add('\n<source>%s</source>' % formatExport(report.source))                                         #string
    res_add('\n<publishdate>%s</publishdate>' % formatExport(report.publishdate))                          #date
    res_add('\n<updatedate>%s</updatedate>' % formatExport(report.updatedate))                             #date
    res_add('\n<createdate>%s</createdate>' % formatExport(report.createdate))                             #date
    res_add('\n<released>%s</released>' % formatExport(report.released))                                   #boolean
    res_add('\n<reporttype>%s</reporttype>' % formatExport(report.reporttype))                             #string
    res_add('\n<reportnum>%s</reportnum>' % formatExport(report.reportnum))                                #int
    res_add('\n<external_url>%s</external_url>' % formatExport(report.external_url))                       #string
    res_add('\n<order_override>%s</order_override>' % formatExport(report.order_override))                 #boolean
    res_add('\n<order_override_text>%s</order_override_text>' % formatExport(report.order_override_text))  #text
    res_add('\n<order_extra_text>%s</order_extra_text>' % formatExport(report.order_extra_text))           #text

    #Extra Property Sheet
    res_add('\n<expiry_date>%s</expiry_date>' % formatExport(report.expiry_date))                       #date
    res_add('\n<version_number>%s</version_number>' % formatExport(report.version_number))              #string
    res_add('\n<price_euro>%s</price_euro>' % formatExport(report.price_euro))                          #string
    res_add('\n<creators_orgs>%s</creators_orgs>' % formatExport(report.creators_orgs))                 #multiple selection
    res_add('\n<creators>%s</creators>' % formatExport(report.creators))                                #lines
    res_add('\n<publishers_orgs>%s</publishers_orgs>' % formatExport(report.publishers_orgs))           #multiple selection
    res_add('\n<publishers>%s</publishers>' % formatExport(report.publishers))                          #lines
    res_add('\n<coverage_time_from>%s</coverage_time_from>' % formatExport(report.coverage_time_from))  #date
    res_add('\n<coverage_time_to>%s</coverage_time_to>' % formatExport(report.coverage_time_to))        #date

    tmp_find = report.copyright.find('EEA, Copenhagen')
    if tmp_find > 0:
        res_add('\n<copyright>%s</copyright>' % formatExport(report.copyright[tmp_find:]))  #text
    else:
        res_add('\n<copyright>%s</copyright>' % formatExport(report.copyright[tmp_find:]))  #text

    res_add('\n<description>%s</description>' % container.unescape(formatExport(report.description)).encode('utf-8'))   #text

    res_add('\n<Subjects_terms>%s</Subjects_terms>' % formatExport(report.Subjects_terms))                        #lines
    res_add('\n<SpatialCoverage_terms>%s</SpatialCoverage_terms>' % formatExport(report.SpatialCoverage_terms))   #lines
    res_add('\n<series_year>%s</series_year>' % formatExport(report.series_year))                                 #selection
    res_add('\n<version_date>%s</version_date>' % formatExport(report.version_date))                              #date
    res_add('\n<sort_title>%s</sort_title>' % formatExport(report.sort_title))                                    #string
    res_add('\n<serial_title>%s</serial_title>' % formatExport(report.serial_title))                              #string
    res_add('\n<series_title>%s</series_title>' % formatExport(report.series_title))                              #string

    if report.id in ['binaryttopic_14_1999pdf', 'topic_report_2001_7', 'topic_report_2001_15',
                     'topic_report_2001_15_Part1', 'topic_report_2001_15_Part2', 'topic_report_2001_15_Part3',
                     'topic_report_2001_16']:
        res_add('\n<catalogue_text>%s</catalogue_text>' % unicode(formatExport(report.catalogue_text), 'ISO-8859-15').encode('utf8'))
    elif ' Jol' in report.catalogue_text:
        res_add('\n<catalogue_text>%s</catalogue_text>' % unicode(formatExport(report.catalogue_text), 'ISO-8859-15').encode('utf8'))
    elif 'ETC/NC leader' in report.catalogue_text:
        res_add('\n<catalogue_text>%s</catalogue_text>' % unicode(formatExport(report.catalogue_text), 'ISO-8859-15').encode('utf8'))
    elif 'Brage Rygg, Norwegian Institute for Water Research, Anita K' in report.catalogue_text:
        res_add('\n<catalogue_text>%s</catalogue_text>' % unicode(formatExport(report.catalogue_text), 'ISO-8859-15').encode('utf8'))
    elif 'J. Feher, A. Lazar, M. Joanny, G. ' in report.catalogue_text:
        res_add('\n<catalogue_text>%s</catalogue_text>' % unicode(formatExport(report.catalogue_text), 'ISO-8859-15').encode('utf8'))
    else:
        res_add('\n<catalogue_text>%s</catalogue_text>' % formatExport(report.catalogue_text))                        #text

    res_add('\n<main_entry>%s</main_entry>' % formatExport(report.main_entry))                                    #boolean
    res_add('\n<report_kind>%s</report_kind>' % formatExport(report.report_kind))                                 #selection

    #Product Property Sheet
    res_add('\n<product_version>%s</product_version>' % formatExport(report.product_version))     #string

    #Relations Property Sheet
    res_add('\n<IsRequiredBy>%s</IsRequiredBy>' % formatExport(report.IsRequiredBy))          #lines
    res_add('\n<Requires>%s</Requires>' % formatExport(report.Requires))                      #lines
    res_add('\n<IsPartOf>%s</IsPartOf>' % formatExport(report.IsPartOf))                      #lines
    res_add('\n<HasPart>%s</HasPart>' % formatExport(report.HasPart))                         #lines
    res_add('\n<IsReferencedBy>%s</IsReferencedBy>' % formatExport(report.IsReferencedBy))    #lines
    res_add('\n<References>%s</References>' % formatExport(report.References))                #lines
    res_add('\n<IsReplacedBy>%s</IsReplacedBy>' % formatExport(report.IsReplacedBy))          #lines
    res_add('\n<Replaces>%s</Replaces>' % formatExport(report.Replaces))                      #lines


    ###CoverImage objects
    #####################
    for img in report.objectValues('CoverImage'):
        res_add('\n<cover_image url="%s">' % img.absolute_url())
        #Zope file properties
        res_add('\n<id>%s</id>' % formatExport(img.getId()))                                 #string
        res_add('\n<title>%s</title>' % formatExport(img.title))                                 #string

        #Atlas Property Sheet
        res_add('\n<result1>%s</result1>' % formatExport(img.result1))                           #string
        res_add('\n<result2>%s</result2>' % formatExport(img.result2))                           #string
        res_add('\n<result3>%s</result3>' % formatExport(img.result3))                           #string
        res_add('\n<result4>%s</result4>' % formatExport(img.result4))                           #string
        res_add('\n<result5>%s</result5>' % formatExport(img.result5))                           #string
        res_add('\n<result6>%s</result6>' % formatExport(img.result6))                           #string
        res_add('\n<result7>%s</result7>' % formatExport(img.result7))                           #string
        res_add('\n<result8>%s</result8>' % formatExport(img.result8))                           #string
        res_add('\n<result9>%s</result9>' % formatExport(img.result9))                           #string
        res_add('\n<result10>%s</result10>' % formatExport(img.result10))                        #string
        res_add('\n<hardreference>%s</hardreference>' % formatExport(img.hardreference))         #string
        res_add('\n<softreference>%s</softreference>' % formatExport(img.softreference))         #string
        res_add('\n<totalresult>%s</totalresult>' % formatExport(img.totalresult))               #string
        res_add('\n<totalmembers>%s</totalmembers>' % formatExport(img.totalmembers))            #string
        res_add('\n<status>%s</status>' % formatExport(img.status))                              #string
        res_add('\n<synch_timestamp>%s</synch_timestamp>' % formatExport(img.synch_timestamp))   #string
        res_add('\n</cover_image>')


    ###Redirect objects
    ###################
    for rdr in report.objectValues('Redirect'):
        res_add('\n<redirect redirect_to="%s" />' % formatExport(rdr.redirect_to, 1))  #string


    ###Tag objects
    ##############
    for tag in report.objectValues('Report Tag'):
        res_add('\n<tag>')

        #Basic Property Sheet
        res_add('\n<title>%s</title>' % formatExport(tag.title))                                #string
        res_add('\n<categories>%s</categories>' % formatExport(tag.categories))                 #string
        res_add('\n<tag_description>%s</tag_description>' % formatExport(tag.tag_description))  #string
        res_add('\n<chapter>%s</chapter>' % formatExport(tag.chapter))                          #string

        #Extra Property Sheet
        res_add('\n<Subjects_terms>%s</Subjects_terms>' % formatExport(tag.Subjects_terms))                         #lines
        res_add('\n<SpatialCoverage_terms>%s</SpatialCoverage_terms>' % formatExport(tag.SpatialCoverage_terms))    #lines

        res_add('\n</tag>')

    ###Language Report objects
    ##########################
    for lang in report.objectValues('Language Report'):
        res_add('\n<language_report url="%s">' % lang.absolute_url())
        #Basic Property Sheet
        res_add('\n<id>%s</id>' % formatExport(lang.id))                           #string
        res_add('\n<eeaid>%s</eeaid>' % formatExport(getattr(lang, 'eeaid', '0'))) #integer
        res_add('\n<language>%s</language>' % formatExport(lang.language))         #string
        res_add('\n<title>%s</title>' % formatExport(lang.title))                  #string

        if lang.isbn == '978-92-9167-919-5' or lang.absolute_url() in lang_exceptions:
            res_add('\n<description>%s</description>' % unicode(formatExport(lang.description), 'ISO-8859-15').encode('utf-8'))  #text
        else:
            res_add('\n<description>%s</description>' % container.unescape(formatExport(lang.description)).encode('utf-8')) #text

        res_add('\n<trailer>%s</trailer>' % formatExport(lang.trailer))                                      #text
        res_add('\n<sections>%s</sections>' % formatExport(lang.sections))                                   #lines
        res_add('\n<order_override_lang>%s</order_override_lang>' % formatExport(lang.order_override_lang))  #boolean

        if report.id == 'state_of_environment_report_2007_1' and lang.id == 'tr':
            res_add('\n<reporttitle>%s</reporttitle>' % tr_reporttitle)                      #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'it':
            res_add('\n<reporttitle>%s</reporttitle>' % it_reporttitle)                      #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'et':
            res_add('\n<reporttitle>%s</reporttitle>' % et_reporttitle)                      #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'is':
            res_add('\n<reporttitle>%s</reporttitle>' % is_reporttitle)                      #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'hu':
            res_add('\n<reporttitle>%s</reporttitle>' % hu_reporttitle)                      #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'fi':
            res_add('\n<reporttitle>%s</reporttitle>' % fi_reporttitle)                      #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'lt':
            res_add('\n<reporttitle>%s</reporttitle>' % lt_reporttitle)                      #string
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/topic_report_2001_10/fr',
                'http://reports.eea.europa.eu/briefing_2003_1/cs', 'http://reports.eea.europa.eu/briefing_2003_1/fr',
                'http://reports.eea.europa.eu/briefing_2003_1/sv', 'http://reports.eea.europa.eu/briefing_2004_2/es',
                'http://reports.eea.europa.eu/briefing_2004_2/fr', 'http://reports.eea.europa.eu/briefing_2004_2/tr',
                'http://reports.eea.europa.eu/briefing_2004_2/sk', 'http://reports.eea.europa.eu/briefing_2004_2/is',
                'http://reports.eea.europa.eu/briefing_2004_2/cs', 'http://reports.eea.europa.eu/briefing_2004_2/sv',
                'http://reports.eea.europa.eu/briefing_2004_2/pt', 'http://reports.eea.europa.eu/briefing_2004_2/hu',
                'http://reports.eea.europa.eu/briefing_2004_3/da', 'http://reports.eea.europa.eu/briefing_2004_3/fi',
                'http://reports.eea.europa.eu/briefing_2004_3/sv', 'http://reports.eea.europa.eu/briefing_2004_3/no',
                'http://reports.eea.europa.eu/briefing_2004_3/hu', 'http://reports.eea.europa.eu/briefing_2004_3/tr',
                'http://reports.eea.europa.eu/briefing_2004_3/sk', 'http://reports.eea.europa.eu/briefing_2004_3/ro',
                'http://reports.eea.europa.eu/TERM2004/tr', 'http://reports.eea.europa.eu/briefing_2004_4/de',
                'http://reports.eea.europa.eu/briefing_2004_4/et', 'http://reports.eea.europa.eu/briefing_2004_4/fr',
                'http://reports.eea.europa.eu/briefing_2004_4/hu', 'http://reports.eea.europa.eu/briefing_2004_4/no',
                'http://reports.eea.europa.eu/briefing_2004_4/pt', 'http://reports.eea.europa.eu/briefing_2004_4/da',
                'http://reports.eea.europa.eu/briefing_2004_4/es', 'http://reports.eea.europa.eu/briefing_2004_4/sv',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/da', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/de',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/fr', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/hu',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/no', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/pt',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/sk', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/fi',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/sv', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/tr',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/is', 'http://reports.eea.europa.eu/briefing_2004_3/is',
                'http://reports.eea.europa.eu/briefing_2005_1/es', 'http://reports.eea.europa.eu/briefing_2005_1/pt',
                'http://reports.eea.europa.eu/briefing_2005_1/sk', 'http://reports.eea.europa.eu/briefing_2005_1/sv',
                'http://reports.eea.europa.eu/briefing_2005_1/et', 'http://reports.eea.europa.eu/briefing_2005_1/hu',
                'http://reports.eea.europa.eu/briefing_2005_1/da', 'http://reports.eea.europa.eu/briefing_2005_1/ro',
                'http://reports.eea.europa.eu/briefing_2005_1/fr', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/da',
                'http://reports.eea.europa.eu/state_of_environment_report_2005_1/et', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fi',
                'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu',
                'http://reports.eea.europa.eu/state_of_environment_report_2005_1/no', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/pt',
                'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sv', 'http://reports.eea.europa.eu/briefing_2005_3/da',
                'http://reports.eea.europa.eu/briefing_2005_3/es', 'http://reports.eea.europa.eu/briefing_2005_3/hu',
                'http://reports.eea.europa.eu/briefing_2005_3/de', 'http://reports.eea.europa.eu/briefing_2005_3/fr',
                'http://reports.eea.europa.eu/briefing_2005_3/sv', 'http://reports.eea.europa.eu/briefing_2005_3/pt',
                'http://reports.eea.europa.eu/briefing_2005_3/no', 'http://reports.eea.europa.eu/briefing_2005_3/is',
                'http://reports.eea.europa.eu/briefing_2005_3/it', 'http://reports.eea.europa.eu/briefing_2005_3/sk',
                'http://reports.eea.europa.eu/eea_report_2006_2/fr',
                'http://reports.eea.europa.eu/briefing_2006_1/fr', 'http://reports.eea.europa.eu/briefing_2006_1/no',
                'http://reports.eea.europa.eu/briefing_2006_1/sv', 'http://reports.eea.europa.eu/briefing_2006_1/tr',
                'http://reports.eea.europa.eu/briefing_2006_1/da', 'http://reports.eea.europa.eu/briefing_2006_1/da/briefing_01_2006-DA.pdf',
                'http://reports.eea.europa.eu/briefing_2006_1/es', 'http://reports.eea.europa.eu/briefing_2006_1/is',
                'http://reports.eea.europa.eu/briefing_2006_1/pt', 'http://reports.eea.europa.eu/briefing_2006_1/et'
                'http://reports.eea.europa.eu/briefing_2006_1/hu', 'http://reports.eea.europa.eu/briefing_2006_1/ro',
                'http://reports.eea.europa.eu/briefing_2006_1/fi', 'http://reports.eea.europa.eu/briefing_2006_1/lv',
                'http://reports.eea.europa.eu/briefing_2006_2/fr', 'http://reports.eea.europa.eu/briefing_2006_4/es',
                'http://reports.eea.europa.eu/briefing_2006_4/hu', 'http://reports.eea.europa.eu/briefing_2006_4/is',
                'http://reports.eea.europa.eu/briefing_2006_4/sv', 'http://reports.eea.europa.eu/briefing_2006_1/et',
                'http://reports.eea.europa.eu/briefing_2006_1/hu', 'http://reports.eea.europa.eu/briefing_2006_4/pt']:
            res_add('\n<reporttitle>%s</reporttitle>' % container.unescape(unicode(formatExport(lang.reporttitle), 'ISO-8859-15').encode('utf8')))
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/eea_report_2006_4/fr']:
            res_add('\n<reporttitle>%s</reporttitle>' % formatExport("Problèmes prioritaires pour l'environnement méditerranéen"))                      #string
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/briefing_2008_1/fr']:
            pass
        else:
            res_add('\n<reporttitle>%s</reporttitle>' % formatExport(lang.reporttitle))                      #string

        #Extra Property Sheet
        res_add('\n<pages>%s</pages>' % formatExport(lang.pages))                    #int
        res_add('\n<isbn>%s</isbn>' % formatExport(lang.isbn))                       #string
        res_add('\n<catalogue>%s</catalogue>' % formatExport(lang.catalogue))        #string

        if report.id == 'state_of_environment_report_2007_1' and lang.id == 'tr':
            res_add('\n<sort_title>%s</sort_title>' % tr_reporttitle)                #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'it':
            res_add('\n<sort_title>%s</sort_title>' % it_reporttitle)                #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'et':
            res_add('\n<sort_title>%s</sort_title>' % et_reporttitle)                #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'is':
            res_add('\n<sort_title>%s</sort_title>' % is_reporttitle)                #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'hu':
            res_add('\n<sort_title>%s</sort_title>' % hu_reporttitle)                #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'fi':
            res_add('\n<sort_title>%s</sort_title>' % fi_reporttitle)                #string
        elif report.id == 'state_of_environment_report_2007_1' and lang.id == 'lt':
            res_add('\n<sort_title>%s</sort_title>' % lt_reporttitle)                #string
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/topic_report_2001_10/fr',
'http://reports.eea.europa.eu/briefing_2003_1/cs', 'http://reports.eea.europa.eu/briefing_2003_1/fr', 'http://reports.eea.europa.eu/briefing_2003_1/sv',
'http://reports.eea.europa.eu/briefing_2004_1/es', 'http://reports.eea.europa.eu/briefing_2004_1/et', 'http://reports.eea.europa.eu/briefing_2004_1/fi',
'http://reports.eea.europa.eu/briefing_2004_1/fr', 'http://reports.eea.europa.eu/briefing_2004_1/is', 'http://reports.eea.europa.eu/briefing_2004_1/pl',
'http://reports.eea.europa.eu/briefing_2004_1/sl', 'http://reports.eea.europa.eu/briefing_2004_1/sv', 'http://reports.eea.europa.eu/briefing_2004_1/tr',
'http://reports.eea.europa.eu/briefing_2004_2/tr', 'http://reports.eea.europa.eu/briefing_2004_2/lv','http://reports.eea.europa.eu/briefing_2004_2/sk',
'http://reports.eea.europa.eu/briefing_2004_2/cs', 'http://reports.eea.europa.eu/briefing_2004_2/pt', 'http://reports.eea.europa.eu/briefing_2004_2/ro',
'http://reports.eea.europa.eu/briefing_2004_2/lt', 'http://reports.eea.europa.eu/briefing_2004_2/hu',
'http://reports.eea.europa.eu/briefing_2004_3/da', 'http://reports.eea.europa.eu/briefing_2004_3/fi', 'http://reports.eea.europa.eu/briefing_2004_3/sv',
'http://reports.eea.europa.eu/briefing_2004_3/no', 'http://reports.eea.europa.eu/briefing_2004_3/sk', 'http://reports.eea.europa.eu/briefing_2004_3/lv',
'http://reports.eea.europa.eu/briefing_2004_3/is', 'http://reports.eea.europa.eu/briefing_2004_3/ro', 'http://reports.eea.europa.eu/TERM2004/tr',
'http://reports.eea.europa.eu/briefing_2004_4/de', 'http://reports.eea.europa.eu/briefing_2004_4/cs',
'http://reports.eea.europa.eu/briefing_2004_4/et', 'http://reports.eea.europa.eu/briefing_2004_4/fr', 'http://reports.eea.europa.eu/briefing_2004_4/hu',
'http://reports.eea.europa.eu/briefing_2004_4/no', 'http://reports.eea.europa.eu/briefing_2004_4/pt', 'http://reports.eea.europa.eu/briefing_2004_4/sk',
'http://reports.eea.europa.eu/briefing_2004_4/tr', 'http://reports.eea.europa.eu/briefing_2004_4/da', 'http://reports.eea.europa.eu/briefing_2004_4/es',
'http://reports.eea.europa.eu/briefing_2004_4/lt', 'http://reports.eea.europa.eu/briefing_2004_4/ro', 'http://reports.eea.europa.eu/briefing_2004_4/lv',
'http://reports.eea.europa.eu/briefing_2004_4/is', 'http://reports.eea.europa.eu/briefing_2004_4/sv', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/da',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/de', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/fr', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/lv',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/hu', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/no', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/pt',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/sk', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/fi', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/sv',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/tr', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/is', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/cs',
'http://reports.eea.europa.eu/briefing_2005_1/es', 'http://reports.eea.europa.eu/briefing_2005_1/lt', 'http://reports.eea.europa.eu/briefing_2005_1/lv',
'http://reports.eea.europa.eu/briefing_2005_1/mt', 'http://reports.eea.europa.eu/briefing_2005_1/pt', 'http://reports.eea.europa.eu/briefing_2005_1/sk',
'http://reports.eea.europa.eu/briefing_2005_1/sv', 'http://reports.eea.europa.eu/briefing_2005_1/tr', 'http://reports.eea.europa.eu/briefing_2005_1/et',
'http://reports.eea.europa.eu/briefing_2005_1/hu', 'http://reports.eea.europa.eu/briefing_2005_1/da', 'http://reports.eea.europa.eu/briefing_2005_1/ro',
'http://reports.eea.europa.eu/briefing_2005_1/fr', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/da', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/cs',
'http://reports.eea.europa.eu/state_of_environment_report_2005_1/et', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fi', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/fr',
'http://reports.eea.europa.eu/state_of_environment_report_2005_1/hu', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/lt', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/lv',
'http://reports.eea.europa.eu/state_of_environment_report_2005_1/no', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/pl', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/pt',
'http://reports.eea.europa.eu/state_of_environment_report_2005_1/ro', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sk', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sl',
'http://reports.eea.europa.eu/state_of_environment_report_2005_1/sv', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/tr', 'http://reports.eea.europa.eu/briefing_2005_3/da',
'http://reports.eea.europa.eu/briefing_2005_3/es', 'http://reports.eea.europa.eu/briefing_2005_3/hu', 'http://reports.eea.europa.eu/briefing_2005_3/de',
'http://reports.eea.europa.eu/briefing_2005_3/fr', 'http://reports.eea.europa.eu/briefing_2005_3/sv', 'http://reports.eea.europa.eu/briefing_2005_3/pt',
'http://reports.eea.europa.eu/briefing_2005_3/no', 'http://reports.eea.europa.eu/briefing_2005_3/is', 'http://reports.eea.europa.eu/briefing_2005_3/it',
'http://reports.eea.europa.eu/briefing_2005_3/tr', 'http://reports.eea.europa.eu/briefing_2005_3/lt', 'http://reports.eea.europa.eu/briefing_2005_3/lv',
'http://reports.eea.europa.eu/briefing_2005_3/sk', 'http://reports.eea.europa.eu/briefing_2005_3/ro', 'http://reports.eea.europa.eu/briefing_2005_3/pl',
'http://reports.eea.europa.eu/eea_report_2006_2/fr', 'http://reports.eea.europa.eu/briefing_2006_1/fr',
'http://reports.eea.europa.eu/briefing_2006_1/no', 'http://reports.eea.europa.eu/briefing_2006_1/sk', 'http://reports.eea.europa.eu/briefing_2006_1/sv',
'http://reports.eea.europa.eu/briefing_2006_1/tr', 'http://reports.eea.europa.eu/briefing_2006_1/da', 'http://reports.eea.europa.eu/briefing_2006_1/da/briefing_01_2006-DA.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/es', 'http://reports.eea.europa.eu/briefing_2006_1/is', 'http://reports.eea.europa.eu/briefing_2006_1/pt',
'http://reports.eea.europa.eu/briefing_2006_1/et', 'http://reports.eea.europa.eu/briefing_2006_1/hu', 'http://reports.eea.europa.eu/briefing_2006_1/ro',
'http://reports.eea.europa.eu/briefing_2006_1/fi', 'http://reports.eea.europa.eu/briefing_2006_1/lv', 'http://reports.eea.europa.eu/briefing_2006_1/lt',
'http://reports.eea.europa.eu/briefing_2006_2/fr', 'http://reports.eea.europa.eu/briefing_2006_4/cs', 'http://reports.eea.europa.eu/briefing_2006_4/es',
'http://reports.eea.europa.eu/briefing_2006_4/hu', 'http://reports.eea.europa.eu/briefing_2006_4/is', 'http://reports.eea.europa.eu/briefing_2006_4/lt',
'http://reports.eea.europa.eu/briefing_2006_4/pt', 'http://reports.eea.europa.eu/briefing_2006_4/ro', 'http://reports.eea.europa.eu/briefing_2006_4/sk',
'http://reports.eea.europa.eu/briefing_2006_4/sl', 'http://reports.eea.europa.eu/briefing_2006_4/sv', 'http://reports.eea.europa.eu/briefing_2006_4/tr',
'http://reports.eea.europa.eu/briefing_2006_4/lv']:
            res_add('\n<sort_title>%s</sort_title>' % unicode(formatExport(lang.sort_title), 'ISO-8859-15').encode('utf8')) #string
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/eea_report_2006_4/fr']:
            res_add('\n<sort_title>%s</sort_title>' % formatExport("Problèmes prioritaires pour l'environnement méditerranéen")) #string
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/brochure_2006_0306_112210/bg',
                'http://reports.eea.europa.eu/briefing_2005_1/bg', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/bg',
                'http://reports.eea.europa.eu/briefing_2004_3/bg', 'http://reports.eea.europa.eu/briefing_2004_4/bg']:
            res_add('\n<sort_title>%s</sort_title>' % unicode(formatExport(lang.sort_title), 'ISO-8859-5').encode('utf8')) #string
        elif lang.absolute_url() in ['http://reports.eea.europa.eu/briefing_2004_1/el',
                'http://reports.eea.europa.eu/briefing_2004_3/el', 'http://reports.eea.europa.eu/briefing_2004_4/el',
                'http://reports.eea.europa.eu/brochure_2006_0306_112210/el', 'http://reports.eea.europa.eu/briefing_2005_1/el',
                'http://reports.eea.europa.eu/state_of_environment_report_2005_1/el', 'http://reports.eea.europa.eu/briefing_2006_4/el']:
            res_add('\n<sort_title>%s</sort_title>' % unicode(formatExport(lang.sort_title), 'iso-8859-7').encode('utf8')) #string
        else:
            res_add('\n<sort_title>%s</sort_title>' % formatExport(lang.sort_title)) #string

        #Manager Property Sheet
        res_add('\n<langreleased>%s</langreleased>' % formatExport(lang.langreleased))   #boolean

        ###Report Chapter objects
        #########################
        for chp in lang.objectValues('Report Chapter'):
            res_add('\n<report_chapter>')
            #Basic Property Sheet
            res_add('\n<id>%s</id>' % formatExport(chp.id))                             #string
            res_add('\n<title>%s</title>' % formatExport(chp.title))                    #text

            #for 1996 <content> need ISO-8859-15->utf8
            if 'southern part of the country are generally rather small. The greatest river is' in chp.content:
                #TODO: fix 1996 on IE (invalid character)
                pass
            elif '8.6 per cent of the total area of Sweden consists' in chp.content:
                #TODO: fix 1996 on IE (invalid character)
                pass
            else:
                # ISO-8859-15 for 1996 reports
                res_add('\n<content>%s</content>' % unicode(formatExport(chp.content), 'ISO-8859-15').encode('utf8'))  #string

            res_add('\n<description>%s</description>' % formatExport(chp.description))  #string
            res_add('\n<pagenumber>%s</pagenumber>' % formatExport(chp.pagenumber))     #int
            res_add('\n<categories>%s</categories>' % formatExport(chp.categories))     #lines
            res_add('\n<section>%s</section>' % formatExport(chp.section))              #string
            res_add('\n<tags>%s</tags>' % formatExport(chp.tags))                       #lines
            res_add('\n<TOC_page>%s</TOC_page>' % formatExport(chp.TOC_page))           #boolean

            #Extra Property Sheet
            res_add('\n<relations>%s</relations>' % formatExport(chp.relations))            #string
            res_add('\n<only_links>%s</only_links>' % formatExport(chp.only_links))         #string
            res_add('\n<external_url>%s</external_url>' % formatExport(chp.external_url))   #string
            res_add('\n</report_chapter>')

        ###Report File objects
        #########################
        for rep_file in lang.objectValues('Report File'):
            res_add('\n<report_file url="%s">' % rep_file.absolute_url())
            #Basic Property Sheet
            res_add('\n<id>%s</id>' % formatExport(rep_file.getId()))       #string
            res_add('\n<tags>%s</tags>' % formatExport(rep_file.tags))      #lines
            res_add('\n<pagenumber>%s</pagenumber>' % formatExport(rep_file.pagenumber))                        #int

            if rep_file.absolute_url() in ['http://reports.eea.europa.eu/topic_report_2001_10/fr/topic-10-web.pdf',
'http://reports.eea.europa.eu/briefing_2003_1/da/EEA_Briefing_WIR_DA.pdf', 'http://reports.eea.europa.eu/briefing_2003_1/fr/EEA_Briefing_WIR_FR.pdf',
'http://reports.eea.europa.eu/briefing_2003_1/hu/EEA_Briefing_WIR_HU.pdf', 'http://reports.eea.europa.eu/briefing_2003_1/is/EEA_Briefing_WIR_IS.pdf',
'http://reports.eea.europa.eu/briefing_2003_1/lt/EEA_Briefing_WIR_LT.pdf', 'http://reports.eea.europa.eu/briefing_2003_1/pl/EEA_Briefing_WIR_PL.pdf',
'http://reports.eea.europa.eu/briefing_2003_1/pt/EEA_Briefing_WIR_PT.pdf', 'http://reports.eea.europa.eu/briefing_2003_1/sk/EEA_Briefing_WIR_SK.pdf',
'http://reports.eea.europa.eu/briefing_2003_1/sv/EEA_Briefing_WIR_SV.pdf', 'http://reports.eea.europa.eu/briefing_2004_1/fi/Briefing-bio_FI_FINAL.pdf',
'http://reports.eea.europa.eu/briefing_2004_1/no/Briefing-bio_NO_FINAL.pdf', 'http://reports.eea.europa.eu/briefing_2004_2/hu/HU_Briefing-Energy_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/da/DA_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/fi/FI_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/sv/SV_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/no/NO_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/hu/HU_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/tr/TR_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/sk/SK_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/is/IS_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/ro/RO_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/TERM2004/tr/TERM2004_TR_final.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/de/DE_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/et/ET_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/fr/FR_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/hu/HU_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/no/NO_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/pt/PT_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/da/DA_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/es/ES_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/sv/SV_Briefing_4.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/da/general_brochure_web-DA.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/de/general_brochure_web-DE.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/lv/general_brochure_web-LV.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/lt/general_brochure_web-LT.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/hu/general_brochure_web-HU.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/no/general_brochure_web-NO.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/pt/general_brochure_web-PT.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/sk/general_brochure_web-SK.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/fi/general_brochure_web-FI.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/sv/general_brochure_web-SV.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/tr/general_brochure_web-TR.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/is/general_brochure_web-IS.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/es/briefing_2005_1-es.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/it/briefing_2005_1-it.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/pt/briefing_2005_1-pt.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/sk/briefing_2005_1-sk.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/sv/briefing_2005_1-sv.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/et/briefing_2005_1-et.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/hu/briefing_2005_1-hu.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/da/briefing_2005_1-da.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/ro/briefing_2005_1-ro.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/fr/briefing_2005_1-fr.pdf', 'http://reports.eea.europa.eu/state_of_environment_report_2005_1/da/part-b_DA.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/da/Briefing_3_2005_DA.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/es/Briefing_3_2005_ES.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/hu/Briefing_3_2005_HU.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/cs/Briefing_3_2005_CS.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/de/Briefing_3_2005_DE.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/fr/Briefing_3_2005_FR.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/sv/Briefing_3_2005_SV.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/pt/Briefing_3_2005_PT.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/no/Briefing_3_2005_NO.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/mt/Briefing_3_2005_MT.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/is/Briefing_3_2005_IS.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/it/Briefing_3_2005_IT.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/tr/Briefing_3_2005_TR.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/lv/Briefing_3_2005_LV.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/sk/Briefing_3_2005_SK.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/ro/Briefing_3_2005_RO.pdf',
'http://reports.eea.europa.eu/eea_report_2006_2/fr/irena2006-FR.pdf', 'http://reports.eea.europa.eu/eea_report_2006_4/fr/eea_report_4_2006_FR.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/fr/briefing_01_2006-FR.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/no/briefing_01_2006-NO.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/sv/briefing_01_2006-SV.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/tr/briefing_01_2006-TR.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/da/briefing_01_2006-DA.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/es/briefing_01_2006-ES.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/is/briefing_01_2006-IS.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/pt/briefing_01_2006-PT.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/et', 'http://reports.eea.europa.eu/briefing_2006_1/et/briefing_01_2006-ET.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/hu', 'http://reports.eea.europa.eu/briefing_2006_1/hu/briefing_01_2006-HU.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/ro/briefing_01_2006-RO.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/fi/briefing_01_2006-FI.pdf',
'http://reports.eea.europa.eu/briefing_2006_2/fr/eea_briefing_02_2006_fr.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/es/eea_briefing_4_2006-ES.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/hu/eea_briefing_4_2006-HU.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/is/eea_briefing_4_2006-IS.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/pt', 'http://reports.eea.europa.eu/briefing_2006_4/pt/eea_briefing_4_2006-PT.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/sv/eea_briefing_4_2006-SV.pdf']:
                res_add('\n<title>%s</title>' % unicode(formatExport(rep_file.title), 'ISO-8859-15').encode('utf8'))   #string
            else:
                res_add('\n<title>%s</title>' % formatExport(rep_file.title))   #string

            if rep_file.getId() == 'eea_briefing_1_2007-de.pdf':
                res_add('\n<file_description>%s</file_description>' % unicode(formatExport(rep_file.file_description), 'ISO-8859-15').encode('utf8'))  #text
            elif rep_file.absolute_url() in ['http://reports.eea.europa.eu/92-9167-029-4/en/TopicReportNo22-1996.pdf',
'http://reports.eea.europa.eu/92-9167-051-0/en/TopicReportNo16-1996.pdf', 'http://reports.eea.europa.eu/briefing_2003_1/fr/EEA_Briefing_WIR_FR.pdf',
'http://reports.eea.europa.eu/briefing_2003_1/sv/EEA_Briefing_WIR_SV.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/da/DA_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/de/DE_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/es/ES_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/et/ET_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/fi/FI_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/fr/FR_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/sv/SV_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/it/IT_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/mt/MT_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/no/NO_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/pt/PT_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/hu/HU_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_3/tr/TR_Briefing_No_03_web.pdf',
'http://reports.eea.europa.eu/briefing_2004_3/is/IS_Briefing_No_03_web.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/de/DE_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/et/ET_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/fi/FI_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/fr/FR_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/hu/HU_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/no/NO_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/pt/PT_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/da/DA_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/es/ES_Briefing_4.pdf',
'http://reports.eea.europa.eu/briefing_2004_4/sv/SV_Briefing_4.pdf', 'http://reports.eea.europa.eu/briefing_2004_4/it/IT_Briefing_4.pdf',
'http://reports.eea.europa.eu/technical_report_2004_6/en/tech_6_2004_web.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/da/general_brochure_web-DA.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/es/general_brochure_web-ES.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/hu/general_brochure_web-HU.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/no/general_brochure_web-NO.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/sk/general_brochure_web-SK.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/fi/general_brochure_web-FI.pdf', 'http://reports.eea.europa.eu/brochure_2006_0306_112210/sv/general_brochure_web-SV.pdf',
'http://reports.eea.europa.eu/brochure_2006_0306_112210/is/general_brochure_web-IS.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/de/briefing_2005_1-de.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/es/briefing_2005_1-es.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/it/briefing_2005_1-it.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/no/briefing_2005_1-no.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/pt/briefing_2005_1-pt.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/sv/briefing_2005_1-sv.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/fi/briefing_2005_1-fi.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/et/briefing_2005_1-et.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/hu/briefing_2005_1-hu.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/da/briefing_2005_1-da.pdf', 'http://reports.eea.europa.eu/briefing_2005_1/fr/briefing_2005_1-fr.pdf'
'http://reports.eea.europa.eu/report_2004_0622_154840/en/Annual-report-FINAL_web.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/da/Briefing_3_2005_DA.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/es/Briefing_3_2005_ES.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/fi/Briefing_3_2005_FI.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/hu/Briefing_3_2005_HU.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/de/Briefing_3_2005_DE.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/fr/Briefing_3_2005_FR.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/sv/Briefing_3_2005_SV.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/nl/Briefing_3_2005_NL.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/pt/Briefing_3_2005_PT.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/no/Briefing_3_2005_NO.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/et/Briefing_3_2005_ET.pdf',
'http://reports.eea.europa.eu/briefing_2005_3/is/Briefing_3_2005_IS.pdf', 'http://reports.eea.europa.eu/briefing_2005_3/tr/Briefing_3_2005_TR.pdf',
'http://reports.eea.europa.eu/briefing_2005_1/fr/briefing_2005_1-fr.pdf', 'http://reports.eea.europa.eu/report_2004_0622_154840/en/Annual-report-FINAL_web.pdf',
'http://reports.eea.europa.eu/eea_report_2006_2/fr/irena2006-FR.pdf', 'http://reports.eea.europa.eu/eea_report_2006_4/fr/eea_report_4_2006_FR.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/de/briefing_01_2006-DE.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/fr/briefing_01_2006-FR.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/it/briefing_01_2006-IT.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/no/briefing_01_2006-NO.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/sv/briefing_01_2006-SV.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/tr/briefing_01_2006-TR.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/da/briefing_01_2006-DA.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/es/briefing_01_2006-ES.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/nl/briefing_01_2006-NL.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/is/briefing_01_2006-IS.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/pt/briefing_01_2006-PT.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/et/briefing_01_2006-ET.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/hu/briefing_01_2006-HU.pdf', 'http://reports.eea.europa.eu/briefing_2006_1/ro/briefing_01_2006-RO.pdf',
'http://reports.eea.europa.eu/briefing_2006_1/fi/briefing_01_2006-FI.pdf', 'http://reports.eea.europa.eu/briefing_2006_2/fr/eea_briefing_02_2006_fr.pdf',
'http://reports.eea.europa.eu/briefing_2006_3/mt/eea_briefing_3_2006-mt.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/da/eea_briefing_4_2006-DA.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/de/eea_briefing_4_2006-DE.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/es/eea_briefing_4_2006-ES.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/et/eea_briefing_4_2006-ET.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/fr/eea_briefing_4_2006-FR.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/hu/eea_briefing_4_2006-HU.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/is/eea_briefing_4_2006-IS.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/it/eea_briefing_4_2006-IT.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/no/eea_briefing_4_2006-NO.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/pt/eea_briefing_4_2006-PT.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/sv/eea_briefing_4_2006-SV.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/pl/eea_briefing_4_2006-PL.pdf', 'http://reports.eea.europa.eu/briefing_2006_4/fi/eea_briefing_4_2006-FI.pdf',
'http://reports.eea.europa.eu/briefing_2006_4/lv/eea_briefing_4_2006-LV.pdf']:
                res_add('\n<file_description>%s</file_description>' % unicode(formatExport(rep_file.file_description), 'ISO-8859-15').encode('utf8'))
            else:
                res_add('\n<file_description>%s</file_description>' % formatExport(rep_file.file_description))  #text

            res_add('\n</report_file>')

        ###ReportOrder objects
        #########################
        for ord in lang.objectValues('ReportOrder'):
            res_add('\n<report_order url="%s">' % ord.absolute_url())
            #Basic Property Sheet
            res_add('\n<title>%s</title>' % formatExport(ord.title))                                                    #string
            res_add('\n<order_id>%s</order_id>' % formatExport(ord.order_id))                                           #string
            res_add('\n<customer_mail>%s</customer_mail>' % formatExport(ord.customer_mail))                            #string
            res_add('\n<order_date>%s</order_date>' % formatExport(ord.order_date))                                     #date
            res_add('\n<order_confirm_date>%s</order_confirm_date>' % formatExport(ord.order_confirm_date))             #date
            res_add('\n<customer_nameandadress>%s</customer_nameandadress>' % unicode(formatExport(ord.customer_nameandadress), 'ISO-8859-15').encode('utf8')) #text
            res_add('\n<order_shipping_date>%s</order_shipping_date>' % formatExport(ord.order_shipping_date))          #date
            res_add('\n<name>%s</name>' % unicode(formatExport(ord.name), 'ISO-8859-15').encode('utf8'))                                                       #string
            res_add('\n<organisation>%s</organisation>' % unicode(formatExport(ord.organisation), 'ISO-8859-15').encode('utf8'))                               #string
            res_add('\n<address>%s</address>' % unicode(formatExport(ord.address), 'ISO-8859-15').encode('utf8'))                                              #string

            if ord.absolute_url() in ['http://reports.eea.europa.eu/topic_report_2002_4/en/401514697',
                                      'http://reports.eea.europa.eu/topic_report_2002_4/en/578070962',
                                      'http://reports.eea.europa.eu/topic_report_2003_1/en/604315246']:
                res_add('\n<postal_code>%s</postal_code>' % unicode(formatExport(ord.postal_code), 'ISO-8859-15').encode('utf8'))                                  #string
            else:
                res_add('\n<postal_code>%s</postal_code>' % formatExport(ord.postal_code))                                  #string
            res_add('\n<city>%s</city>' % unicode(formatExport(ord.city), 'ISO-8859-15').encode('utf8'))                                                       #string
            if ord.absolute_url() in ['http://reports.eea.europa.eu/Topic_report_No_111999/en/15710794',
                                      'http://reports.eea.europa.eu/topic_report_2001_7/en/769877952']:
                res_add('\n<country>%s</country>' % unicode(formatExport(ord.country), 'ISO-8859-15').encode('utf8'))
            elif 'Espa' in ord.country:
                res_add('\n<country>%s</country>' % unicode(formatExport(ord.country), 'ISO-8859-15').encode('utf8'))
            elif 'ESPA' in ord.country:
                res_add('\n<country>%s</country>' % unicode(formatExport(ord.country), 'ISO-8859-15').encode('utf8'))
            elif 'espa' in ord.country:
                res_add('\n<country>%s</country>' % unicode(formatExport(ord.country), 'ISO-8859-15').encode('utf8'))
            elif 'XICO' in ord.country:
                res_add('\n<country>%s</country>' % unicode(formatExport(ord.country), 'ISO-8859-15').encode('utf8'))
            else:
                res_add('\n<country>%s</country>' % formatExport(ord.country))                                              #string
            res_add('\n</report_order>')

        ###ReportOrder2 objects
        #########################
        for ord2 in lang.objectValues('ReportOrder2'):
            res_add('\n<report_order2>')
            #Basic Property Sheet
            res_add('\n<title>%s</title>' % formatExport(ord2.title))                                                       #string
            res_add('\n<order_id>%s</order_id>' % formatExport(ord2.order_id))                                              #string
            res_add('\n<customer_mail>%s</customer_mail>' % formatExport(ord2.customer_mail))                               #string
            res_add('\n<order_date>%s</order_date>' % formatExport(ord2.order_date))                                        #date
            res_add('\n<order_confirm_date>%s</order_confirm_date>' % formatExport(ord2.order_confirm_date))                #date
            res_add('\n<customer_nameandadress>%s</customer_nameandadress>' % formatExport(ord2.customer_nameandadress))    #text
            res_add('\n<order_shipping_date>%s</order_shipping_date>' % formatExport(ord2.order_shipping_date))             #date
            res_add('\n<report_order2>')

        ###Search objects
        #########################
        for search in lang.objectValues('Search'):
            res_add('\n<search>')
            #Basic Property Sheet
            res_add('\n<title>%s</title>' % formatExport(search.title))                   #string
            res_add('\n<publishdate>%s</publishdate>' % formatExport(search.publishdate)) #date
            res_add('\n</search>')

        ###Zope File objects
        #########################
        for file in lang.objectValues('File'):
            res_add('\n<zope_file url="%s">' % file.absolute_url())
            res_add('\n<file_id>%s</file_id>' % formatExport(file.getId()))
            res_add('\n<content_type>%s</content_type>' % file.content_type)

            file_title = file.title
            if file.getId() == 'PT-SCP-chapter-final-web.pdf':
                file_title = file_title.replace('&aacute;', 'á')

            try:
                res_add('\n<file_title>%s</file_title>' % container.unescape(formatExport(file_title)).encode('utf-8'))
            except:
                if file.getId() in ['TR-SCP-chapter-final-web.pdf', 'ET-SCP-chapter_final-web.pdf', 'FI-SCP-chapter_final-web.pdf']:
                    try:
                        res_add('\n<file_title>%s</file_title>' % file.getId())
                    except:
                        res_add('\nALEC1')
                elif file.getId() in ['ES-SCP-chapter-final-web.pdf', 'PT-SCP-chapter-final-web.pdf']:
                    res_add('\n<file_title>%s</file_title>' % formatExport(file_title))
                elif file.getId() == 'toprep02_2001.pdf':
                    res_add('\n<file_title>European Topic Centre on Inland Waters. Annual topic update 2000. Topic report No 2/2001</file_title>')
                elif file.getId() == 'Topic_5_2002.pdf':
                    res_add('\n<file_title>Emissions of atmospheric pollutants in Europe, 1990-99</file_title>')
                elif file.getId() == 'Topic_7.pdf':
                    res_add('\n<file_title>Greenhouse gas emission trends in Europe, 1990-2000</file_title>')
                elif file.getId() == 'topic_4.pdf':
                    res_add('\n<file_title>Air quality in Europe. State and trends 1990-99</file_title>')
                elif file.absolute_url() in file_exceptions:
                    res_add('\n<file_title>%s</file_title>' % unicode(formatExport(file_title), 'ISO-8859-15').encode('utf-8'))
                else:
                    res_add('\n<file_title>%s</file_title>' % formatExport(file_title).encode('utf-8'))

            res_add('\n</zope_file>')

        ###Zope Image objects
        #########################
        for img in lang.objectValues('Image'):
            res_add('\n<zope_image url="%s">' % img.absolute_url())
            res_add('\n<id>%s</id>' % formatExport(img.getId()))
            res_add('\n</zope_image>')

        res_add('\n</language_report>')
    res_add('\n</report>')

res_add('\n</reports>')
print ''.join(res)
return printed
