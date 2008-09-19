""" Adapters
"""
import os
import tempfile
from zope import interface
from zope import component
from Products.ATContentTypes import interface as atctifaces

from eea.reports import interfaces
from eea.reports.config import REPORT_SUBOBJECTS

import logging
logger = logging.getLogger('eea.reports.adapter.report')

@interface.implementer(interfaces.IReport)
@component.adapter(atctifaces.IATFolder)
def ATCTReport(context):
    if not interfaces.IPossibleReportContainer.providedBy(context):
        return None
    return _ATCTReport(context)

class _ATCTReport(object):
    """ Report
    """
    interface.implements(interfaces.IReport)
    component.adapts(atctifaces.IATFolder)

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return '<eea.report %s title="%s">' % (
            self.__class__.__name__, self.context.title)
    __repr__ = __str__

    def restrictSubObjects(self, restriction_type=-1):
        """ Restrict report addable sub-objects to File and Link
        """
        self.context.setConstrainTypesMode(restriction_type)
        if restriction_type != 1:
            return
        self.context.setImmediatelyAddableTypes(REPORT_SUBOBJECTS)
        self.context.setLocallyAllowedTypes(REPORT_SUBOBJECTS)

    def generateImage(self, data=None, width=210, height=297):
        """
        try safely to generate the cover image if pdftk and imagemagick are present
        """
        tmp_pdfin = tmp_pdfout = tmp_gifin = None
        try:
            if getattr(data, 'read', None):
                tmpdata = data.read()
                data.seek(0)
                data = tmpdata
            if not data:
                return 0
            tmp_pdfin = tempfile.mkstemp(suffix='.pdf')
            tmp_pdfout = tempfile.mkstemp(suffix='.pdf')
            tmp_gifin = tempfile.mkstemp(suffix='.gif')
            fhout = open(tmp_pdfout[1], "w")
            fhimg = open(tmp_gifin[1], "r")
            fhout.write(data)
            fhout.seek(0)
            cmd = "pdftk %s cat 1 output %s" %(tmp_pdfout[1], tmp_pdfin[1])
            logger.info(cmd)
            res = os.popen(cmd)
            result = res.read()
            if result:
                logger.warn("popen-1: %s" % (result))
            cmd = "convert %s -resize %sx%s %s" %(tmp_pdfin[1], width, height,
                                                  tmp_gifin[1])
            res = os.popen(cmd)
            result = res.read()
            if result:
                logger.warn("popen-2: %s" % (result))
            #fhimg.seek(0)
            coverdata = fhimg.read()
            self.context.getField('cover_image').getMutator(self.context)(coverdata)
            status = 1
        except Exception, e:
            logger.warn("generateImage: Could not autoconvert because: %s" %e)
            status = 0

        # try to clean up
        if tmp_pdfin is not None:
            try: os.remove(tmp_pdfin[1])
            except: pass
        if tmp_pdfout is not None:
            try: os.remove(tmp_pdfout[1])
            except: pass
        if tmp_gifin is not None:
            try: os.remove(tmp_gifin[1])
            except: pass

        return status
