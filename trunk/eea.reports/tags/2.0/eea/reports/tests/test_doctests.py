""" Doc tests
"""
import doctest
import unittest
from base import ReportFunctionalTestCase
from Testing.ZopeTestCase import FunctionalDocFileSuite as Suite

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


def test_suite():
    """ Suite
    """
    return unittest.TestSuite((
            Suite('doc/subtyping.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase) ,
            Suite('doc/metadata.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase) ,
            Suite('doc/coverimage.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase) ,
            Suite('doc/relations.txt',
                  optionflags=OPTIONFLAGS,
                  package='eea.reports',
                  test_class=ReportFunctionalTestCase) ,
              ))
