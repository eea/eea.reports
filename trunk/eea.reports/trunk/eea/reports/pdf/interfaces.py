""" Interfaces for PDF handlers
"""
from eea.converter.interfaces import IPDFCoverImage
from eea.converter.interfaces import IPDFMetadataParser as IReportPDFParser
from eea.converter.interfaces import IPDFMetadataUpdater

# BBB
__all__ = [
    IPDFCoverImage.__name__,
    IReportPDFParser.__name__,
    IPDFMetadataUpdater.__name__,
]
