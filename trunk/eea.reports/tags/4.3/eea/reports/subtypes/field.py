""" Archetypes custom fields
"""
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Field import decode, encode
from Products.Archetypes.Registry import registerField, registerPropertyType
from Products.Archetypes.utils import DisplayList
from Products.Archetypes.Field import ReferenceField
from Products.Archetypes import atapi

from archetypes.schemaextender.field import ExtensionField

from eea.reports.subtypes.widget import SerialTitleWidget
from eea.reports.events import FileUploadedEvent

from plone.app.blob.field import BlobField

from zope.schema.interfaces import IVocabularyFactory
from zope.event import notify
from zope.component import queryUtility

from eea.forms.fields.ManagementPlanField import ManagementPlanField

import logging
logger = logging.getLogger('eea.reports.subtypes.field')

class SerialTitleField(atapi.ObjectField):
    """For creating lines objects"""
    _properties = atapi.ObjectField._properties.copy()
    _properties.update({
        'types_vocabulary' : (),
        'years_vocabulary' : (),
        'default': (),
        'widget' : SerialTitleWidget,
    })

    security = ClassSecurityInfo()

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """
        If passed-in value is a string, split at line breaks and
        remove leading and trailing white space before storing in object
        with rest of properties.
        """
        rtype = decode(value[0].strip(), instance, **kwargs)
        num = value[1]
        year = value[2]
        alt = decode(value[3].strip(), instance, **kwargs)
        value = (rtype, num, year, alt)
        super(SerialTitleField, self).set(instance, value, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        """ Getter
        """
        value = super(SerialTitleField, self).get(instance, **kwargs) or ()
        data = [encode(v, instance, **kwargs) for v in value]
        return tuple(data)

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
        """ Raw getter
        """
        return self.get(instance, **kwargs)

    security.declarePublic('is_empty')
    def is_empty(self, instance, **kwargs):
        """ Check if serial title is set or not.
        """
        value = self.get(instance, **kwargs)
        if not value:
            return True
        if len(value) < 4:
            return True

        # Alt title is not empty
        if value[3]:
            return False
        elif value[0] and value[0] != 'N/A':
            return False
        return True

    security.declarePublic('get_size')
    def get_size(self, instance):
        """Get size of the stored data used for get_size in BaseObject
        """
        size = 0
        for line in self.get(instance):
            size += len(str(line))
        return size

    security.declarePublic('Vocabulary')
    def Vocabulary(self, content_instance=None, vocabulary='types_vocabulary'):
        """ Returns a DisplayList
        """

        value = getattr(self, vocabulary, None)
        if not isinstance(value, (unicode, str)):
            return DisplayList()

        if not isinstance(value, unicode):
            value = value.decode('utf-8')

        vocab = queryUtility(IVocabularyFactory, value)
        if not vocab:
            return DisplayList()

        return DisplayList(((term.value, term.title, term.token) for term in
                            vocab(content_instance)))

class ExtensionFieldMixin:
    """ Archetypes SchemaExtender FieldMixin
    """
    def translationMutator(self, instance):
        """ Translation mutator
        """
        return self.getMutator(instance)

class ReportOrderableReferenceField(ExtensionField, ExtensionFieldMixin,
                                    ReferenceField):
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

class ReportManagementPlanField(ExtensionField, ExtensionFieldMixin,
                                ManagementPlanField):
    """ Archetypes SchemaExtender aware management plan field """

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

registerField(SerialTitleField,
              title='Serial Title Field',
              description=('Used for storing report serial title'))

registerPropertyType('types_vocabulary', 'string')
registerPropertyType('years_vocabulary', 'string')
