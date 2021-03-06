from collections import namedtuple

import pytest

from ermaket.api.system import Hierachy, HierachyConstructor
from ermaket.api.system.hierarchy import AccessRight

DummyRole = namedtuple('DummyRole', ['name'])


@pytest.mark.usefixtures("algorithm")
def test_constructor(algorithm):
    dummy_admin = DummyRole(name='admin')
    constructor = HierachyConstructor(algorithm.tables, 'er1', dummy_admin)

    hierarchy = constructor.construct()
    constructor.insert_system_pages(hierarchy)

    xml1 = hierarchy.pretty_xml()
    xml2 = Hierachy.from_xml(hierarchy.pretty_xml()).pretty_xml()
    assert xml1 == xml2

    obj1 = hierarchy.to_object()
    assert obj1 == Hierachy.from_xml(hierarchy.pretty_xml()).to_object()


def test_extract(algorithm):
    admin1 = DummyRole(name='admin1')
    admin2 = DummyRole(name='admin2')
    c1 = HierachyConstructor(algorithm.tables, 'er1', admin1)
    c2 = HierachyConstructor(algorithm.tables, 'er2', admin2)
    h1 = c1.construct()

    elem = h1.values[0]
    assert elem.accessRights.has(['admin1'], AccessRight.VIEW)
    assert elem.accessRights.has(['admin1'], AccessRight.CHANGE)
    assert elem.accessRights.has(['admin1'], AccessRight.DELETE)

    assert not elem.accessRights.has(['admin2'], AccessRight.VIEW)
    assert not elem.accessRights.has(['admin2'], AccessRight.CHANGE)
    assert not elem.accessRights.has(['admin2'], AccessRight.DELETE)

    h = Hierachy.from_xml(h1.to_xml())
    h2 = c2.construct()

    h1.merge(h2)
    assert h1.pretty_xml() == Hierachy.from_xml(h1.pretty_xml()).pretty_xml()

    h3 = h1.extract([admin1.name])
    assert h.pretty_xml() == h3.pretty_xml()

    r1 = h1.extract_rights([admin1.name])
    r2 = h3.extract_rights([admin1.name])
    assert r1 == r2

    h1.drop_schema('er2')
    er2_section = [
        section for section in h1.sections if section.name == 'Er2'
    ][0]
    assert len(er2_section._children) == 0

    h1.drop_by_id(er2_section.id)
    assert h.pretty_xml() == h1.pretty_xml()
