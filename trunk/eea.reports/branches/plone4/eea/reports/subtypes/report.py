""" Subtyping
"""
from plone.app.blob.field import BlobField
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from Products.Archetypes import atapi
from Products.CMFPlone import PloneMessageFactory as _

try:
    from Products.OrderableReferenceField._field import OrderableReferenceField
except ImportError:
    from Products.Archetypes.Field import ReferenceField as OrderableReferenceField

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import IOrderableSchemaExtender
from datetime import datetime

# XXX WTF eea.dataservice dependency?
#from eea.dataservice.fields.ManagementPlanField import ManagementPlanField
#from eea.dataservice.vocabulary import DatasetYears
#from eea.dataservice.widgets.ManagementPlanWidget import ManagementPlanWidget

from eea.reports.config import COPYRIGHTS
from eea.reports.events import FileUploadedEvent
from eea.reports.subtypes.field import SerialTitleField, ThemesField
from eea.reports.subtypes.widget import SerialTitleWidget
from eea.reports.vocabulary import ReportYearsVocabulary, ReportThemesVocabulary
from zope.event import notify
from zope.interface import implements

class ExtensionFieldMixin:
    """ Archetypes SchemaExtender FieldMixin
    """
    def translationMutator(self, instance):
        """ Translation mutator
        """
        return self.getMutator(instance)

class ReportOrderableReferenceField(ExtensionField, ExtensionFieldMixin,
                                    OrderableReferenceField):
    """ Archetypes SchemaExtender aware reference field """

class ReportStringField(ExtensionField, ExtensionFieldMixin, atapi.StringField):
    """ Archetypes SchemaExtender aware string field """

class ReportIntegerField(ExtensionField, ExtensionFieldMixin,
                         atapi.IntegerField):
    """ Archetypes SchemaExtender aware integer field """

class ReportBooleanField(ExtensionField, ExtensionFieldMixin,
                         atapi.BooleanField):
    """ Archetypes SchemaExtender aware boolean field """

class ReportLinesField(ExtensionField, ExtensionFieldMixin, atapi.LinesField):
    """ Archetypes SchemaExtender aware lines field """

class ReportFloatField(ExtensionField, ExtensionFieldMixin, atapi.FloatField):
    """ Archetypes SchemaExtender aware float field """

class ReportTextField(ExtensionField, ExtensionFieldMixin, atapi.TextField):
    """ Archetypes SchemaExtender aware text field """

class ReportSerialTitleField(ExtensionField, ExtensionFieldMixin,
                             SerialTitleField):
    """ Archetypes SchemaExtender aware serial title field """

class ReportThemesField(ExtensionField, ExtensionFieldMixin, ThemesField):
    """ Archetypes SchemaExtender aware themes field """

#class ReportManagementPlanField(ExtensionField, ExtensionFieldMixin,
#                                ManagementPlanField):
#    """ Archetypes SchemaExtender aware management plan field """

class ReportFileField(ExtensionField, ExtensionFieldMixin, BlobField):
    """ Archetypes SchemaExtender aware file field """

    def set(self, instance, value, **kwargs):
        """ Field mutator
        """
        is_value = value and value != "DELETE_FILE"

        # Handle update title and description checkbox
        update_main = kwargs.pop('_update_main_', False)

        # Handle migration
        migration = kwargs.pop('_migration_', False)
        if is_value and not migration:
            notify(FileUploadedEvent(instance, value, update_main))

        BlobField.set(self, instance, value, **kwargs)

class ReportFileWidget(atapi.FileWidget):
    """ Report widget
    """
    def process_form(self, instance, field, form, **kwargs):
        """ Handle form data
        """
        res = atapi.FileWidget.process_form(self, instance,
                                            field, form, **kwargs)
        if not res:
            return res
        value, res = res

        meta = form.get('%s_update_meta_input' % field.getName(), None)
        if meta:
            res['_update_main_'] = True
        return value, res


class SchemaExtender(object):
    """ Schema extender
    """
    implements(IOrderableSchemaExtender)
    _fields = [
            ReportTextField('description',
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
            ReportFileField('file',
                schemata='default',
                languageIndependent=False,
                widget=ReportFileWidget(
                    label=_(u'label_report_file',
                            default=u'Publication file'),
                    description=_(u'description_report_file',
                                  default=u'Fill in the publication file'),
                    helper_js=('widgets/update_metadata.js',),
                    macro='widgets/report_file',
                    i18n_domain='eea.reports',
                    ),
                ),
            ReportStringField('isbn',
                schemata='report',
                required=True,
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label=_(u'label_isbn', default=u'ISBN'),
                    description=_(u'description_isbn',
                       default=u'Fill in the ISBN Number of this publication.'),
                    i18n_domain='eea.reports',
                    ),
                ),
            ReportIntegerField('eeaid',
                schemata='report',
                lanaguageIndependent=False,
                default=0,
                widget=atapi.IntegerWidget(
                    visible= -1,
                    label=_(u'label_eeaid',
                            default=u'EEA Publication Internal ID'),
                    description=_(u'description_eeaid',
                                default=u'Fill in EEA publication internal id'),
                    i18n_domain='eea.reports',
                    ),
                ),
            ReportStringField('order_id',
                schemata='report',
                languageIndependent=False,
                widget=atapi.StringWidget(
                    label=_(u'label_order_id',
                            default=u'ORDER ID (Catalogue Number)'),
                    description=_(u'description_order_id',
                          default=u'Fill in the Order ID of this publication.'),
                    i18n_domain='eea.reports',
                    ),
                ),
            ReportBooleanField('for_sale',
                    schemata='report',
                    languageIndependent=True,
                    default=False,
                    widget=atapi.BooleanWidget(
                        label=_(u'label_for_sale', default=u'For sale?'),
                        description=_(u'description_for_sale',
                                      default=u'Is this publication for sale?'),
                        i18n_domain='eea.reports',
                        ),
                    ),
            ReportSerialTitleField('serial_title',
                    schemata='report',
                    required=True,
                    languageIndependent=True,
                    validators=('serialTitle',),
                    types_vocabulary=NamedVocabulary("report_types"),
                    years_vocabulary=ReportYearsVocabulary(),
                    default=(u'', 0, -1, u''),
                    widget=SerialTitleWidget(
                        label=_(u'label_serial_title', default=u'Serial title'),
                        description=_(u'description_serial_title',
                                      default=u'Fill in serial title'),
                        i18n_domain='eea.reports',
                        ),
                    ),
            ReportLinesField('creators',
                    schemata='report',
                    required=True,
                    languageIndependent=False,
                    multiValued=1,
                    default=(u'EEA (European Environment Agency)',),
                    vocabulary=NamedVocabulary("report_creators"),
                    widget=atapi.KeywordWidget(
                        label=_(u'label_creators', default=u'Creators/Authors'),
                        description=_(u'description_creators',
                                default=u'Fill in additional creators/authors'),
                        macro='report_keywords',
                        i18n_domain='eea.reports',
                        ),
                    ),
            ReportLinesField('publishers',
                    schemata='report',
                    required=True,
                    languageIndependent=False,
                    multiValued=1,
                    default=(u'EEA (European Environment Agency)',),
                    vocabulary=NamedVocabulary("report_publishers"),
                    widget=atapi.KeywordWidget(
                        label=_(u'label_publishers', default=u'Publishers'),
                        description=_(u'description_publishers',
                                      default=u'Fill in additional publishers'),
                        macro='report_keywords',
                        i18n_domain='eea.reports',
                        ),
                    ),
#            ReportThemesField('themes',
#                    schemata='report',
#                    required=True,
#                    validators=('maxValues',),
#                    vocabulary=ReportThemesVocabulary(),
#                    widget=atapi.InAndOutWidget(
#                        maxValues=3,
#                        label=_(u'EEAContentTypes_label_themes',
#                                default=u'Themes'),
#                        description=_(u'EEAContentTypes_help_themes',
#                                      default=u'Choose publication themes'),
#                        i18n_domain='EEAContentTypes',
#                        ),
#                    languageIndependent=True,
#                    index="KeywordIndex:brains",
#                    enforceVocabulary=1
#                    ),
            ReportLinesField('publication_groups',
                    schemata='relations',
                    vocabulary=NamedVocabulary("publications_groups"),
                    languageIndependent=True,
                    index="KeywordIndex:brains",
                    widget=atapi.InAndOutWidget(
                        label=_(u'label_publication_groups',
                                default=u'Publication groups'),
                        description=_(u'description_publication_groups',
                                      default=u'Fill in publication groups'),
                        i18n_domain='eea.reports',
                        ),
                    ),
            ReportOrderableReferenceField('relatedItems',
                    schemata='relations',
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
            ReportFloatField('price',
                    schemata='report',
                    languageIndependent=True,
                    default=0,
                    widget=atapi.DecimalWidget(
                        label=_(u'label_price', default=u'Price (Euro)'),
                        description=_(u'description_price',
                                      default=u'Fill in publication price'),
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
                        label=_(u'label_order_override_text',
                         default=u'Override the order text with your own text'),
                        description=_(u'description_order_override_text',
                                 default=u'Fill in to override the order text'),
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
                        label=_(u'label_order_extra_text',
                               default=u'OR add some text to the order screen'),
                        description=_(u'description_order_extra_text',
                         default=u'Fill in to add this text to the order text'),
                        i18n_domain='eea.reports',
                        ),
                    ),
            ReportIntegerField('pages',
                    schemata='report',
                    lanaguageIndependent=False,
                    default=0,
                    widget=atapi.IntegerWidget(
                        label=_(u'label_pages', default=u'Pages'),
                        description=_(u'description_pages',
                                      default=u'Fill in total number of pages'),
                        i18n_domain='eea.reports',
                        ),
                    ),
#            ReportManagementPlanField(
#                    name='management_plan',
#                    schemata='report',
#                    languageIndependent=True,
#                    required_for_published=True,
#                    required=True,
#                    default=(datetime.now().year, ''),
#                    validators=('management_plan_code_validator',),
#                    vocabulary=DatasetYears(),
#                    widget=ManagementPlanWidget(
#                        format="select",
#                        label="EEA Management Plan",
#                        description=(
#                            "EEA Management plan code. Internal EEA project "
#                            "line code, used to assign an EEA product output to"
#                            " a specific EEA project number in the "
#                            "management plan."),
#                        label_msgid='dataservice_label_eea_mp',
#                        description_msgid='dataservice_help_eea_mp',
#                        i18n_domain='eea.dataservice',
#                        )
#                    ),
            ReportStringField('copyrights',
                    schemata='report',
                    languageIndependent=True,
                    default=COPYRIGHTS,
                    widget=atapi.StringWidget(
                        label=_(u'label_copyrights', default=u'Copyrights'),
                        description=_(u'description_copyrights',
                                      default=u'Fill in copyrights'),
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
                        label=_(u'label_trailer', default=u'Trailer'),
                        description=_(u'description_trailer',
                                      default=u'Fill in the trailer.'),
                        i18n_domain='eea.reports',
                        )
                    ),
            ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """ Returns available fields
        """
        return self._fields

    def getOrder(self, original):
        """ Returns fields order
        """
        order = original.get('report', [])
        new_order = [
                'serial_title',
                'isbn',
                'creators',
                'publishers',
#                'themes',
                'publication_groups',
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
        original['report'] = new_order

        return original
