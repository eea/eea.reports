""" Subtyping
"""
from Products.CMFPlone import PloneMessageFactory as _
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes import atapi
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField
from eea.reports.config import COPYRIGHTS
from eea.reports.vocabulary import ReportYearsVocabulary, ReportThemesVocabulary
from eea.reports.subtypes.field import SerialTitleField
from eea.reports.subtypes.widget import SerialTitleWidget

class ExtensionFieldMixin:
    def translationMutator(self, instance):
        return self.getMutator(instance)

class ReportStringField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class ReportIntegerField(ExtensionField, ExtensionFieldMixin, atapi.IntegerField):
    """ """

class ReportBooleanField(ExtensionField, ExtensionFieldMixin, atapi.BooleanField):
    """ """

class ReportLinesField(ExtensionField, ExtensionFieldMixin, atapi.LinesField):
    """ """

class ReportFloatField(ExtensionField, ExtensionFieldMixin, atapi.FloatField):
    """ """

class ReportFileField(ExtensionField, ExtensionFieldMixin, atapi.FileField):
    """ """

class ReportImageField(ExtensionField, ExtensionFieldMixin, atapi.ImageField):
    """ """

class ReportTextField(ExtensionField, ExtensionFieldMixin, atapi.TextField):
    """ """

class ReportSerialTitleField(ExtensionField, ExtensionFieldMixin, SerialTitleField):
    """ """

class SchemaExtender(object):
    """ Schema extender
    """
    implements(IOrderableSchemaExtender)
    _fields = [
            ReportFileField('file',
                schemata='default',
                languageIndependent=False,
                widget=atapi.FileWidget(
                    label = _(u'label_report_file', default=u'Report File'),
                    description=_(u'description_report_file', default=u'Fill in the Report file'),
                ),
            ),
            ReportImageField('cover_image',
                schemata='report',
                languageIndependent=False,
                widget=atapi.ImageWidget(
                    label = _(u'label_cover_image', default=u'Cover Image'),
                    description=_(u'description_cover_image', default=u'Upload a cover image. Leave empty to have the system autogenerate one for you.'),
                ),
            ),
            ReportStringField('isbn',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label = _(u'label_isbn', default=u'ISBN'),
                    description=_(u'description_isbn', default=u'Fill in the ISBN Number of this Report.'),
                ),
            ),
            ReportStringField('order_id',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label = _(u'label_order_id', default=u'Order ID'),
                    description=_(u'description_order_id', default=u'Fill in the Order ID of this Report.'),
                ),
            ),
            ReportBooleanField('for_sale',
                schemata='report',
                languageIndependent=True,
                widget=atapi.BooleanWidget(
                    label = _(u'label_for_sale', default=u'For sale?'),
                    description=_(u'description_for_sale', default=u'Is this Report for sale?'),
                ),
            ),
            ReportFileField('metadata_upload',
                schemata='report',
                languageIndependent=True,
                widget=atapi.FileWidget(
                    label = _(u'label_metadata_upload', default=u'Metadata INI upload'),
                    description=_(u'description_metadata_upload', default=u'Upload Metadata in INI style format.'),
                ),
            ),
            ReportSerialTitleField('serial_title',
                schemata='report',
                languageIndependent=True,
                types_vocabulary=NamedVocabulary("report_types"),
                years_vocabulary=ReportYearsVocabulary(),
                default=(u'', 0, -1, u''),
                widget=SerialTitleWidget(
                    label=_(u'label_serial_title', default=u'Serial title'),
                    description=_(u'description_serial_title', default=u'Fill in serial title'),
                ),
            ),
            ReportLinesField('creators',
                schemata='report',
                languageIndependent=True,
                multiValued=1,
                default=(u'EEA (European Environment Agency)',),
                vocabulary=NamedVocabulary("report_creators"),
                widget=atapi.KeywordWidget(
                    label=_(u'label_creators', default=u'Creators/Authors'),
                    description=_(u'description_creators', default=u'Fill in additional creators/authors'),
                    macro='report_keywords',
                ),
            ),
            ReportLinesField('publishers',
                schemata='report',
                languageIndependent=True,
                multiValued=1,
                default=(u'EEA (European Environment Agency)',),
                vocabulary=NamedVocabulary("report_publishers"),
                widget=atapi.KeywordWidget(
                    label=_(u'label_publishers', default=u'Publishers'),
                    description=_(u'description_publishers', default=u'Fill in additional publishers'),
                    macro='report_keywords',
                ),
            ),
            ReportLinesField('themes',
                schemata='report',
                vocabulary=ReportThemesVocabulary(),
                widget=atapi.InAndOutWidget(
                    label=_(u'EEAContentTypes_label_themes', default=u'Themes'),
                    description=_(u'EEAContentTypes_help_themes', default=u'Choose max 3 themes go with this Highlight.'),
                    i18n_domain='EEAContentTypes',
                ),
                languageIndependent=True,
                index="KeywordIndex:brains",
                enforceVocabulary=1
            ),
            ReportFloatField('price',
                schemata='report',
                languageIndependent=True,
                widget=atapi.DecimalWidget(
                    label=_(u'label_price', default=u'Price'),
                    description=_(u'description_price', default=u'Fill in price'),
                ),
            ),
            ReportTextField('order_override_text',
                schemata='report',
                languageIndependent=False,
                widget=atapi.RichWidget(
                    label=_(u'label_order_override_text', default=u'Override the order text with your own text'),
                    description=_(u'description_order_override_text', default=u'Fill in to override the order text'),
                ),
            ),
            ReportTextField('order_extra_text',
                schemata='report',
                languageIndependent=False,
                widget=atapi.RichWidget(
                    label=_(u'label_order_extra_text', default=u'OR add some text to the order screen'),
                    description=_(u'description_order_extra_text', default=u'Fill in to add this text to the order text'),
                ),
            ),
            ReportIntegerField('pages',
                schemata='report',
                lanaguageIndependent=True,
                widget=atapi.IntegerWidget(
                    label=_(u'label_pages', default=u'Pages'),
                    description=_(u'description_pages', default=u'Fill in pages'),
                ),
            ),
            ReportStringField('copyrights',
                schemata='report',
                languageIndependent=False,
                default=COPYRIGHTS,
                widget=atapi.StringWidget(
                    label=_(u'label_copyrights', default=u'Copyrights'),
                    description=_(u'description_copyrights', default=u'Fill in copyrights'),
                ),
            ),
            ReportTextField('trailer',
                schemata='report',
                languageIndependent=False,
                widget=atapi.RichWidget(
                    label = _(u'label_trailer', default=u'Trailer'),
                    description=_(u'description_trailer', default=u'Fill in the trailer.'),
                )
            ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self._fields

    def getOrder(self, original):
        order = original.get('report', [])
        new_order = [
            'serial_title',
            'isbn',
            'creators',
            'publishers',
            'themes',
            'copyrights',
            'metadata_upload',
            'for_sale',
            'order_id',
            'price',
            'pages',
            'trailer',
            'order_override_text',
            'order_extra_text',
        ]
        new_order.extend([x for x in order if x not in new_order])
        original['report'] = new_order

        return original
