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
            @param file                               Dict;
            @param relatedItems:                      Iterator;
            @param cover_image_file:                  URL;
            @param author:                            String;
            @param isbn:                              String;
            @param order_id:                          String;
            @param for_sale:                          Boolean;
            @param chapters:                          Dict;
            @param serial_title_type:                 String;
            @param serial_title_number:               Integer;
            @param serial_title_year:                 String;
            @param serial_title_alt:                  String;
            @param creators_existing_keywords:        Iterator;
            @param creators_keywords                  Iterator;
            @param publishers_existing_keywords:      Iterator;
            @param publishers_keywords:               Iterator;
            @param themes:                            Iterator;
            @param price:                             Float;
            @param order_override_text:               String;
            @param order_extra_text:                  String;
            @param pages:                             Integer;
            @param copyrights:                        String;
            @param trailer:                           String;
            @param effectiveDate                      String
            @param expirationDate                     String;
            @param images                             Dict;
            @param replaces                           Iterator;
            @param is_replaced_by                     Iterator;
            @param has_part                           Iterator;
            @param is_part_of                         Iterator;
        """
        pass

    def set(self, key, value):
        return setattr(self, key, value)

    def delete(self, key):
        if hasattr(self, key):
            return delattr(self, key)

    def __call__(self, all=False):
        if all:
            return self.__dict__
        return dict((key, value) for key, value in self.items()
                    if key not in ('id', 'lang', 'title', 'cover_image', 'file'))

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
LANGUAGE_REPORT_SUB_OBJECTS = [
    'report_chapter', 'report_file', 'report_order', 'report_order2',
    'search', 'zope_file', 'zope_image'
]

LANGUAGE_REPORT_PROPS = [
    'reporttitle', 'language', 'description',
    'isbn', 'catalogue', 'pages', 'trailer', 'eeaid'
]

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
        self.__image_context = 0
        self.__images = {}
        self.__image_data = []
        self.__chapters = {}
        self.__chapter_titles = []
        self.__report_files = {}
        self.__report_file_data = []

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

        if name == 'report_file':
            self.__report_file_data.append(attrs['url'])

        if name == 'zope_file':
            self.__report_file_data.append(attrs['url'])

        if name == 'zope_image':
            self.__image_context = 1
            self.__image_data.append(attrs['url'])

        if name in REPORT_SUB_OBJECTS:
            self.__report_context = 0
        if name in LANGUAGE_REPORT_SUB_OBJECTS:
            self.__language_report_context = 0

    def endElement(self, name):
        if name == 'report':
            self.__report_context = 0
            self.__report_current = ''

        if name == 'report_file_title':
            data = u''.join(self.__data).strip()
            self.__report_file_data.append(data)

        if name == 'file_title':
            data = u''.join(self.__data).strip()
            self.__report_file_data.append(data)

        if name in ('zope_file', 'report_file'):
            self.__report_files[self.__report_file_data[0]] = self.__report_file_data[1]
            self.__report_file_data = []

        if name == 'language_report':
            self.__language_report_context = 0
            #set properties from Report object
            self.__language_report_current.set('id', self.__report_current.get('id'))
            self.__language_report_current.set('themes', self.__report_current.get('categories').split('###'))
            self.__language_report_current.set('author', self.__report_current.get('author'))
            for_sale = self.__report_current.get('order_override', True)
            self.__language_report_current.set('for_sale', for_sale in (u'False', 'False', False, 0))
            self.__language_report_current.set('serial_title_type', self.__report_current.get('reporttype'))
            try:
                serial_number = int(self.__report_current.get('reportnum'))
            except (ValueError, TypeError):
                serial_number = 0
            self.__language_report_current.set('serial_title_number', serial_number)
            try:
                serial_year = int(self.__report_current.get('series_year'))
            except (ValueError, TypeError):
                serial_year = 1990
            self.__language_report_current.set('serial_title_year', serial_year)
            self.__language_report_current.set('serial_title_alt', self.__report_current.get('series_title'))
            self.__language_report_current.set('price', self.__report_current.get('price_euro'))
            self.__language_report_current.set('order_override_text', self.__report_current.get('order_override_text'))
            self.__language_report_current.set('order_extra_text', self.__report_current.get('order_extra_text'))
            self.__language_report_current.set('copyrights', self.__report_current.get('copyright'))
            cover_image_url = self.__report_current.get('rep_cover_image')
            self.__language_report_current.set('cover_image_file', cover_image_url)
            self.__language_report_current.set('creators_existing_keywords', self.__report_current.get('creators_orgs').split('###'))
            creators = self.__report_current.get('creators').replace('\n', '').split('###')
            creators = [x.strip() for x in creators if x.strip()]
            self.__language_report_current.set('creators_keywords', creators)
            self.__language_report_current.set('publishers_existing_keywords', self.__report_current.get('publishers_orgs').split('###'))
            publishers = self.__report_current.get('publishers').replace('\n', '').split('###')
            publishers = [x.strip() for x in publishers if x.strip()]
            self.__language_report_current.set('publishers_keywords', publishers)

            # Relations
            replaces = self.__report_current.get('Replaces').replace('\n', '').split('###')
            replaces = [x.strip() for x in replaces if x.strip()]
            replaces = set([x.split('/')[-1] for x in replaces])
            self.__language_report_current.set('replaces', replaces)

            is_replaced_by = self.__report_current.get('IsReplacedBy').replace('\n', '').split('###')
            is_replaced_by = [x.strip() for x in is_replaced_by if x.strip()]
            is_replaced_by = set([x.split('/')[-1] for x in is_replaced_by])
            self.__language_report_current.set('is_replaced_by', is_replaced_by)

            has_part = self.__report_current.get('HasPart').replace('\n', '').split('###')
            has_part = [x.strip() for x in has_part if x.strip()]
            has_part = set([x.split('/')[-1] for x in has_part])
            self.__language_report_current.set('has_part', has_part)

            is_part_of = self.__report_current.get('IsPartOf').replace('\n', '').split('###')
            is_part_of = [x.strip() for x in is_part_of if x.strip()]
            is_part_of = set([x.split('/')[-1] for x in is_part_of])
            self.__language_report_current.set('is_part_of', is_part_of)

            # Effective date
            self.__language_report_current.set('effectiveDate', self.__report_current.get('publishdate'))
            # Expiration date
            self.__language_report_current.set('expirationDate', self.__report_current.get('expiry_date'))

            #set files
            self.__language_report_current.set('file', self.__report_files)

            #add language report to results
            self.__language_report_current.set('chapters', self.__chapters)

            #add images
            self.__language_report_current.set('images', self.__images)

            self.__reports.append(self.__language_report_current)
            self.__language_report_context = ''

            self.__report_files = {}
        #
        # Report chapter
        #
        if name == 'report_chapter':
            self.__chapters[self.__chapter_titles[0]] = (self.__chapter_titles[1], self.__chapter_titles[2])
            self.__chapter_titles = []
            self.__chapter_context = 0

        if name == 'id' and self.__chapter_context:
            data = u''.join(self.__data).strip()
            self.__chapter_titles.append(data)

        if name == 'title' and self.__chapter_context:
            data = u''.join(self.__data).strip()
            self.__chapter_titles.append(data)

        if name == 'content' and self.__chapter_context:
            data = u''.join(self.__data).strip()
            self.__chapter_titles.append(data)
        #
        # Zope image
        #
        if name == 'zope_image':
            zid = self.__image_data[1]
            zurl =  self.__image_data[0]
            self.__images[zid] = zurl
            self.__image_data = []
            self.__image_context = 0

        if name == 'id' and self.__image_context:
            data = u''.join(self.__data).strip()
            self.__image_data.append(data)

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
                if name in ('pages', 'eeaid'):
                    try:
                        data = int(data)
                    except (ValueError, TypeError):
                        data = 0
                    self.__language_report_current.set(name, data)
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
        parser.parse(inpsrc)
        return chandler

    def parseHeader(self, file):
        parser = make_parser()
        chandler = zreports_handler()
        parser.setContentHandler(chandler)
        try:    parser.setFeature(chandler.feature_external_ges, 0)
        except: pass
        inputsrc = InputSource()

        if type(file) is StringType:
            inputsrc.setByteStream(StringIO(file))
        else:
            filecontent = file.read()
            inputsrc.setByteStream(StringIO(filecontent))
        parser.parse(inputsrc)
        return chandler

def get_reports(url="http://10.0.0.24:8080/export_ZReports"):
    """ Returns a list of Report instances.
    """
    f = urllib2.urlopen(url)
    s = f.read()
    parser = zreports_parser()
    data = parser.parseHeader(s)
    return data.get_reports()

def get_file_upload(data, filename, ctype):
    """ Returns an instance of FileUpload from given data stream
    """
    fp = StringIO(data)
    env = {'REQUEST_METHOD':'PUT'}
    headers = {'content-length': len(data),
               'content-disposition':'attachment; filename=%s' % filename}
    if ctype:
        headers['content-type'] = ctype
    fs = FieldStorage(fp=fp, environ=env, headers=headers)
    return FileUpload(fs)

def grab_file_from_url(url, ctype='image/jpg', zope=True):
    """ Returns a data stream if zope is False
        or a FileUpload instance with data from given url.
    """
    try:
        url_file = urllib2.urlopen(url)
    except:
        return None
    filename = url.split('/')[-1]
    data = url_file.read()
    size = len(data)
    if zope:
        return get_file_upload(data, filename, ctype)
    return data

if __name__ == '__main__':
    print len(get_reports())
