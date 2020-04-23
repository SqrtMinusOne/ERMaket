from bs4 import BeautifulSoup
from .xml_object import XMLObject

__all__ = ['RootMixin']


class RootMixin:
    def _init_root(self, xml, root_attrs, *args, **kwargs):
        if isinstance(xml, BeautifulSoup):
            self.soup = xml
            args, kwargs = self._from_xml(getattr(self.soup, self._tag_name))
        elif isinstance(xml, str) and len(xml) > 0:
            self.soup = BeautifulSoup(xml, features='xml')
            args, kwargs = self._from_xml(getattr(self.soup, self._tag_name))
        else:
            self.soup = BeautifulSoup(features='xml')
            if args is None:
                args = []
            if kwargs is None:
                kwargs = {}
            self.soup.append(self.soup.new_tag(self._tag_name, root_attrs))
        XMLObject.soup = self.soup
        return args, kwargs
