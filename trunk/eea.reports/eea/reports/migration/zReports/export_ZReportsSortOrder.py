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
    return res

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
    res_add('\n<id>%s</id>' % formatExport(report.id))

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
        res_add('\n<id>%s</id>' % formatExport(lang.id))
        res_add('\n<language>%s</language>' % formatExport(lang.language))

        ###Report File objects
        #########################
        for rep_file in lang.objectValues('Report File'):
            res_add('\n<report_file url="%s" id="%s" pagenumber="%s">' %
                    (rep_file.absolute_url(), formatExport(rep_file.getId()), formatExport(rep_file.pagenumber)))
            res_add('\n</report_file>')

        ###Zope File objects
        #########################
        files = lang.objectValues('File')

        if lang.absolute_url(1) in ['eea_report_2006_8/en', 'eea_report_2008_6/en']:
            files.extend(lang.factsheets.objectValues('File'))

        for file in files:
            res_add('\n<zope_file url="%s" id="%s">' % (file.absolute_url(), formatExport(file.getId())))
            res_add('\n</zope_file>')

        res_add('\n</language_report>')
    res_add('\n</report>')

res_add('\n</reports>')
print ''.join(res)
return printed