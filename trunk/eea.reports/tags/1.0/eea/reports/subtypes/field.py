import logging
logger = logging.getLogger('eea.reports.subtypes.field')

from persistent.list import PersistentList
from types import ListType, TupleType, StringType, UnicodeType
from AccessControl import ClassSecurityInfo
from zope.app.annotation.interfaces import IAnnotations
from eea.themecentre.themetaggable import KEY, checkTheme
from Products.Archetypes.interfaces.vocabulary import IVocabulary
from Products.Archetypes.atapi import ObjectField, StringField
from Products.Archetypes.Field import decode, encode
from Products.Archetypes.utils import DisplayList, mapply, Vocabulary
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerPropertyType
from eea.reports.subtypes.widget import SerialTitleWidget
from eea.themecentre.interfaces import IThemeTagging

STRING_TYPES = [StringType, UnicodeType]

class ThemesField(StringField):
    """ Save themes as annotation """
    def set(self, instance, value, **kwargs):
        """ Save as annotation
        """
        IThemeTagging(instance).tags = value

    def get(self, instance, **kwargs):
        """ Get from annotation
        """
        return IThemeTagging(instance).tags

class SerialTitleField(ObjectField):
    """For creating lines objects"""
    _properties = ObjectField._properties.copy()
    _properties.update({
        'types_vocabulary' : (),
        'years_vocabulary' : (),
        'default': (),
        'widget' : SerialTitleWidget,
    })

    security  = ClassSecurityInfo()

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
        ObjectField.set(self, instance, value, **kwargs)

    security.declarePrivate('get')
    def get(self, instance, **kwargs):
        value = ObjectField.get(self, instance, **kwargs) or ()
        data = [encode(v, instance, **kwargs) for v in value]
        return tuple(data)

    security.declarePrivate('getRaw')
    def getRaw(self, instance, **kwargs):
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
        size=0
        for line in self.get(instance):
            size+=len(str(line))
        return size

    security.declarePublic('Vocabulary')
    def Vocabulary(self, content_instance=None, vocabulary='types_vocabulary'):
        """
        Returns a DisplayList.

        Uses self.vocabulary as source.

        1) Static vocabulary

           - is already a DisplayList
           - is a list of 2-tuples with strings (see above)
           - is a list of strings (in this case a DisplayList
             with key=value will be created)

        2) Dynamic vocabulary:

           - precondition: a content_instance is given.

           - has to return a:

                * DisplayList or
                * list of strings or
                * list of 2-tuples with strings:
                    '[("key1","value 1"),("key 2","value 2"),]'

           - the output is postprocessed like a static vocabulary.

           - vocabulary is a string:
                if a method with the name of the string exists it will be called

           - vocabulary is a class implementing IVocabulary:
                the "getDisplayList" method of the class will be called.

        """

        value = getattr(self, vocabulary, ())
        if not isinstance(value, DisplayList):

            if content_instance is not None and type(value) in STRING_TYPES:
                # Dynamic vocabulary by method on class of content_instance
                method = getattr(content_instance, value, None)
                if method and callable(method):
                    args = []
                    kw = {'content_instance' : content_instance,
                          'field' : self}
                    value = mapply(method, *args, **kw)
            elif content_instance is not None and \
                 IVocabulary.isImplementedBy(value):
                # Dynamic vocabulary provided by a class that
                # implements IVocabulary
                value = value.getDisplayList(content_instance)

            # Post process value into a DisplayList
            # Templates will use this interface
            sample = value[:1]
            if isinstance(sample, DisplayList):
                # Do nothing, the bomb is already set up
                pass
            elif type(sample) in (TupleType, ListType):
                # Assume we have ((value, display), ...)
                # and if not ('', '', '', ...)
                if sample and type(sample[0]) not in (TupleType, ListType):
                    # if not a 2-tuple
                    value = zip(value, value)
                value = DisplayList(value)
            elif len(sample) and type(sample[0]) is StringType:
                value = DisplayList(zip(value, value))
            else:
                logger.debug('Unhandled type in Vocab')
                logger.debug(value)

        if content_instance:
            # Translate vocabulary
            i18n_domain = (getattr(self, 'i18n_domain', None) or
                          getattr(self.widget, 'i18n_domain', None))

            return Vocabulary(value, content_instance, i18n_domain)

        return value

registerField(SerialTitleField,
              title='Serial Title Field',
              description=('Used for storing report serial title'))

registerPropertyType('types_vocabulary', 'string')
registerPropertyType('years_vocabulary', 'string')
