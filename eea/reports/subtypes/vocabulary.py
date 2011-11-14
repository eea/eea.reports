""" Reports vocabularies
"""
from datetime import datetime
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from eea.reports.config import STARTING_YEAR
from Products.ATVocabularyManager.namedvocabulary import NamedVocabulary
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm

class ReportYears(object):
    """ Report years vocabulary
    """
    implements(IVocabularyFactory)

    def __call__(self, context=None):
        now = datetime.now()
        end_year = now.year + 2
        terms = [SimpleTerm('-1', '-1', 'N/A'), ]
        terms.extend(SimpleTerm(str(key), str(key), str(key))
                        for key in reversed(range(STARTING_YEAR, end_year)))
        return SimpleVocabulary(terms)

class ReportTypes(object):
    """ Report types
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        voc = NamedVocabulary('report_types')
        items = [SimpleTerm('N/A', 'N/A', 'N/A'), ]
        items.extend([SimpleTerm(value, key, value) for key, value in
                      voc.getDisplayList(context).items()])
        return SimpleVocabulary(items)


class ReportCreators(object):
    """ Report creators
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        voc = NamedVocabulary("report_creators")
        items = voc.getDisplayList(context).items()
        return SimpleVocabulary([SimpleTerm(value, key, value)
                                 for key, value in items])


class ReportPublishers(object):
    """ Report publishers
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        voc = NamedVocabulary("report_publishers")
        items = voc.getDisplayList(context).items()
        return SimpleVocabulary([SimpleTerm(value, key, value)
                                 for key, value in items])


class PublicationGroups(object):
    """ Publication Groups
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        voc = NamedVocabulary("publications_groups")
        items = voc.getDisplayList(context).items()
        return SimpleVocabulary([SimpleTerm(key, key, value)
                                 for key, value in items])
