""" Subtyping
"""
from Products.CMFPlone import PloneMessageFactory as _
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes import atapi
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField
from slc.publications.subtypes.publication import SchemaExtender as PublicationSchemaExtender
from slc.publications.subtypes.publication import ExtensionFieldMixin
from eea.reports.config import COPYRIGHTS
from eea.reports.vocabulary import ReportYearsVocabulary, ReportThemesVocabulary
from eea.reports.field import SerialTitleField
from eea.reports.widget import SerialTitleWidget

class ReportStringField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class ReportIntegerField(ExtensionField, ExtensionFieldMixin, atapi.IntegerField):
    """ """

class ReportLinesField(ExtensionField, ExtensionFieldMixin, atapi.LinesField):
    """ """

class ReportFloatField(ExtensionField, ExtensionFieldMixin, atapi.FloatField):
    """ """

class ReportTextField(ExtensionField, ExtensionFieldMixin, atapi.TextField):
    """ """

class ReportSerialTitleField(ExtensionField, ExtensionFieldMixin, SerialTitleField):
    """ """

class SchemaExtender(PublicationSchemaExtender):
    """ Schema extender
    """
    implements(IOrderableSchemaExtender)
    _fields = PublicationSchemaExtender._fields + [
        ReportSerialTitleField('serial_title',
            schemata='report',
            languageIndependent=False,
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
                validators=('maxValues',),
                vocabulary=ReportThemesVocabulary(),
                widget=atapi.InAndOutWidget(
                    maxValues=3,
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
                languageIndependent=False,
                widget=atapi.DecimalWidget(
                    label=_(u'label_price', default=u'Price'),
                    description=_(u'description_price', default=u'Fill in price'),
                ),
            ),
            ReportTextField('order_override_text',
                schemata='report',
                languageIndependent=True,
                widget=atapi.RichWidget(
                    label=_(u'label_order_override_text', default=u'Override the order text with your own text'),
                    description=_(u'description_order_override_text', default=u'Fill in to override the order text'),
                ),
            ),
            ReportTextField('order_extra_text',
                schemata='report',
                languageIndependent=True,
                widget=atapi.RichWidget(
                    label=_(u'label_order_extra_text', default=u'OR add some text to the order screen'),
                    description=_(u'description_order_extra_text', default=u'Fill in to add this text to the order text'),
                ),
            ),
            ReportIntegerField('pages',
                schemata='report',
                lanaguageIndependent=False,
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
                languageIndependent=True,
                widget=atapi.RichWidget(
                    label = _(u'label_trailer', default=u'Trailer'),
                    description=_(u'description_trailer', default=u'Fill in the trailer.'),
                )
            ),
    ]
    
    def getOrder(self, original):
        order = original.get('report', [])
        new_order = [
            'serial_title',
            'creators',
            'publishers',
            'themes',
            'price',
            'pages',
            'copyrights',
            'trailer',
            'order_override_text',
            'order_extra_text',
        ]
        new_order.extend([x for x in order if x not in new_order])
        original['report'] = new_order
        
        return original
