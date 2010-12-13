""" Events
"""
from eea.reports import interfaces
from eea.reports.pdf.interfaces import IReportPDFParser, IPDFCoverImage
from zope.component import getUtility
from Products.CMFCore.utils import getToolByName
from p4a.subtyper.interfaces import ISubtyper
from eea.reports.config import REPORT_SUBOBJECTS
from eea.reports.vocabulary import ReportThemesVocabulary
#
# Restrict report sub-objects
#
def subtype_added(evt):
    """ EVENT

    Called when an object is subtyped as report.
    """
    _restrict_subobjects(evt, 1)

def subtype_removed(evt):
    """ EVENT

    Called when an object is un-subtyped as report.
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
def add_image_file(obj, image, image_id='cover', image_title='Cover Image'):
    """ Util method used to add an image to given object.

    @param obj: a portal object
    @param image: image data
    """
    if not image:
        return
    if image_id not in obj.objectIds():
        image_id = obj.invokeFactory('Image', id=image_id, title=image_title)
    img_obj = obj._getOb(image_id)
    img_obj.getField('image').getMutator(img_obj)(image)

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
def _get_themes_from_keywords(instance, keywords):
    """ Match keywords with themes vocabulary
    """
    if not keywords:
        return []
    vocab = ReportThemesVocabulary()
    all_themes = vocab.getDisplayList(instance)
    keywords = set([x.lower() for x in keywords])
    res = set([key for key, value in all_themes if value.lower() in keywords])
    return tuple(res)

def parse_metadata(obj, evt):
    """ EVENT
        called on new file upload. Tries to import pdf metadata.
    """
    update_main = evt.update_main
    if not update_main:
        return

    pdfparser = getUtility(IReportPDFParser)
    metadata = pdfparser.parse(evt.data.read())
    if not metadata:
        return

    # Do not modify effective date
    metadata['effectiveDate'] = obj.getEffectiveDate()

    # Get themes from keywords
    keywords = metadata.get('subject', ())
    themes = _get_themes_from_keywords(obj, keywords)
    if themes:
        metadata['themes'] = themes

    for key, value in metadata.items():
        field = obj.getField(key)
        if not field:
            continue
        if not value:
            continue
        field.getMutator(obj)(value)
#
# Invalidate squid cache
#
def invalidate_cache(instance, evt):
    """ EVENT
        called on new file upload. Tries to invalidate squid cache
    """
    stool = getToolByName(instance, 'portal_squid', None)
    if not stool:
        return
    key = instance.absolute_url(1) + '/at_download/file'
    res = stool.pruneUrls([
        key,
        'http/localhost/81/%s' % key
    ])
#
# Report initialize
#
def report_initialized(obj, evt):
    """ EVENT
        called when a Report content-type is added. Subtype it as report.
    """
    subtyper = getUtility(ISubtyper)
    canonical = obj.getCanonical()

    # Object added
    if obj == canonical and evt.portal_type == 'Report':
        obj.setExcludeFromNav(True)
        # Fix language
        parent_lang = obj.getParentNode().getLanguage()
        if obj.getLanguage() != parent_lang:
            obj.setLanguage(parent_lang)
        return subtyper.change_type(obj, 'eea.reports.FolderReport')

    # Object translated
    subtype = subtyper.existing_type(canonical)
    subtype_name = getattr(subtype, 'name', None)
    if subtype_name == 'eea.reports.FolderReport':
        obj.setExcludeFromNav(True)
        return subtyper.change_type(obj, 'eea.reports.FolderReport')
#
# Set the language independent
#
def setLanguageIndependent(obj, evt):
    """ Set the language independent values on translations.
    """
    subtyper = getUtility(ISubtyper)
    canonical = obj.getCanonical()
    if obj == canonical:
        # Default
        independent_fields = {}
        obj_schemata = canonical.Schemata()
        ctool = getToolByName(canonical, 'portal_catalog')

        # Get language independent fields
        for schema_id in obj_schemata.keys():
            [independent_fields.setdefault(field.getName(), None) for field in obj_schemata[schema_id].filterFields(languageIndependent=True)]
        for field_id in independent_fields.keys():
            independent_fields[field_id] = canonical.getField(field_id).get(canonical)

        # Set (if case) values for langauge independent fields
        for trans in canonical.getTranslations():
            detect_diff = False
            ob_trans = canonical.getTranslation(trans)
            for field_id in independent_fields.keys():
                new_value = independent_fields[field_id]
                old_value = ob_trans.getField(field_id).get(ob_trans)
                if new_value != old_value:
                    detect_diff = True
                    ob_trans.getField(field_id).getMutator(ob_trans)(new_value)
            if detect_diff: ctool.reindexObject(ob_trans)
