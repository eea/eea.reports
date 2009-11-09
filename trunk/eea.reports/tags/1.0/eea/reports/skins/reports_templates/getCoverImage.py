##parameters=REQUEST=None
if 'cover' in context.objectIds('ATImage'):
    return context.cover

for image in context.objectValues('ATImage'):
    return image

# No image found in context, try to get it from canonical
canonical = context.getCanonical()
if context != canonical:
    return canonical.getCoverImage()
return None
