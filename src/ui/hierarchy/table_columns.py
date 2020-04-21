from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox, QHeaderView, QTableWidgetItem, QWidget

from api.system.hierarchy import TableLinkType
from api.system.hierarchy.table import _link_type_multiple, _link_type_singular
from ui.ui_compiled.hierarchy.table_columns import Ui_TableColumns

__all__ = ['TableColumns']


class TableColumns(QWidget):
    COLUMNS = {0: 'rowName', 1: 'type', 3: 'text'}
    COLUMNS_CB = {4: 'isSort', 5: 'isFilter', 6: 'isFilter', 7: 'isVisible'}
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

    def _connect_ui(self):
        self.ui.table.cellChanged.connect(self._on_cell_changed)

    def set_elem(self, elem):
        self.elem = elem
        self._set_columns()

    def _set_columns(self):
        self.ui.table.blockSignals(True)
        self.ui.table.setRowCount(0)
        self.ui.table.setRowCount(len(self.elem.columns))
        for row, column in enumerate(self.elem.columns):
            for col, attr in self.COLUMNS.items():
                item = QTableWidgetItem(getattr(column, attr))
                self.ui.table.setItem(row, col, item)
                if col < 2:
                    item.setFlags(Qt.ItemIsEnabled)
                else:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)

            for col, attr in self.COLUMNS_CB.items():
                enabled = not (
                    col != 7 and column._tag_name == 'linkedColumn'
                    and column.isMultiple
                )
                self._add_checkbox(row, col, enabled, getattr(column, attr))

            if column._tag_name == 'linkedColumn':
                self._add_link_type(row, column)
            else:
                item = QTableWidgetItem()
                item.setFlags(Qt.NoItemFlags)
                self.ui.table.setItem(row, self.LINK_TYPE, item)
        self.ui.table.blockSignals(False)

    def _add_link_type(self, row, column):
        combobox = QComboBox()
        if column.isMultiple:
            combobox.addItems([str(val) for val in _link_type_multiple])
        else:
            combobox.addItems([str(val) for val in _link_type_singular])
        combobox.setCurrentText(str(column.linkType))
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

    def _on_cell_changed(self, row, col):
        print(row, col)
        # item = self.item(row, col)
        pass
