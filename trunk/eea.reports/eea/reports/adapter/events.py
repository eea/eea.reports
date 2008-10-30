""" Events
"""
from eea.reports import interfaces
from eea.reports.pdf.interfaces import IReportPDFParser, IPDFCoverImage
from zope.component import getUtility
from p4a.subtyper.interfaces import ISubtyper
from eea.reports.config import REPORT_SUBOBJECTS
#
# Debug
#
def printEvent(obj, evt):
    print "================"
    print [obj], [evt]
#
# Restrict report sub-objects
#
def subtype_added(evt):
    """ EVENT

    Called when a Folder is subtyped as report.
    """
    _restrict_subobjects(evt, 1)

def subtype_removed(evt):
    """ EVENT

    Called when a Folder is un-subtyped as report.
    """
    _restrict_subobjects(evt, -1)

def _restrict_subobjects(evt, rtype=-1):
    """ Restrict report subobjects
    """
    obj = evt.object
    subtype = evt.subtype
    # Nothing to do
    if not subtype:
        return
    # Only possible report
    if not interfaces.IPossibleReportContainer.providedBy(obj):
        return
    # Only report subtype
    if subtype.type_interface is not interfaces.IReportContainerEnhanced:
        return
    # Restrict
    obj.setConstrainTypesMode(rtype)
    if rtype != 1:
        return
    obj.setImmediatelyAddableTypes(REPORT_SUBOBJECTS)
    obj.setLocallyAllowedTypes(REPORT_SUBOBJECTS)
#
# Generate cover image
#
def add_image_file(obj, image):
    """ Util method used to add an image to given object.

    @param obj: a portal object
    @param image: image data
    """
    if not image:
        return
    if 'cover' not in obj.objectIds():
        obj.invokeFactory('Image', id='cover', title='Cover Image')
    cover = obj._getOb('cover')
    cover.getField('image').getMutator(cover)(image)

def generate_image(obj, evt):
    """ EVENT
        called on objectmodified. Tries to generate the cover image.
    """
    generator = getUtility(IPDFCoverImage)
    image = generator.generate(evt.data)
    if not image:
        return
    add_image_file(obj, image)
#
# Parse pdf metadata
#
def parse_metadata(obj, evt):
    """ EVENT
        called on new file upload. Tries to import pdf metadata.
    """
    pdfparser = getUtility(IReportPDFParser)
    metadata = pdfparser.parse(evt.data.read())
    if not metadata:
        return
    for key, value in metadata.items():
        field = obj.getField(key)
        if not field:
            continue
        field.getMutator(obj)(value)
#
# Report initialize
#
def report_initialized(obj, evt):
    """ EVENT
        called when a Report content-type were added. COnvert it to folder
        and subtype as report.
    """
    subtyper = getUtility(ISubtyper)
    canonical = obj.getCanonical()

    # Object added
    if obj == canonical and evt.portal_type == 'Report':
        obj.portal_type = 'Folder'
        return subtyper.change_type(obj, 'eea.reports.FolderReport')

    # Object translated
    if subtyper.existing_type(canonical).name == 'eea.reports.FolderReport':
        obj.portal_type = 'Folder'
        return subtyper.change_type(obj, 'eea.reports.FolderReport')
