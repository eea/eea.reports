""" Subtyping
"""
from Products.AddRemoveWidget import AddRemoveWidget
from Products.CMFPlone import PloneMessageFactory as _
from Products.Archetypes import atapi

from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender

from eea.forms.widgets.ManagementPlanWidget import ManagementPlanWidget

from eea.reports.subtypes import field
from eea.reports.subtypes import widget
from eea.reports.config import COPYRIGHTS
from eea.reports.subtypes.widget import SerialTitleWidget

from datetime import datetime

from zope.interface import implements

class SchemaExtender(object):
    """ Schema extender
    """
    implements(IOrderableSchemaExtender)
    _fields = [
            field.ReportTextField('description',
                schemata='default',
                default='',
                searchable=1,
                accessor="Description",
                required=True,
                widget=atapi.TextAreaWidget(
                    label='Description',
                    description="A short summary of the content",
                    label_msgid="label_description",
                    description_msgid="help_description",
                    i18n_domain="plone"
                    ),
                ),
            field.ReportFileField('file',
                schemata='default',
                languageIndependent=False,
                required=True,
                widget=widget.ReportFileWidget(
                    label=_(u'label_report_file',
                            default=u'Publication file'),
                    description=_(u'description_report_file',
                                  default=u'Fill in the publication file'),
                    helper_js=('widgets/update_metadata.js',),
                    macro='widgets/report_file',
                    i18n_domain='eea',
                    ),
                ),
            field.ReportStringField('isbn',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label=_(u'label_isbn', default=u'ISBN'),
                    description=_(u'description_isbn',
                       default=u'Fill in the ISBN Number of this publication.'),
                    i18n_domain='eea',
                    ),
                ),
            field.ReportIntegerField('eeaid',
                schemata='report',
                lanaguageIndependent=False,
                default=0,
                widget=atapi.IntegerWidget(
                    visible= -1,
                    label=_(u'label_eeaid',
                            default=u'EEA Publication Internal ID'),
                    description=_(u'description_eeaid',
                                default=u'Fill in EEA publication internal id'),
                    i18n_domain='eea',
                    ),
                ),
            field.ReportStringField('order_id',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label=_(u'label_order_id',
                            default=u'ORDER ID (Catalogue Number)'),
                    description=_(u'description_order_id',
                          default=u'Fill in the Order ID of this publication.'),
                    i18n_domain='eea',
                    ),
                ),
            field.ReportBooleanField('for_sale',
                    schemata='report',
                    languageIndependent=True,
                    default=False,
                    widget=atapi.BooleanWidget(
                        label=_(u'label_for_sale', default=u'For sale?'),
                        description=_(u'description_for_sale',
                                      default=u'Is this publication for sale?'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportSerialTitleField('serial_title',
                    schemata='report',
                    required=True,
                    languageIndependent=True,
                    validators=('serialTitle',),
                    types_vocabulary=u"eea.reports.vocabulary.ReportTypes",
                    years_vocabulary=u"eea.reports.vocabulary.ReportYears",
                    default=(u'', 0, -1, u''),
                    widget=SerialTitleWidget(
                        label=_(u'label_serial_title', default=u'Serial title'),
                        description=_(u'description_serial_title',
                                      default=u'Fill in serial title'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportLinesField('creators',
                    schemata='report',
                    required=True,
                    languageIndependent=False,
                    multiValued=1,
                    default=(u'EEA (European Environment Agency)',),
                    vocabulary_factory="eea.reports.vocabulary.ReportCreators",
                    widget=AddRemoveWidget(
                        label=_(u'label_creators', default=u'Creators/Authors'),
                        description=_(u'description_creators',
                                default=u'Fill in additional creators/authors'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportLinesField('publishers',
                schemata='report',
                required=True,
                languageIndependent=False,
                multiValued=1,
                default=(u'EEA (European Environment Agency)',),
                vocabulary_factory="eea.reports.vocabulary.ReportPublishers",
                widget=AddRemoveWidget(
                    label=_(u'label_publishers', default=u'Publishers'),
                    description=_(u'description_publishers',
                                  default=u'Fill in additional publishers'),
                    i18n_domain='eea',
                    ),
                ),
            field.ReportLinesField('publication_groups',
                schemata='categorization',
                vocabulary_factory="eea.reports.vocabulary.PublicationGroups",
                languageIndependent=True,
                index="KeywordIndex:brains",
                widget=atapi.InAndOutWidget(
                    label=_(u'label_publication_groups',
                            default=u'Publication groups'),
                    description=_(u'description_publication_groups',
                                  default=u'Fill in publication groups'),
                    i18n_domain='eea',
                    ),
                ),
            field.ReportOrderableReferenceField('relatedItems',
                    schemata='categorization',
                    languageIndependent=True,
                    index='KeywordIndex',
                    relationship='relatesTo',
                    multiValued=True,
                    isMetadata=True,
                    widget=ReferenceBrowserWidget(
                        allow_search=True,
                        allow_browse=True,
                        allow_sorting=True,
                        show_indexes=False,
                        force_close_on_insert=True,
                        label=_(u'label_related_items',
                                default=u'Related Item(s)'),
                        description=_(u'help_related_items', default=u''),
                        i18n_domain="plone",
                        ),
                    ),
            field.ReportFloatField('price',
                    schemata='report',
                    languageIndependent=True,
                    default=0,
                    widget=atapi.DecimalWidget(
                        label=_(u'label_price', default=u'Price (Euro)'),
                        description=_(u'description_price',
                                      default=u'Fill in publication price'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportTextField('order_override_text',
                    schemata='report',
                    languageIndependent=False,
                    allowable_content_types=('text/html',),
                    default_content_type='text/html',
                    default_output_type='text/html',
                    widget=atapi.RichWidget(
                        label=_(u'label_order_override_text',
                         default=u'Override the order text with your own text'),
                        description=_(u'description_order_override_text',
                                 default=u'Fill in to override the order text'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportTextField('order_extra_text',
                    schemata='report',
                    languageIndependent=False,
                    allowable_content_types=('text/html',),
                    default_content_type='text/html',
                    default_output_type='text/html',
                    widget=atapi.RichWidget(
                        label=_(u'label_order_extra_text',
                               default=u'OR add some text to the order screen'),
                        description=_(u'description_order_extra_text',
                         default=u'Fill in to add this text to the order text'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportIntegerField('pages',
                    schemata='report',
                    lanaguageIndependent=False,
                    default=0,
                    widget=atapi.IntegerWidget(
                        label=_(u'label_pages', default=u'Pages'),
                        description=_(u'description_pages',
                                      default=u'Fill in total number of pages'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportManagementPlanField(
                    name='management_plan',
                    schemata='report',
                    languageIndependent=True,
                    required_for_published=True,
                    required=True,
                    default=(datetime.now().year, ''),
                    validators=('management_plan_code_validator',),
                    vocabulary_factory=u"Temporal coverage",
                    widget=ManagementPlanWidget(
                        format="select",
                        label="EEA Management Plan",
                        description=(
                            "EEA Management plan code. Internal EEA project "
                            "line code, used to assign an EEA product output to"
                            " a specific EEA project number in the "
                            "management plan."),
                        label_msgid='dataservice_label_eea_mp',
                        description_msgid='dataservice_help_eea_mp',
                        i18n_domain='eea',
                        )
                    ),
            field.ReportStringField('copyrights',
                    schemata='report',
                    languageIndependent=True,
                    default=COPYRIGHTS,
                    widget=atapi.StringWidget(
                        label=_(u'label_copyrights', default=u'Copyrights'),
                        description=_(u'description_copyrights',
                                      default=u'Fill in copyrights'),
                        i18n_domain='eea',
                        ),
                    ),
            field.ReportTextField('trailer',
                    schemata='report',
                    languageIndependent=False,
                    allowable_content_types=('text/html',),
                    default_content_type='text/html',
                    default_output_type='text/html',
                    widget=atapi.RichWidget(
                        label=_(u'label_trailer', default=u'Trailer'),
                        description=_(u'description_trailer',
                                      default=u'Fill in the trailer.'),
                        i18n_domain='eea',
                        )
                    ),
            field.ReportBooleanField('excludeFromNav',
                    required = False,
                    languageIndependent = True,
                    schemata = 'settings',
                    default=True,
                    widget = atapi.BooleanWidget(
                        description=_(u'help_exclude_from_nav',
                                      default=(
                                          u'If selected, this item will '
                                          'not appear in the navigation tree')),
                        label = _(u'label_exclude_from_nav',
                                  default=u'Exclude from navigation'),
                        visible={'view' : 'hidden',
                                 'edit' : 'visible'},
                        i18n_domain='plone',
                        ),
                ),
            ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns available fields
        """
        return self._fields

    def getOrder(self, schematas):
        """ Returns fields order
        """
        # Report schemata
        order = schematas.get('report', [])
        new_order = [
                'serial_title',
                'isbn',
                'creators',
                'publishers',
                'copyrights',
                'for_sale',
                'order_id',
                'eeaid',
                'price',
                'pages',
#                'management_plan',
                'trailer',
                'order_override_text',
                'order_extra_text',
        ]

        new_order.extend([x for x in order if x not in new_order])
        schematas['report'] = new_order

        # Categorization schemata
        order = schematas.get('categorization', [])
        new_order = [
            'publication_groups',
            'relatedItems',
        ]
        order = [y for y in order if y not in new_order]
        order.extend(new_order)
        schematas['categorization'] = order

        return schematas
