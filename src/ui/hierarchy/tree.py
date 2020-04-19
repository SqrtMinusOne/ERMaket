from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTreeWidget

from api.system import Hierachy

from .item import HierachyTreeItem

__all__ = ['HierachyTree']


class HierachyTree(QTreeWidget):
    order_updated = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHeaderLabels(['Name', 'Type'])
        self.setDragEnabled(True)
        self.setDragDropMode(self.InternalMove)
        self._h = None

    def set_hirearchy(self, h: Hierachy):
        self.clear()
        self._h = h
        root = []
        for elem in h._root:
            item = HierachyTreeItem(elem, h, self)
            item.add_children()
            root.append(item)
        self.addTopLevelItems(root)

    def update_order(self):
        for i in range(self.topLevelItemCount()):
            self.topLevelItem(i).set_child_ids()
        self._h.set_tree()
        self.order_updated.emit()

    def dropEvent(self, event):
        super().dropEvent(event)
        self.update_order()
