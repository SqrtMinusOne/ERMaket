from bs4 import BeautifulSoup
from .xml_object import XMLObject

__all__ = ['RootMixin']


class RootMixin:
    def _init_root(self, xml, root_attrs):
        if xml is not None:
            if isinstance(xml, BeautifulSoup):
                self.soup = xml
            else:
                self.soup = BeautifulSoup(xml, features='xml')
            args, kwargs = self._from_xml(self.soup.hierarchy)
        else:
            self.soup = BeautifulSoup(features='xml')
            args, kwargs = [], {}
            self.soup.append(
                self.soup.new_tag(
                    self._tag_name, root_attrs
                )
            )
        XMLObject.soup = self.soup
        return args, kwargs
