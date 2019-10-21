""" eea.depiction IImageView adapter
"""
from zope.interface import implements
from zope.publisher.interfaces import NotFound
from Products.Five.browser import BrowserView
from eea.depiction.browser.interfaces import IImageView
from eea.depiction.browser import atfolder

class ImageView(BrowserView):
    """ Get cover image from folder contents or from canonical folder contents
    """
    implements(IImageView)
    _img = False

    @property
    def img(self):
        """ img
        """
        if self._img is False:
            self._img = atfolder.FolderImageView(self.context, self.request)
            if not getattr(self._img, 'img', None):
                canonical = self.context.getCanonical()
                if self.context != canonical:
                    self._img = atfolder.FolderImageView(canonical, self.request)
        return self._img

    def display(self, scalename='thumb'):
        """ Display image?
        """
        return self.img.display(scalename)

    def __call__(self, scalename='thumb'):
        if self.img.display(scalename):
            return self.img(scalename)
        raise NotFound(self.request, self.name)
