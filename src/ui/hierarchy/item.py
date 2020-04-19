from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtGui import QIcon

__all__ = ['HierachyTreeItem']


class HierachyTreeItem(QTreeWidgetItem):
    NAMES = {
        'section': 'Section',
        'formEntry': 'Form',
        'tableEntry': 'Table',
        'page': 'User Page',
        'prebuiltPageEntry': 'Prebuilt page'
    }

    ICONS = {
        'section': ':/icons/entry.png',
        "formEntry": ':/icons/form.png',
        'tableEntry': ':/icons/table.png',
        'page': ':/icons/page.png',
        'prebuiltPageEntry': ':/icons/prebuiltPage.png'
    }

    def __init__(self, elem, hierarchy, *args, **kwargs):
        super(QTreeWidgetItem, self).__init__(*args, **kwargs)
        self.elem = elem
        self._hierarchy = hierarchy

        flags = Qt.ItemIsSelectable | Qt.ItemIsDragEnabled | Qt.ItemIsEnabled

        if self.can_have_children:
            flags = flags | Qt.ItemIsDropEnabled
        self.setFlags(flags)

        self.update_ui()
        self.is_root = False

    def update_ui(self):
        self.setText(0, self.elem.name)
        self.setText(1, self.elem_type)

        icon = self.ICONS.get(self.elem._tag_name, None)
        if icon is not None:
            self.setIcon(1, QIcon(icon))

    def add_children(self):
        if self.can_have_children:
            for child_id in self.elem.children:
                elem = self._hierarchy.get_by_id(child_id)
                HierachyTreeItem(elem, self._hierarchy, self)

    def set_child_ids(self):
        if self.can_have_children:
            ids = []
            for i in range(self.childCount()):
                child = self.child(i)
                ids.append(child.elem.id)
                child.is_root = False
                child.set_child_ids()
            self.elem.set_child_ids(ids)

    @property
    def can_have_children(self):
        return self.elem._tag_name == 'section'

    @property
    def elem_type(self):
        return self.NAMES.get(
            self.elem._tag_name, f"<{self.elem._tag_name} />"
        )
