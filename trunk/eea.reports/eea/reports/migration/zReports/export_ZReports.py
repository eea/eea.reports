# -*- coding: utf8 -*-

# Get the HTML request and response objects
request = container.REQUEST
RESPONSE =  request.RESPONSE

# Set content type
RESPONSE.setHeader('content-type', 'text/xml')

root = container.restrictedTraverse('/')
report_metatype = ['Multilingual Report']
reports_year = [2007, 2008]

res = []
res_add = res.append

def formatExport(data):
    res = data
    data_type = container.getType(data)
    if data_type in ['list', 'tuple']:
        res = '###'.join([str(x) for x in data])
    if data_type in ['int', 'date']:
        res = str(res)
    if len(res) > 5:
        if '%' in res:
            res = '<![CDATA[%s]]>' % res
    return res

# Export content
res_add("""<?xml version="1.0" encoding="utf-8"?>""")
res_add('\n<reports>')

for report in root.objectValues(report_metatype):
    if report.series_year in reports_year:
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
        res_add('\n<expiry_date>%s</expiry_date>' % formatExport(report.expiry_date))                                 #date
        res_add('\n<version_number>%s</version_number>' % formatExport(report.version_number))                        #string
        res_add('\n<price_euro>%s</price_euro>' % formatExport(report.price_euro))                                    #string
        res_add('\n<creators_orgs>%s</creators_orgs>' % formatExport(report.creators_orgs))                           #multiple selection
        res_add('\n<creators>%s</creators>' % formatExport(report.creators))                                          #lines
        res_add('\n<publishers_orgs>%s</publishers_orgs>' % formatExport(report.publishers_orgs))                     #multiple selection
        res_add('\n<publishers>%s</publishers>' % formatExport(report.publishers))                                    #lines
        res_add('\n<coverage_time_from>%s</coverage_time_from>' % formatExport(report.coverage_time_from))            #date
        res_add('\n<coverage_time_to>%s</coverage_time_to>' % formatExport(report.coverage_time_to))                  #date

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
            res_add('\n<id>%s</id>' % formatExport(img.getId()))        #string
            res_add('\n<title>%s</title>' % formatExport(img.title))    #string

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
            res_add('\n<redirect redirect_to="%s" />' % formatExport(rdr.redirect_to))  #string


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
            res_add('\n<language_report>')
            #Basic Property Sheet
            res_add('\n<id>%s</id>' % formatExport(lang.id))                                                     #string
            res_add('\n<language>%s</language>' % formatExport(lang.language))                                   #string
            res_add('\n<title>%s</title>' % formatExport(lang.title))                                            #string

            if lang.isbn == '978-92-9167-919-5':
                res_add('\n<description>%s</description>' % unicode(formatExport(lang.description), 'latin1').encode('utf-8'))  #text
            else:
                res_add('\n<description>%s</description>' % container.unescape(formatExport(lang.description)).encode('utf-8')) #text

            res_add('\n<trailer>%s</trailer>' % formatExport(lang.trailer))                                      #text
            res_add('\n<reporttitle>%s</reporttitle>' % formatExport(lang.reporttitle))                          #string
            res_add('\n<sections>%s</sections>' % formatExport(lang.sections))                                   #lines
            res_add('\n<order_override_lang>%s</order_override_lang>' % formatExport(lang.order_override_lang))  #boolean

            #Extra Property Sheet
            res_add('\n<pages>%s</pages>' % formatExport(lang.pages))                    #int
            res_add('\n<isbn>%s</isbn>' % formatExport(lang.isbn))                       #string
            res_add('\n<catalogue>%s</catalogue>' % formatExport(lang.catalogue))        #string
            res_add('\n<sort_title>%s</sort_title>' % formatExport(lang.sort_title))     #string

            #Manager Property Sheet
            res_add('\n<langreleased>%s</langreleased>' % formatExport(lang.langreleased))   #boolean

            ###Report Chapter objects
            #########################
            for chp in lang.objectValues('Report Chapter'):
                res_add('\n<report_chapter>')
                #Basic Property Sheet
                res_add('\n<id>%s</id>' % formatExport(chp.id))                             #string
                res_add('\n<title>%s</title>' % formatExport(chp.title))                    #text
                res_add('\n<content>%s</content>' % formatExport(chp.content))              #string
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
                res_add('\n<id>%s</id>' % formatExport(rep_file.getId()))                                       #string
                res_add('\n<title>%s</title>' % formatExport(rep_file.title))                                   #string
                res_add('\n<tags>%s</tags>' % formatExport(rep_file.tags))                                      #lines
                if rep_file.getId() == 'eea_briefing_1_2007-de.pdf':
                    res_add('\n<file_description>%s</file_description>' % unicode(formatExport(rep_file.file_description), 'latin1').encode('utf8'))  #text
                else:
                    res_add('\n<file_description>%s</file_description>' % formatExport(rep_file.file_description))  #text
                res_add('\n<pagenumber>%s</pagenumber>' % formatExport(rep_file.pagenumber))                    #int
                res_add('\n</report_file>')

            ###ReportOrder objects
            #########################
            for ord in lang.objectValues('ReportOrder'):
                res_add('\n<report_order>')
                #Basic Property Sheet
                res_add('\n<title>%s</title>' % formatExport(ord.title))                                                    #string
                res_add('\n<order_id>%s</order_id>' % formatExport(ord.order_id))                                           #string
                res_add('\n<customer_mail>%s</customer_mail>' % formatExport(ord.customer_mail))                            #string
                res_add('\n<order_date>%s</order_date>' % formatExport(ord.order_date))                                     #date
                res_add('\n<order_confirm_date>%s</order_confirm_date>' % formatExport(ord.order_confirm_date))             #date
                res_add('\n<customer_nameandadress>%s</customer_nameandadress>' % formatExport(ord.customer_nameandadress)) #text
                res_add('\n<order_shipping_date>%s</order_shipping_date>' % formatExport(ord.order_shipping_date))          #date
                res_add('\n<name>%s</name>' % formatExport(ord.name))                                                       #string
                res_add('\n<organisation>%s</organisation>' % formatExport(ord.organisation))                               #string
                res_add('\n<address>%s</address>' % formatExport(ord.address))                                              #string
                res_add('\n<postal_code>%s</postal_code>' % formatExport(ord.postal_code))                                  #string
                res_add('\n<city>%s</city>' % formatExport(ord.city))                                                       #string
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
                res_add('\n<title>%s</title>' % formatExport(search.title))                     #string
                res_add('\n<publishdate>%s</publishdate>' % formatExport(search.publishdate))   #date
                res_add('\n</search>')

            ###Zope File objects
            #########################
            for file in lang.objectValues('File'):
                res_add('\n<zope_file url="%s">' % file.absolute_url())
                res_add('\n<id>%s</id>' % formatExport(file.getId()))
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

