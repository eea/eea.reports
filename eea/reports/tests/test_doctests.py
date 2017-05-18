""" Doc tests
"""
import doctest
import unittest
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

from eea.reports.tests.base import ReportFunctionalTestCase
try:
    from eea import rdfmarshaller as RDF
except ImportError:
    RDF = None

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """ Suite
    """
    suite = (
            Suite('doc/subtyping.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase),
            Suite('doc/metadata.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase),
            Suite('doc/metaparser.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase),
            Suite('doc/coverimage.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase),
            Suite('doc/relations.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase),
            )

    if RDF is not None:
        suite += (
            Suite('doc/marshaller.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase),
              )

    return unittest.TestSuite(suite)
