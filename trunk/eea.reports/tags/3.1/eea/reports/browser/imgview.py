from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from valentine.imagescales.browser.interfaces import IImageView
from valentine.imagescales.browser import atfield, atfolder

class ImageView(BrowserView):
    """ Get cover image from folder contents or from canonical folder contents
    """
    implements(IImageView)

    def __init__(self, context, request):
        super(ImageView, self).__init__(context, request)
        self.img = atfolder.ImageView(context, request)
        canonical = context.getCanonical()
        if context != canonical:
            self.canonical = atfolder.ImageView(canonical, request)
        else:
            self.canonical = self.img

    def display(self, scalename='thumb'):
        return self.img.display(scalename) or self.canonical.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.img.display(scalename):
            return self.img(scalename)
        if self.canonical.display(scalename):
            return self.canonical(scalename)
        raise NotFound(self.request, self.name)
