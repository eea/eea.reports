""" Interfaces for PDF handlers
"""
import warnings
from eea.converter.interfaces import IPDFCoverImage
from eea.converter.interfaces import IPDFMetadataParser as IReportPDFParser
from eea.converter.interfaces import IPDFMetadataUpdater

warnings.warn("eea.reports.pdf.interfaces is deprecated. "
              "Please use eea.converter.interfaces instead",
              DeprecationWarning)
# BBB
__all__ = [
    IPDFCoverImage.__name__,
    IReportPDFParser.__name__,
    IPDFMetadataUpdater.__name__,
]
