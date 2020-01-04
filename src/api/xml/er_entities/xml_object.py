from abc import ABC, abstractmethod

import bs4


__all__ = ['XMLObject']


class XMLObject(ABC):
    """An abstract class for a xml-derived object"""
    soup: bs4.BeautifulSoup = None

    @classmethod
    @abstractmethod
    def from_xml(cls, tag: bs4.element.Tag):
        pass

    @abstractmethod
    def to_xml(self):
        pass

    @classmethod
    def new_tag(cls, name, string):
        tag = cls.soup.new_tag(name)
        tag.string = string
        return tag
