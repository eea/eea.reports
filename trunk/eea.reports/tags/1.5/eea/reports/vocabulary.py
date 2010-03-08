""" Reports vocabularies
"""
from datetime import datetime
from zope.interface.declarations import implements
from zope.app.schema.vocabulary import IVocabularyFactory
from eea.reports.config import STARTING_YEAR
from eea.themecentre.vocabulary import ThemesEditVocabularyFactory
from Products.Archetypes.interfaces.vocabulary import IVocabulary

class ReportYearsVocabularyFactory(object):
    """ Report years vocabulary
    """
    implements(IVocabularyFactory,)
    
    def __call__(self):
        now = datetime.now()
        end_year = now.year + 2
        terms = [('-1', 'N/A')]
        terms.extend((str(key), str(key))
                     for key in reversed(range(STARTING_YEAR, end_year)))
        return terms

ReportYearsVocabulary = ReportYearsVocabularyFactory()

class ReportThemesVocabulary:
    """ Report themes vocabulary
    """
    __implements__ = (IVocabulary,)
    
    def getDisplayList(self, instance):
        """ Returns 
        """
        vocab = ThemesEditVocabularyFactory(instance)
        return [(term.value, term.title) for term in vocab]

    def getVocabularyDict(self, instance):
        return {}
    
    def isFlat(self):
        return False
    
    def showLeafsOnly(self):
        return False
