""" Initialize
"""
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types, listTypes
from eea.reports.config import PROJECTNAME, DEFAULT_ADD_CONTENT_PERMISSION

def initialize(context):
    """initialize product (called by zope)"""

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME),
        PROJECTNAME)

    cmfutils.ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
        ).initialize(context)
