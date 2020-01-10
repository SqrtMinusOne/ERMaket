from collections import namedtuple
from typing import List

from api.erd.er_entities import XMLObject

__all__ = ['Element', 'Button', 'Trigger']

Button = namedtuple('Button', ['text', 'location'])
Trigger = namedtuple('Trigger', ['activation', 'scriptId'])


class Element(XMLObject):
    def __init__(
        self,
        _id: int,
        name: str,
        buttons: List[Button] = None,
        triggers: List[Trigger] = None
    ):
        self._id = _id
        self.name = name
        self.buttons = buttons
        self.triggers = triggers

    @classmethod
    def from_xml(cls, tag):
        _id = int(tag['id'])
        name = tag.find('name').text
        buttons, triggers = None, None
        if tag.buttonList:
            buttons = [
                Button(but.text.text, but.location.text)
                for but in tag.buttonList.children
            ]
        if tag.triggerList:
            triggers = [
                Trigger(trg.activation.text, int(trg.scriptId.text))
                for trg in tag.triggerList.children
            ]
        return cls(_id, name, buttons, triggers)

    def to_xml(self, name):
        tag = self.soup.new_tag('entity', id=self._id)
        tag.append(self.new_tag('name', self.name))
