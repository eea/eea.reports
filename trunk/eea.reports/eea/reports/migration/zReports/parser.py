import urllib2
import sys
from xml.sax.handler import ContentHandler
from xml.sax import *
from cStringIO import StringIO
from types import StringType, UnicodeType
from cgi import FieldStorage
from ZPublisher.HTTPRequest import FileUpload

class Report(object):
    """ Encapsulate report
    """
    def __init__(self):
        """
            @param id:                                String;
            @param lang:                              String;
            @param title:                             String;
            @param description:                       String;
            @param file                               File;
            @param relatedItems:                      Tuple;
            @param cover_image_file:                  ImageFile;
            @param author:                            String;
            @param isbn:                              String;
            @param order_id:                          String;
            @param for_sale:                          Boolean;
            @param chapters:                          Tuple;
            @param metadata_upload:                   File;
            @param owner_password:                    String;
            @param user_password:                     String;
            @param serial_title_type:                 String;
            @param serial_title_number:               Integer;
            @param serial_title_year:                 String;
            @param serial_title_alt:                  String;
            @param creators_existing_keywords:        Tuple;
            @param creators_keywords                  Tuple;
            @param publishers_existing_keywords:      Tuple;
            @param publishers_keywords:               Tuple;
            @param themes:                            Tuple;
            @param price:                             Float;
            @param order_override_text:               String;
            @param order_extra_text:                  String;
            @param pages:                             Integer;
            @param copyrights:                        String;
            @param trailer:                           String;
        """
        pass

    def set(self, key, value):
        return setattr(self, key, value)

    def __call__(self, all=False):
        if all:
            return self.__dict__
        return dict((key, value) for key, value in self.items()
                    if key not in ('id', 'lang', 'title', 'cover_image'))

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
        self.__chapter_context = 0
        self.__chapter_titles = []

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

        if name == 'report_chapter':
            self.__chapter_context = 1

        if name in REPORT_SUB_OBJECTS:
            self.__report_context = 0
        if name in LANGUAGE_REPORT_SUB_OBJECTS:
            self.__language_report_context = 0

    def endElement(self, name):
        if name == 'report':
            self.__report_context = 0
            self.__report_current = ''

        if name == 'language_report':
            self.__language_report_context = 0
            #set properties from Report object
            self.__language_report_current.set('id', self.__report_current.get('id'))
            self.__language_report_current.set('themes', self.__report_current.get('categories').split('###'))
            self.__language_report_current.set('author', self.__report_current.get('author'))
            for_sale = self.__report_current.get('order_override', False)
            self.__language_report_current.set('for_sale', for_sale in (u'True', 'True', True))
            self.__language_report_current.set('serial_title_type', self.__report_current.get('reporttype'))
            try:
                serial_number = int(self.__report_current.get('reportnum'))
            except (ValueError, TypeError):
                serial_number = 0
            self.__language_report_current.set('serial_title_number', serial_number)
            try:
                serial_year = int(self.__report_current.get('series_year'))
            except ValueError, TypeError:
                serial_year = 1990
            self.__language_report_current.set('serial_title_year', serial_year)
            self.__language_report_current.set('serial_title_alt', self.__report_current.get('series_title'))
            self.__language_report_current.set('price', self.__report_current.get('price_euro'))
            self.__language_report_current.set('order_override_text', self.__report_current.get('order_override_text'))
            self.__language_report_current.set('order_extra_text', self.__report_current.get('order_extra_text'))
            self.__language_report_current.set('copyrights', self.__report_current.get('copyright'))
            cover_image_url = self.__report_current.get('rep_cover_image')
            cover_image_file = grab_file_from_url(cover_image_url)
            self.__language_report_current.set('cover_image_file', cover_image_file)
            self.__language_report_current.set('creators_existing_keywords', self.__report_current.get('creators_orgs').split('###'))
            creators = self.__report_current.get('creators').replace('\n', '').split('###')
            creators = [x.strip() for x in creators if x.strip()]
            self.__language_report_current.set('creators_keywords', creators)
            self.__language_report_current.set('publishers_existing_keywords', self.__report_current.get('publishers_orgs').split('###'))
            publishers = self.__report_current.get('publishers').replace('\n', '').split('###')
            publishers = [x.strip() for x in publishers if x.strip()]
            self.__language_report_current.set('publishers_keywords', publishers)


            #add language report to results
            self.__language_report_current.set('chapters', self.__chapter_titles)
            self.__reports.append(self.__language_report_current)
            self.__language_report_context = ''
            self.__chapter_titles = []
            
        if name == 'report_chapter':
            self.__chapter_context = 0
        
        if name == 'title' and self.__chapter_context:
            data = u''.join(self.__data).strip()
            self.__chapter_titles.append(data)

        if name in REPORT_SUB_OBJECTS:
            self.__report_context = 1
        if name in LANGUAGE_REPORT_SUB_OBJECTS:
            self.__language_report_context = 1

        if self.__report_context:
            data = u''.join(self.__data).strip()
            self.__report_current.set(name, data)

        if self.__language_report_context:
            if name in LANGUAGE_REPORT_PROPS:
                data = u''.join(self.__data).strip()
                if name == 'reporttitle':
                    self.__language_report_current.set('title', data)
                elif name == 'language':
                    self.__language_report_current.set('lang', data)
                elif name == 'catalogue':
                    self.__language_report_current.set('order_id', data)
                if name == 'pages':
                    try:
                        pages = int(data)
                    except (TypeError, ValueError):
                        pages = 0
                    self.__language_report_current.set(name, pages)
                else:
                    self.__language_report_current.set(name, data)
        self.__data = []

    def characters(self, content):
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
        parser.setFeature(chandler.feature_external_ges, 0)
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
        try:    parser.setFeature(chandler.feature_external_ges, 0)
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

def get_reports(url="http://10.0.0.24:8080/export_ZReports"):
    """ Returns a list of Report instances.
    """
    f = urllib2.urlopen(url)
    s = f.read()
    parser = zreports_parser()
    data = parser.parseHeader(s)
    return data.get_reports()

def grab_file_from_url(url, ctype='image/jpg', zope=True):
    """ Returns a FileUpload instance with data from given url.
    """
    try:
        url_file = urllib2.urlopen(url)
    except:
        return None
    filename = url.split('/')[-1]
    data = url_file.read()
    size = len(data)
    if not zope:
        return data
    fp = StringIO(data)
    env = {'REQUEST_METHOD':'PUT'}
    headers = {'content-type' : ctype,
               'content-length': size,
               'content-disposition':'attachment; filename=%s' % filename}
    fs = FieldStorage(fp=fp, environ=env, headers=headers)
    return FileUpload(fs)

if __name__ == '__main__':
    print len(get_reports())
