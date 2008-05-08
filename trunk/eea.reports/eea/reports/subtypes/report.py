""" Subtyping
"""
from Products.CMFPlone import PloneMessageFactory as _
from Products.Archetypes import atapi 
from zope.interface import implements
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from archetypes.schemaextender.field import ExtensionField
from slc.publications.subtypes.publication import SchemaExtender as PublicationSchemaExtender
from slc.publications.subtypes.publication import ExtensionFieldMixin
from eea.reports.config import COPYRIGHTS

class ReportTypeFiled(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class ReportNumField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class SeriesYearField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class SeriesTitleField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class TrailerField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class CreatorsOrgsField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class CreatorsField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class PublishersOrgsField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class PublishersField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class ThemesField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class PriceField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class OrderOverrideTextField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class OrderExtraTextField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class CopyrightField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class PagesField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ """

class SchemaExtender(PublicationSchemaExtender):
    """ Schema extender
    """
    implements(IOrderableSchemaExtender)
    _fields = PublicationSchemaExtender._fields + [
            ReportTypeFiled('reporttype',
                schemata='report',
                languageIndependent=False,
                default=u'',
                widget=atapi.SelectionWidget(
                    label=_(u'label_reporttype', default=u'Serial title (Report type)'),
                    description=_(u'description_reporttype', default=u'Fill in report-type'),
                ),
            ),
            ReportNumField('reportnum',
                schemata='report',
                languageIndependent=False,
                default=1,
                widget=atapi.IntegerWidget(
                    label=_(u'label_reportnum', default=u'Serial title (Report number)'),
                    description=_(u'description_reportnum', default=u'Fill in report-number'),
                ),
            ),
            SeriesYearField('series_year',
                schemata='report',
                languageIndependent=False,
                default=u'',
                widget=atapi.SelectionWidget(
                    label=_(u'label_series_year', default=u'Serial title (Report year)'),
                    description=_(u'description_series_year', default=u'Fill in report-year'),
                ),
            ),
            SeriesTitleField('series_title',
                schemata='report',
                languageIndependent=True,
                widget=atapi.StringWidget(
                    label=_(u'label_series_title', default=u'Serial title (Alternative)'),
                    description=_(u'description_reporttype', default=u'Fill in report-type'),
                ),
            ),
            CreatorsOrgsField('creators_orgs',
                schemata='report',
                languageIndependent=False,
                widget=atapi.MultiSelectionWidget(
                    label=_(u'label_creators_orgs', default=u'Authors (organisations)'),
                    description=_(u'description_creators_orgs', default=u'Fill in authors(organisations)'),
                ),
            ),
            CreatorsField('creators',
                schemata='report',
                languageIndependent=True,
                widget=atapi.LinesWidget(
                    label=_(u'label_creators', default=u'Additional Creators/Authors'),
                    description=_(u'description_creators', default=u'Fill in additional creators/authors'),
                ),
            ),
            PublishersOrgsField('publishers_orgs',
                schemata='report',
                languageIndependent=False,
                widget=atapi.MultiSelectionWidget(
                    label=_(u'label_publishers_orgs', default=u'Publishers'),
                    description=_(u'description_publishers_orgs', default=u'Fill in publishers'),
                ),
            ),
            PublishersField('publishers',
                schemata='report',
                languageIndependent=True,
                widget=atapi.LinesWidget(
                    label=_(u'label_publishers', default=u'Additional Publishers'),
                    description=_(u'description_publishers', default=u'Fill in additional publishers'),
                ),
            ),
            ThemesField('themes',
                schemata='report',
                languageIndependent=False,
                widget=atapi.MultiSelectionWidget(
                    label=_(u'label_themes', default=u'Themes'),
                    description=_(u'description_themes', default=u'Fill in themes'),
                ),
            ),
            PriceField('price',
                schemata='report',
                languageIndependent=False,
                widget=atapi.DecimalWidget(
                    label=_(u'label_price', default=u'Price'),
                    description=_(u'description_price', default=u'Fill in price'),
                ),
            ),
            OrderOverrideTextField('order_override_text',
                schemata='report',
                languageIndependent=True,
                widget=atapi.RichWidget(
                    label=_(u'label_order_override_text', default=u'Override the order text with your own text'),
                    description=_(u'description_order_override_text', default=u'Fill in to override the order text'),
                ),
            ),
            OrderExtraTextField('order_extra_text',
                schemata='report',
                languageIndependent=True,
                widget=atapi.RichWidget(
                    label=_(u'label_order_extra_text', default=u'OR add some text to the order screen'),
                    description=_(u'description_order_extra_text', default=u'Fill in to add this text to the order text'),
                ),
            ),
            PagesField('pages',
                schemata='report',
                lanaguageIndependent=False,
                widget=atapi.IntegerWidget(
                    label=_(u'label_pages', default=u'Pages'),
                    description=_(u'description_pages', default=u'Fill in pages'),
                ),
            ),
            CopyrightField('coppyrights',
                schemata='report',
                languageIndependent=False,
                default=COPYRIGHTS,
                widget=atapi.StringWidget(
                    label=_(u'label_copyrights', default=u'Copyrights'),
                    description=_(u'description_copyrights', default=u'Fill in copyrights'),
                ),
            ),
            TrailerField('trailer',
                schemata='report',
                languageIndependent=True,
                widget=atapi.RichWidget(
                    label = _(u'label_trailer', default=u'Trailer'),
                    description=_(u'description_trailer', default=u'Fill in the trailer.')
                )
            ),
    ]
    
    def getOrder(self, original):
        order = original.get('report', [])
        new_order = [
            'reporttype',
            'reportnum',
            'series_year',
            'series_title',
            'creators_orgs',
            'creators',
            'publishers_orgs',
            'publishers',
            'themes',
            'price',
            'pages',
            'coppyrights',
            'trailer',
            'order_override_text',
            'order_extra_text',
        ]
        new_order.extend([x for x in order if x not in new_order])
        original['report'] = new_order
        
        return original
