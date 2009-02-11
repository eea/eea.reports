#parameters=report_year='',report_from='',report_to=''
#title=Export ZReports SortOrder
# -*- coding: utf8 -*-

# Get the HTML request and response objects
request = container.REQUEST
RESPONSE =  request.RESPONSE

# REQUEST parameters
if report_year != '':
    report_year = int(report_year)
    if report_from == '':   report_from = 0
    else:                   report_from = int(report_from)
    if report_to == '': report_to = 0
    else:               report_to = int(report_to)

# Set content type
RESPONSE.setHeader('content-type', 'text/xml')

root = container.restrictedTraverse('/')
report_metatype = ['Multilingual Report']

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
            res = res.replace('<! Table 3 end -->', '<!-- Table 3 end -->')
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
    if excep1 in res:
        findex = res.find(excep1)
        res = res[:findex+len(excep1)] + '&Oslash;' + res[findex+1+len(excep1):]
    if excep2 in res:
        findex = res.find(excep2)
        res = res[:findex+len(excep2)] + '&micro;' + res[findex+1+len(excep2):]
    for k in [excep3, excep4, excep5, excep6, excep7]:
        if k in res: res = unicode(res, 'ISO-8859-15').encode('utf8')

    # HTML entities
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

file_exceptions = [
'state_of_environment_report_2005_1/da/DA-summary.pdf'
,'state_of_environment_report_2005_1/da/DA_DA-ppt.ppt'
,'state_of_environment_report_2005_1/cs/CS_CS-ppt.ppt'
,'state_of_environment_report_2005_1/de/AT_DE-ppt.ppt'
,'state_of_environment_report_2005_1/de/AT_DE-countryprofile.pdf'
,'state_of_environment_report_2005_1/es/ES-countryprofile.pdf'
,'state_of_environment_report_2005_1/es/part-b_ES.pdf'
,'state_of_environment_report_2005_1/et/ET-summary.pdf'
,'state_of_environment_report_2005_1/et/ET-countryprofile.pdf'
,'state_of_environment_report_2005_1/et/ET_ET-ppt.ppt'
,'state_of_environment_report_2005_1/fi/FI-summary.pdf'
,'state_of_environment_report_2005_1/fi/FI_FI-ppt.ppt'
,'state_of_environment_report_2005_1/fr/FR-summary.pdf'
,'state_of_environment_report_2005_1/fr/BE_FR-ppt.ppt'
,'state_of_environment_report_2005_1/fr/FR_FR-ppt.ppt'
,'state_of_environment_report_2005_1/fr/LU_FR-ppt.ppt'
,'state_of_environment_report_2005_1/fr/CH_FR-ppt.ppt'
,'state_of_environment_report_2005_1/hu/HU-summary.pdf'
,'state_of_environment_report_2005_1/hu/part-b_HU.pdf'
,'state_of_environment_report_2005_1/hu/HU-countryprofile.pdf'
,'state_of_environment_report_2005_1/hu/HU_HU-ppt.ppt'
,'state_of_environment_report_2005_1/is/IS-summary.pdf'
,'state_of_environment_report_2005_1/is/IS-countryprofile.pdf'
,'state_of_environment_report_2005_1/is/part-b_IS.pdf'
,'state_of_environment_report_2005_1/nl/BE_NL-countryprofile.pdf'
,'state_of_environment_report_2005_1/no/NO-summary.pdf'
,'state_of_environment_report_2005_1/pl/PL_PL-ppt.ppt'
,'state_of_environment_report_2005_1/pt/PT-summary.pdf'
,'state_of_environment_report_2005_1/sk/SK-countryprofile.pdf'
,'state_of_environment_report_2005_1/sk/part-a_SK.pdf'
,'state_of_environment_report_2005_1/sv/SV-summary.pdf'
,'state_of_environment_report_2005_1/sv/part-b_SV.pdf'
,'state_of_environment_report_2005_1/tr/TR-countryprofile.pdf'
,'state_of_environment_report_2005_1/tr/TR_TR-ppt.ppt'
,'state_of_environment_report_2005_1/tr/part-b_TR.pdf',
'briefing_2004_2/es/ES_Briefing-Energy_web.pdf',
'briefing_2004_2/fr/FR_Briefing-Energy_web.pdf',
'briefing_2004_2/tr/TR_Briefing-Energy_web.pdf',
'briefing_2004_2/sk/SK_Briefing-Energy_web.pdf',
'briefing_2004_2/is/IS_Briefing-Energy_web.pdf',
'briefing_2004_2/cs/CS_Briefing-Energy_web.pdf',
'briefing_2004_2/sv/SV_Briefing-Energy_web.pdf',
'briefing_2004_2/pt/PT_Briefing-Energy_web.pdf'
]

#Sort reports by year
reports = {}
for report in root.objectValues(report_metatype):
    val = reports.get(report.series_year, [])
    val.append(report)
    reports[report.series_year] = val

exported_reports = []
if report_year != '':
    data = list(reports[int(report_year)])
    if report_to == 0: report_to = len(data)
    exported_reports.extend(data[report_from:report_to])
else:
    for report in reports.keys():
        exported_reports.extend(reports[report])

# Export content
res_add("""<?xml version="1.0" encoding="utf-8"?>""")
res_add('\n<reports>')

for report in exported_reports:
    res_add('\n<report>')
    res_add('\n<id>%s</id>' % report.id)
    res_add('\n<reporttype>%s</reporttype>' % formatExport(report.reporttype))
    res_add('\n<reportnum>%s</reportnum>' % formatExport(report.reportnum))
    res_add('\n<series_year>%s</series_year>' % formatExport(report.series_year))
    res_add('\n<series_title>%s</series_title>' % formatExport(report.series_title))

    ###Language Report objects
    ##########################
    language_reports = report.objectValues('Language Report')
    for lang_rep in language_reports:
        if lang_rep.language.lower() == 'en':
            en_lang_rep = lang_rep
            break
    language_reports.remove(lang_rep)
    language_reports.insert(0, lang_rep)

    for lang in language_reports:
        res_add('\n<language_report url="%s">' % lang.absolute_url())
        res_add('\n<id>%s</id>' % lang.id)
        res_add('\n<language>%s</language>' % formatExport(lang.language))

        ###Report File objects
        #########################
        for rep_file in lang.objectValues('Report File'):
            res_add('\n<report_file url="%s" id="%s" pagenumber="%s">' %
                    (rep_file.absolute_url(), rep_file.getId(), formatExport(rep_file.pagenumber)))
            res_add('\n<report_file_title></report_file_title>')
            res_add('\n</report_file>')

        ###Zope File objects
        #########################
        files = lang.objectValues('File')

        if lang.absolute_url(1) in ['eea_report_2006_8/en', 'eea_report_2008_6/en']:
            files.extend(lang.factsheets.objectValues('File'))

        for file in files:
            res_add('\n<zope_file url="%s" id="%s">' % (file.absolute_url(), file.getId()))
            file_title = file.title
            if file.getId() == 'PT-SCP-chapter-final-web.pdf':
                file_title = file_title.replace('&aacute;', 'á')

            if report.series_year == -1 and not lang.language in ['bg', 'el']:
                res_add('\n<file_title>%s</file_title>' % container.unescape(unicode(formatExport(file_title), 'iso-8859-15')).encode('utf8')) #text
            elif report.series_year == -1 and lang.language == 'el':
                res_add('\n<file_title>%s</file_title>' % container.unescape(unicode(formatExport(file_title), 'iso-8859-7')).encode('utf8')) #text
            else:
                try:
                    res_add('\n<file_title>%s</file_title>' % container.unescape(formatExport(file_title)).encode('utf-8'))
                except:
                    if file.getId() in ['TR-SCP-chapter-final-web.pdf', 'ET-SCP-chapter_final-web.pdf', 'FI-SCP-chapter_final-web.pdf']:
                        try:
                            res_add('\n<file_title>%s</file_title>' % file.getId())
                        except:
                            res_add('\n<file_title></file_title>')
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
                    elif file.absolute_url(1) in file_exceptions:
                        res_add('\n<file_title>%s</file_title>' % unicode(formatExport(file_title), 'ISO-8859-15').encode('utf-8'))
                    else:
                        try:
                            res_add('\n<file_title>%s</file_title>' % formatExport(file_title).encode('utf-8'))
                        except:
                            res_add('\n<file_title>%s</file_title>' % formatExport(file_title))
            res_add('\n</zope_file>')

        res_add('\n</language_report>')
    res_add('\n</report>')

res_add('\n</reports>')
print ''.join(res)
return printed