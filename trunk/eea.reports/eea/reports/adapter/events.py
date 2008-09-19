from eea.reports import interfaces
#
# Debug
#
def printEvent(obj, evt):
    print "================"
    print [obj], [evt]
#
# Restrict report sub-objects
#
def subtype_added(evt):
    """ EVENT

    Called when a Folder is subtyped as report.
    """
    _restrict_subobjects(evt, 1)

def subtype_removed(evt):
    """ EVENT

    Called when a Folder is un-subtyped as report.
    """
    _restrict_subobjects(evt, -1)

def _restrict_subobjects(evt, rtype=-1):
    obj = evt.object
    subtype = evt.subtype
    # Nothing to do
    if not subtype:
        return
    # Only possible report
    if not interfaces.IPossibleReportContainer.providedBy(obj):
        return
    # Only report subtype
    if subtype.type_interface is not interfaces.IReportContainerEnhanced:
        return
    interfaces.IReport(obj).restrictSubObjects(rtype)
#
# Generate cover image
#
def generate_image(obj, evt):
    """ EVENT
        called on objectmodified. Tries to generate the cover image.
    """
    # Make sure we execute this only on the canonical
    if obj != obj.getCanonical():
        return

    interfaces.IReport(obj).generateImage(evt.data)
