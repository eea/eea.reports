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
                required=True,
                validators=('newFileUpload',),
                languageIndependent=False,
                widget=atapi.FileWidget(
                    label = _(u'label_report_file', default=u'Report File'),
                    description=_(u'description_report_file', default=u'Fill in the publication file'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportStringField('isbn',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label = _(u'label_isbn', default=u'ISBN'),
                    description=_(u'description_isbn', default=u'Fill in the ISBN Number of this publication.'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportIntegerField('eeaid',
                schemata='report',
                lanaguageIndependent=False,
                default=0,
                widget=atapi.IntegerWidget(
                    label=_(u'label_eeaid', default=u'EEA Publication Internal ID'),
                    description=_(u'description_eeaid', default=u'Fill in EEA publication internal id'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportStringField('order_id',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label = _(u'label_order_id', default=u'ORDER ID (Catalogue Number)'),
                    description=_(u'description_order_id', default=u'Fill in the Order ID of this publication.'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportBooleanField('for_sale',
                schemata='report',
                languageIndependent=False,
                default=False,
                widget=atapi.BooleanWidget(
                    label = _(u'label_for_sale', default=u'For sale?'),
                    description=_(u'description_for_sale', default=u'Is this publication for sale?'),
                    i18n_domain='eea.reports',
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
                    i18n_domain='eea.reports',
                ),
            ),
            ReportLinesField('creators',
                schemata='report',
                languageIndependent=False,
                multiValued=1,
                default=(u'EEA (European Environment Agency)',),
                vocabulary=NamedVocabulary("report_creators"),
                widget=atapi.KeywordWidget(
                    label=_(u'label_creators', default=u'Creators/Authors'),
                    description=_(u'description_creators', default=u'Fill in additional creators/authors'),
                    macro='report_keywords',
                    i18n_domain='eea.reports',
                ),
            ),
            ReportLinesField('publishers',
                schemata='report',
                languageIndependent=False,
                multiValued=1,
                default=(u'EEA (European Environment Agency)',),
                vocabulary=NamedVocabulary("report_publishers"),
                widget=atapi.KeywordWidget(
                    label=_(u'label_publishers', default=u'Publishers'),
                    description=_(u'description_publishers', default=u'Fill in additional publishers'),
                    macro='report_keywords',
                    i18n_domain='eea.reports',
                ),
            ),
            ReportLinesField('themes',
                schemata='report',
                vocabulary=ReportThemesVocabulary(),
                widget=atapi.InAndOutWidget(
                    label=_(u'EEAContentTypes_label_themes', default=u'Themes'),
                    description=_(u'EEAContentTypes_help_themes', default=u'Choose publication themes'),
                    i18n_domain='EEAContentTypes',
                ),
                languageIndependent=True,
                index="KeywordIndex:brains",
                enforceVocabulary=1
            ),
            ReportLinesField('publication_groups',
                schemata='report',
                vocabulary=NamedVocabulary("publications_groups"),
                languageIndependent=True,
                widget=atapi.InAndOutWidget(
                    label=_(u'label_publication_groups', default=u'Publication groups'),
                    description=_(u'description_publication_groups', default=u'Fill in publication groups'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportFloatField('price',
                schemata='report',
                languageIndependent=False,
                default=0,
                widget=atapi.DecimalWidget(
                    label=_(u'label_price', default=u'Price'),
                    description=_(u'description_price', default=u'Fill in publication price'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportTextField('order_override_text',
                schemata='report',
                languageIndependent=False,
                allowable_content_types=('text/html',),
                default_content_type='text/html',
                default_output_type='text/html',
                widget=atapi.RichWidget(
                    label=_(u'label_order_override_text', default=u'Override the order text with your own text'),
                    description=_(u'description_order_override_text', default=u'Fill in to override the order text'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportTextField('order_extra_text',
                schemata='report',
                languageIndependent=False,
                allowable_content_types=('text/html',),
                default_content_type='text/html',
                default_output_type='text/html',
                widget=atapi.RichWidget(
                    label=_(u'label_order_extra_text', default=u'OR add some text to the order screen'),
                    description=_(u'description_order_extra_text', default=u'Fill in to add this text to the order text'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportIntegerField('pages',
                schemata='report',
                lanaguageIndependent=False,
                default=0,
                widget=atapi.IntegerWidget(
                    label=_(u'label_pages', default=u'Pages'),
                    description=_(u'description_pages', default=u'Fill in pages'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportStringField('copyrights',
                schemata='report',
                languageIndependent=False,
                default=COPYRIGHTS,
                widget=atapi.StringWidget(
                    label=_(u'label_copyrights', default=u'Copyrights'),
                    description=_(u'description_copyrights', default=u'Fill in copyrights'),
                    i18n_domain='eea.reports',
                ),
            ),
            ReportTextField('trailer',
                schemata='report',
                languageIndependent=False,
                allowable_content_types=('text/html',),
                default_content_type='text/html',
                default_output_type='text/html',
                widget=atapi.RichWidget(
                    label = _(u'label_trailer', default=u'Trailer'),
                    description=_(u'description_trailer', default=u'Fill in the trailer.'),
                    i18n_domain='eea.reports',
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
            'publication_groups',
            'copyrights',
            'for_sale',
            'order_id',
            'eeaid',
            'price',
            'pages',
            'trailer',
            'order_override_text',
            'order_extra_text',
        ]
        new_order.extend([x for x in order if x not in new_order])
        original['report'] = new_order

        return original
