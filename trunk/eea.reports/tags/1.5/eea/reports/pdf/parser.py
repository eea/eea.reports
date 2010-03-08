import tempfile, logging, os, re
from DateTime import DateTime
from interfaces import IReportPDFParser
from zope.component import getUtility
from slc.publications.pdf.interfaces import IPDFParser
from zope import interface

logger = logging.getLogger('eea.reports.pdf')

class PDFParser(object):
    """ parses metadata from pdf files """

    interface.implements(IReportPDFParser)

    def parse(self, pdf):
        """ Safely parses the given pdf file and returns a mapping of attributes
        """
        try:
            metadata = self._parse(pdf)
        except Exception, err:
            logger.warn('Could not parse pdf metadata: %s', err)
            return {}
        else:
            return metadata

    def _split(self, text):
        if not (isinstance(text, str) or isinstance(text, unicode)):
            return text
        if text.find(';') != -1:
            return [x.strip() for x in text.split(';') if x.strip()]
        return [x.strip() for x in text.split(',') if x.strip()]

    def _fix_metadata(self, metadata):
        """ Update metadata dict
        """
        # Fix authors
        if metadata.has_key('author'):
            metadata['creators'] = self._split(metadata.pop('author', ''))
        if metadata.has_key('creator'):
            creator = self._split(metadata.pop('creator', ''))
            metadata.setdefault('creators', [])
            metadata['creators'].extend([
                x for x in creator if x not in metadata['creators']])

        # Fix effectiveDate
        if metadata.has_key('moddate'):
            metadata['effectiveDate'] = metadata.pop('moddate')
        elif metadata.has_key('modificationdate'):
            metadata['effectiveDate'] = metadata.pop('modificationdate')
        elif metadata.has_key('creationdate'):
            metadata['effectiveDate'] = metadata.pop('creationdate')

        # Fix description
        description = metadata.pop('subject', metadata.get('description', ''))
        if isinstance(description, tuple) or isinstance(description, list):
            description = ' '.join([x.strip() for x in description])
        if not description:
            description = ' '
        metadata['description'] = description

        # Fix subject
        keywords = metadata.pop('keywords', ())
        if keywords:
            keywords = self._split(keywords)
            metadata['subject'] = keywords
        else:
            metadata.pop('subject', '')

        return metadata

    def _parse(self, pdf):
        """ parses the given pdf file and returns a mapping of attributes """
        # Use slc.publications metadata parser
        pdfparser = getUtility(IPDFParser)
        metadata = pdfparser.parse(pdf)
        if not metadata:
            metadata = {}

        # Get plain/text metadata
        tmp_pdf = tempfile.mkstemp(suffix='.pdf')
        fd = open(tmp_pdf[1], 'w')
        fd.write( pdf )
        fd.close()
        statement = 'pdfinfo '
        statement += tmp_pdf[1]
        logger.debug('pdfinfo commandline: %s' % statement)
        ph = os.popen4(statement)
        result = ph[1].read()

        ph[0].close()
        ph[1].close()

        # cleanup the tempfile
        os.remove(tmp_pdf[1])

        # check for errors or encryption
        if result.startswith('Error: No paper information available - using defaults'):
            # Irritating error if libpaper is not configured correctly. For our case this is irrelevant
            pass
        elif result.startswith('Error'):
            error =  result.split('\n')[0]
            logger.error("Error in pdfinfo conversion: %s" % error)
            return metadata
        elif 'command not found' in result:
            return metadata

        crypt_patt = re.compile('Encrypted:.*?copy:no', re.I)
        mobj = crypt_patt.search(result, 1)
        if mobj is not None:
            error = "Error: PDF is encrypted"
            logger.error(error)
            return metadata

        result = result.replace('  ', ' ').replace('\r\n', '\n')
        res_list = result.splitlines()
        new_metadata = [[r.strip() for r in x.split(':', 1)]
                        for x in res_list]
        new_metadata = dict((x[0].lower(), x[1]) for x in new_metadata
                            if len(x) == 2)
        metadata.update(new_metadata)
        #
        # Fix some metadata
        #
        metadata = self._fix_metadata(metadata)
        return metadata
