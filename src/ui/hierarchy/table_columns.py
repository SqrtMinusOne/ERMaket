from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QHeaderView, QPushButton,
                             QTableWidgetItem, QWidget)

from api.system.hierarchy import TableLinkType
from api.system.hierarchy.table import _link_type_multiple, _link_type_singular
from ui.ui_compiled.hierarchy.table_columns import Ui_TableColumns

from .column_dialog import ColumnDialog

__all__ = ['TableColumns']


class TableColumns(QWidget):
    COLUMNS = {0: 'rowName', 1: 'type', 3: 'text'}
    COLUMNS_CB = {4: 'isSort', 5: 'isFilter', 6: 'isEditable', 7: 'isVisible'}
    LINK_TYPE = 2
    ACTIONS = 8

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_TableColumns()
        self.ui.setupUi(self)
        self.ui.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self._connect_ui()

    def _block_signals(func):
        def decorate(self, *args, **kwargs):
            self.ui.table.blockSignals(True)
            res = func(self, *args, **kwargs)
            self.ui.table.blockSignals(False)
            return res

        return decorate

    def _connect_ui(self):
        self.ui.table.cellChanged.connect(self._on_cell_changed)

    def set_elem(self, elem):
        self.elem = elem
        self._set_columns()

    @_block_signals
    def _set_columns(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setRowCount(len(self.elem.columns))
        for row, column in enumerate(self.elem.columns):
            self._set_row(row, column)

    @_block_signals
    def _set_row(self, row, column):
        for col, attr in self.COLUMNS.items():
            item = QTableWidgetItem(getattr(column, attr))
            self.ui.table.setItem(row, col, item)
            if col < 2:
                item.setFlags(Qt.ItemIsEnabled)
            else:
                item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)

        for col, attr in self.COLUMNS_CB.items():
            enabled = not (
                col != 7 and col != 6 and
                column._tag_name == 'linkedColumn' and column.isMultiple
            )
            self._add_checkbox(row, col, enabled, getattr(column, attr))

        if column._tag_name == 'linkedColumn':
            self._add_link_type(row, column)
        else:
            item = QTableWidgetItem()
            item.setFlags(Qt.NoItemFlags)
            self.ui.table.setItem(row, self.LINK_TYPE, item)
        self._add_actions(row)

    def _add_link_type(self, row, column):
        def on_link_type_changed(value):
            new = TableLinkType(value)
            column.linkType = new

        combobox = QComboBox()
        if column.isMultiple:
            combobox.addItems([str(val) for val in _link_type_multiple])
        else:
            combobox.addItems([str(val) for val in _link_type_singular])
        combobox.setCurrentText(str(column.linkType))
        combobox.currentTextChanged.connect(on_link_type_changed)
        self.ui.table.setCellWidget(row, self.LINK_TYPE, combobox)

    def _add_checkbox(self, x, y, enabled, value):
        item = QTableWidgetItem()
        if enabled:
            item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        else:
            item.setFlags(Qt.ItemIsUserCheckable)
        if value:
            item.setCheckState(Qt.Checked)
        else:
            item.setCheckState(Qt.Unchecked)
        self.ui.table.setItem(x, y, item)
        return item

    def _add_actions(self, row):
        def on_up():
            self._swap_rows(row, row - 1)

        def on_down():
            self._swap_rows(row, row + 1)

        def on_save():
            self._set_row(row, self.elem.columns[row])

        def on_edit():
            dialog = ColumnDialog(self.elem, row, self)
            dialog.saved.connect(on_save)
            dialog.show()

        actions = QWidget()
        layout = QHBoxLayout()
        actions.setLayout(layout)

        up = QPushButton()
        up.setIcon(QIcon(':/icons/up.png'))
        up.setDisabled(row == 0)
        up.clicked.connect(on_up)
        layout.addWidget(up)

        down = QPushButton()
        down.setIcon(QIcon(':/icons/down.png'))
        down.setDisabled(row == len(self.elem.columns) - 1)
        down.clicked.connect(on_down)
        layout.addWidget(down)

        edit = QPushButton()
        edit.setIcon(QIcon(':/icons/edit.png'))
        edit.clicked.connect(on_edit)
        layout.addWidget(edit)
        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.table.setCellWidget(row, self.ACTIONS, actions)

    @_block_signals
    def _swap_rows(self, a, b):
        cols = self.ui.table.columnCount()
        for col in range(cols):
            item = self.ui.table.takeItem(a, col)
            self.ui.table.setItem(a, col, self.ui.table.takeItem(b, col))
            self.ui.table.setItem(b, col, item)

        self.elem.columns[a], self.elem.columns[b] = self.elem.columns[
            b], self.elem.columns[a]

        self.ui.table.removeCellWidget(a, self.LINK_TYPE)
        self.ui.table.removeCellWidget(b, self.LINK_TYPE)

        if self.elem.columns[a]._tag_name == 'linkedColumn':
            self._add_link_type(a, self.elem.columns[a])
        if self.elem.columns[b]._tag_name == 'linkedColumn':
            self._add_link_type(b, self.elem.columns[b])
        self._add_actions(a)
        self._add_actions(b)

    def _on_cell_changed(self, row, col):
        cb = self.COLUMNS_CB.get(col, None)
        if cb is not None:
            state = self.ui.table.item(row, col).checkState()
            setattr(self.elem.columns[row], cb, bool(state))
            return
        attr = self.COLUMNS.get(col, None)
        if attr is not None:
            value = self.ui.table.item(row, col).text()
            setattr(self.elem.columns[row], attr, value)
