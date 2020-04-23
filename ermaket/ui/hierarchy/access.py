from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QHeaderView, QPushButton, QTableWidget, QTableWidgetItem
)

from ermaket.api.system.hierarchy import AccessRight, RoleAccess

__all__ = ['AccessTable']


class AccessTable(QTableWidget):
    TYPES = {
        1: AccessRight(AccessRight.VIEW),
        2: AccessRight(AccessRight.CHANGE),
        3: AccessRight(AccessRight.DELETE)
    }

    def __init__(self, parent):
        super(AccessTable, self).__init__(parent)
        self.setColumnCount(5)
        self.setHorizontalHeaderLabels(
            ['Role', 'View', 'Change', 'Delete', 'Action']
        )
        self.cellChanged.connect(self._on_cell_changed)
        self._setting_data = False
        self.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

    def set_access(self, access):
        self.access = access
        self._fill_table()

    def update_state(self):
        self._fill_table()

    def _fill_table(self):
        self._setting_data = True
        self.setRowCount(0)
        if self.access.inherit:
            self.setEnabled(False)
            return
        self.setEnabled(True)
        self.setRowCount(len(self.access))

        for i, role_access in enumerate(self.access):
            self._fill_row(i, role_access)

        self._setting_data = False

    def _fill_row(self, i, role_access):
        def on_delete():
            return self.on_delete(i)

        self.setItem(i, 0, QTableWidgetItem(role_access.role_name))
        for k in range(1, 4):
            self._add_checkbox(i, k, role_access.has(self.TYPES[k]))
        delete_button = QPushButton()
        delete_button.setIcon(QIcon(':/icons/delete.png'))
        delete_button.clicked.connect(on_delete)
        self.setCellWidget(i, 4, delete_button)

    def on_delete(self, i):
        del self.access[i]
        self._fill_table()

    def on_add(self):
        self._setting_data = True
        self.setRowCount(self.rowCount() + 1)
        new = RoleAccess("", [])
        self.access.append(new)
        self._fill_row(self.rowCount() - 1, new)
        self._setting_data = False

    def _add_checkbox(self, x, y, value):
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        if value:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.setItem(x, y, item)

    def _on_cell_changed(self, x, y):
        if self._setting_data:
            return
        if 1 <= y <= 3:
            state = self.item(x, y).checkState()
            if state:
                self.access[x].access_types.add(self.TYPES[y])
                if y == 2 or y == 3:
                    self.item(x, 1).setCheckState(Qt.Checked)
            else:
                self.access[x].access_types.discard(self.TYPES[y])
                if y == 1:
                    self.item(x, 2).setCheckState(Qt.Unchecked)
                    self.item(x, 3).setCheckState(Qt.Unchecked)
        elif y == 0:
            self.access[x].role_name = self.item(x, y).text()
