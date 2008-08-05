import urllib2
import sys
from xml.sax.handler import ContentHandler
from xml.sax import *
from cStringIO import StringIO
from types import StringType, UnicodeType

class Report(object):
    """ Encapsulate report
        >>> report = Report(id='myreport', title="My Title", for_sale=True)
        >>> isbn = report.get('isbn')
        >>> isbn is None
        True
        >>> report.get('for_sale', False)
        True
    """
    #def __init__(self, id, lang='en', **kwargs):
    def __init__(self):
        """
            @param id:                     String;
            @param lang:                   String;
            @param title:                  String;
            @param description:            String;
            @param file                    File;
            @param relatedItems:           Tuple;
            @param cover_image:            Image;
            @param author:                 String;
            @param isbn:                   String;
            @param order_id:               String;
            @param for_sale:               Boolean;
            @param chapters:               Tuple;
            @param metadata_upload:        File;
            @param owner_password:         String;
            @param user_password:          String;
            @param serial_title_type:      String;
            @param serial_title_number:    Integer;
            @param serial_title_year:      String;
            @param serial_title_alt:       String;
            @param creators:               Tuple;
            @param publishers:             Tuple;
            @param themes:                 Tuple;
            @param price:                  Float;
            @param order_override_text:    String;
            @param order_extra_text:       String;
            @param pages:                  Integer;
            @param copyrights:             String;
            @param trailer:                String;
        """
#        self.id = id
#        self.lang = lang
#        for key, value in kwargs.items():
#            setattr(self, key, value)

    def set(self, key, value):
        return setattr(self, key, value)
    def get(self, key, default=None):
        return getattr(self, key, default)
    def items(self):
        return self.__dict__.items()
    def keys(self):
        return self.__dict__.keys()
    def values(self):
        return self.__dict__.values()
    def getId(self):
        return self.id
    def language(self, default='en'):
        return self.get('lang', default)

REPORT_SUB_OBJECTS = ['cover_image', 'redirect', 'tag', 'language_report']
LANGUAGE_REPORT_SUB_OBJECTS = ['report_chapter', 'report_file', 'report_order', 'report_order2', 'search', 'zope_file', 'zope_image']

LANGUAGE_REPORT_PROPS = ['reporttitle', 'language', 'description', 'isbn', 'catalogue', 'pages', 'trailer']

class zreports_handler(ContentHandler):
    """ """

    def __init__(self):
        """ constructor """
        self.__reports = []
        self.__data = []

        self.__report_context = 0
        self.__report_current = ''
        self.__language_report_context = 0
        self.__language_report_current = ''

    def get_reports(self):
        return self.__reports

    def startElement(self, name, attrs):
        if name == 'report':
            self.__report_context = 1
            self.__report_current = Report()

        if name == 'cover_image':
            self.__report_current.set('rep_cover_image', attrs['url'])

        if name == 'language_report':
            self.__language_report_context = 1
            self.__language_report_current = Report()

        if name in REPORT_SUB_OBJECTS:
            self.__report_context = 0
        if name in LANGUAGE_REPORT_SUB_OBJECTS:
            self.__language_report_context = 0

    def endElement(self, name):
        if name == 'report':
            self.__report_context = 0
            ###OLD
            #self.__reports.append(self.__report_current)
            self.__report_current = ''

        if name == 'language_report':
            self.__language_report_context = 0
            #set properties from Report object
            self.__language_report_current.set('id', self.__report_current.get('id'))
            self.__language_report_current.set('themes', self.__report_current.get('categories'))
            self.__language_report_current.set('author', self.__report_current.get('author'))
            self.__language_report_current.set('for_sale', self.__report_current.get('order_override'))
            self.__language_report_current.set('serial_title_type', self.__report_current.get('reporttype'))
            self.__language_report_current.set('serial_title_number', self.__report_current.get('reportnum'))
            self.__language_report_current.set('serial_title_year', self.__report_current.get('series_year'))
            self.__language_report_current.set('serial_title_alt', self.__report_current.get('series_title'))
            self.__language_report_current.set('price', self.__report_current.get('price_euro'))
            self.__language_report_current.set('order_override_text', self.__report_current.get('order_override_text'))
            self.__language_report_current.set('order_extra_text', self.__report_current.get('order_extra_text'))
            self.__language_report_current.set('copyrights', self.__report_current.get('copyright'))
            self.__language_report_current.set('cover_image', self.__report_current.get('rep_cover_image'))

            #add language report to results
            self.__reports.append(self.__language_report_current)
            self.__language_report_context = ''

        if name in REPORT_SUB_OBJECTS:
            self.__report_context = 1
        if name in LANGUAGE_REPORT_SUB_OBJECTS:
            self.__language_report_context = 1

        if self.__report_context:
            data = u''.join(self.__data).strip()
            self.__data = []
            self.__report_current.set(name, data)

        if self.__language_report_context:
            if name in LANGUAGE_REPORT_PROPS:
                data = u''.join(self.__data).strip()
                self.__data = []
                if name == 'reporttitle':
                    self.__language_report_current.set('title', data)
                elif name == 'language':
                    self.__language_report_current.set('lang', data)
                elif name == 'catalogue':
                    self.__language_report_current.set('order_id', data)
                else:
                    self.__language_report_current.set(name, data)

    def characters(self, content):
        if self.__report_context or self.__language_report_context:
            self.__data.append(content)

class zreports_parser:
    """ """

    def __init__(self):
        """ """
        pass

    def parseContent(self, xml_string):
        """ """
        chandler = zreports_handler()
        parser = make_parser()
        parser.setContentHandler(chandler)
        parser.setFeature(handler.feature_external_ges, 0)
        inpsrc = InputSource()
        inpsrc.setByteStream(StringIO(xml_string))
        try:
            parser.parse(inpsrc)
            return chandler
        except:
            return None

    def parseHeader(self, file):
        parser = make_parser()
        chandler = zreports_handler()
        parser.setContentHandler(chandler)
        try:    parser.setFeature(handler.feature_external_ges, 0)
        except: pass
        inputsrc = InputSource()

        try:
            if type(file) is StringType:
                inputsrc.setByteStream(StringIO(file))
            else:
                filecontent = file.read()
                inputsrc.setByteStream(StringIO(filecontent))
            parser.parse(inputsrc)
            return chandler
        except:
            return None

#Parse exported ZReports data
f = urllib2.urlopen("http://10.0.0.24:8080/export_ZReports")
s = f.read()
parser = zreports_parser()
data = parser.parseHeader(s)

res = data.get_reports()

for k in res: print k.cover_image