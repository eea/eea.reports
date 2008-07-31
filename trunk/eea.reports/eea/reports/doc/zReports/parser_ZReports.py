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
            @param reporttype:             String;
            @param reportnum:              Integer;
            @param series_year:            String;
            @param series_title:           String;
            @param creators_orgs:          Tuple;
            @param creators:               Tuple;
            @param publishers_orgs:        Tuple;
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

SUB_OBJECTS = ['cover_image', 'redirect', 'tag', 'language_report']
class zreports_handler(ContentHandler):
    """ """

    def __init__(self):
        """ constructor """
        self.__reports = []
        self.__currentTag = ''
        self.__data = []

        self.__report_context = 0
        self.__report_current = ''

    def get_reports(self):
        return self.__reports

    def startElement(self, name, attrs):
        self.__currentTag = name

        if name == 'report':
            self.__report_context = 1
            self.__report_current = Report()

        if name in SUB_OBJECTS:
            self.__report_context = 0

    def endElement(self, name):
        if name == 'report':
            self.__report_context = 0
            self.__reports.append(self.__report_current)
            self.__report_current = ''

        if name in SUB_OBJECTS:
            self.__report_context = 1

        if self.__report_context:
            data = u''.join(self.__data).strip()
            self.__data = []
            self.__report_current.set(name, data)

        self.__currentTag = ''

    def characters(self, content):
        if self.__report_context:
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
