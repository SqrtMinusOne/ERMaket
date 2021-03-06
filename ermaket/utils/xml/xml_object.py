from abc import ABC, abstractmethod

import bs4
import prettierfier

__all__ = ['XMLObject', 'ConvertableXML']


class ConvertableXML(ABC):
    @abstractmethod
    def to_object(self, add_name=False):
        pass


class XMLObject(ABC):
    """An abstract class for a xml-derived object"""
    soup: bs4.BeautifulSoup = None

    @staticmethod
    def _make_args(*args, **kwargs):
        return (args, kwargs)

    @property
    @abstractmethod
    def _tag_name(self):
        pass

    @classmethod
    @abstractmethod
    def _from_xml(cls, tag):
        pass

    @classmethod
    def from_xml(cls, tag: bs4.element.Tag):
        args, kwargs = cls._from_xml(tag)
        return cls(*args, **kwargs)

    @abstractmethod
    def to_xml(self) -> bs4.element.Tag:
        pass

    def pretty_xml(self) -> str:
        return prettierfier.prettify_xml(str(self.to_xml()), 4)

    @classmethod
    def new_tag(cls, name, string):
        tag = cls.soup.new_tag(name)
        tag.string = str(string)
        return tag
