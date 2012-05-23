""" Events
"""
from zope.interface import alsoProvides
from zope.component import getUtility, queryUtility
from zope.schema.interfaces import IVocabularyFactory
from Products.CMFCore.utils import getToolByName
from eea.reports.pdf.interfaces import IReportPDFParser, IPDFCoverImage
from eea.reports.interfaces import IReportContainerEnhanced
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
    img_obj.setExcludeFromNav(True)
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

    vocab = queryUtility(IVocabularyFactory, name=u'Allowed themes for edit')

    # eea.themecentre is not installed
    if not vocab:
        return []

    keywords = set([x.lower() for x in keywords])
    res = set([term.value for term in vocab(instance)
                if term.title.lower() in keywords])
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
# Report initialize
#
def report_initialized(obj, evt):
    """ EVENT
        called when a Report content-type is added. Subtype it as Report.
    """
    if not IReportContainerEnhanced.providedBy(obj):
        if getattr(obj, 'portal_type', '') == 'Report':
            alsoProvides(obj, IReportContainerEnhanced)
        # Portal type not changed yet, check name
        elif getattr(evt, 'newName', '').startswith('report'):
            alsoProvides(obj, IReportContainerEnhanced)

#
# Restrict subobjects
#
def restrict_subobjects(obj, evt):
    """ EVENT
        called when a Report content-type is added. Setup its subobjects type
        restrictions to "Allow the standard types to be added"
    """
    try:
        obj.setConstrainTypesMode(0)
    except AttributeError:
        pass

#
# Set the language independent
#
def setLanguageIndependent(obj, evt):
    """ Set the language independent values on translations.
    """
    canonical = obj.getCanonical()
    if obj == canonical:
        # Default
        independent_fields = {}
        obj_schemata = canonical.Schemata()
        ctool = getToolByName(canonical, 'portal_catalog')

        # Get language independent fields
        for schema_id in obj_schemata.keys():
            for field in obj_schemata[schema_id].filterFields(
                languageIndependent=True):
                independent_fields.setdefault(field.getName(), None)

        for field_id in independent_fields.keys():
            independent_fields[field_id] = canonical.getField(
                field_id).get(canonical)

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
            if detect_diff:
                ctool.reindexObject(ob_trans)
