##parameters=REQUEST=None

eeaid = REQUEST.get('eeaid', None)
url = '%s?portal_status_message=%s'

try:
    eeaid = int(eeaid)
except:
    msg = "you must provide a number for the value of eeaid (internal EEA ID)."
    return context.REQUEST.RESPONSE.redirect(url % (context.absolute_url(), msg))

ctool = context.portal_catalog
brains = ctool(eeaid=eeaid,
               object_provides='eea.reports.interfaces.IReportContainerEnhanced')

redirect_to = ''
for brain in brains:
    redirect_to = brain.getURL()
    break

if not redirect_to:
    msg = 'No publications found with internal EEA ID = %s.' % eeaid
    return context.REQUEST.RESPONSE.redirect(url % (context.absolute_url(), msg))

return context.REQUEST.RESPONSE.redirect(redirect_to)
