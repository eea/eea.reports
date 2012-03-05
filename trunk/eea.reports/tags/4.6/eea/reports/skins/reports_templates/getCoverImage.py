##parameters=REQUEST=None
for image in context.getFolderContents(contentFilter={
    'portal_type': 'Image', 'review_state':['published', 'visible']}, full_objects = True):
    return image

# No image found in context, try to get it from canonical
canonical = context.getCanonical()
if context != canonical:
    return canonical.getCoverImage()
return None
