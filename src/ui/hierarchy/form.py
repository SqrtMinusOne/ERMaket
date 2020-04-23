from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QHeaderView, QPushButton,
                             QTableWidgetItem, QWidget)

from api.system import HierachyManager
from api.system.hierarchy import (FormGroup, FormGroups, LinkedField, LinkType,
                                  RowNames, SimpleField)
from api.system.hierarchy.form import (_form_link_type_multiple,
                                       _form_link_type_singular)
from ui.ui_compiled.hierarchy.form import Ui_FormColumns

__all__ = ['FormColumns']


class FormColumns(QWidget):
    COLUMNS = {0: 'rowName', 1: 'text', 6: 'hint', 7: 'help'}
    GROUP = 2
    COLUMNS_CB = {4: 'isEditable', 5: 'isVisible'}
    LINK_TYPE = 3
    ACTIONS = 8

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=None)
        self.ui = Ui_FormColumns()
        self.ui.setupUi(self)
        self.ui.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self._connect_ui()
        self.unlocked = False
        self._mgr = HierachyManager(save=False)

        self.ui.add_button.setVisible(False)
        self.ui.add_linked_button.setVisible(False)

    def _block_signals(func):
        def decorate(self, *args, **kwargs):
            self.ui.table.blockSignals(True)
            res = func(self, *args, **kwargs)
            self.ui.table.blockSignals(False)
            return res

        return decorate

    def _connect_ui(self):
        self.ui.table.cellChanged.connect(self._on_cell_changed)
        self.ui.unlock_button.clicked.connect(self._on_unlock)
        self.ui.add_button.clicked.connect(self._on_add)
        self.ui.add_linked_button.clicked.connect(self._on_add_linked)

    def _on_unlock(self):
        self.ui.add_button.setVisible(True)
        self.ui.add_linked_button.setVisible(True)
        self.ui.unlock_button.setVisible(False)
        self.unlocked = True
        self._set_fields()

    def set_elem(self, elem):
        self.elem = elem
        if self.form is not None:
            self._set_fields()
            self.setEnabled(True)
        else:
            self.setEnabled(False)

    @property
    def form(self):
        return self.elem.formDescription

    @_block_signals
    def _set_fields(self):
        self.ui.table.setRowCount(0)
        self.ui.table.setRowCount(len(self.form.fields))
        for row, field in enumerate(self.form.fields):
            self._set_row(row, field)

    @_block_signals
    def _set_row(self, row, field):
        for col, attr in self.COLUMNS.items():
            if col == 0 and self.unlocked:
                self._add_table_column(row)
            else:
                item = QTableWidgetItem(getattr(field, attr))
                self.ui.table.setItem(row, col, item)
                if col == 0 and not self.unlocked:
                    item.setFlags(Qt.ItemIsEnabled)
                else:
                    item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsEditable)

        for col, attr in self.COLUMNS_CB.items():
            self._add_checkbox(row, col, True, getattr(field, attr))

        if field._tag_name == 'linkedField':
            self._add_link_type(row, field)

        group = next(
            (g.legend for g in self.form.groups if field.rowName in g.rows),
            None
        )
        group_item = QTableWidgetItem(group)
        self.ui.table.setItem(row, self.GROUP, group_item)
        self._add_actions(row)

    def _add_table_column(self, row):
        def on_current_text_changed(text):
            self.form.fields[row].rowName = text
            self._update_groups()

        combobox = QComboBox()
        try:
            combobox.addItems([
                col.rowName for col in self._linked_table.columns
            ])
        except AttributeError:
            pass
        combobox.setEditable(True)
        combobox.setCurrentText(self.form.fields[row].rowName)
        combobox.currentTextChanged.connect(on_current_text_changed)
        self.ui.table.setCellWidget(row, 0, combobox)

    def _add_link_type(self, row, field):
        def on_link_type_changed(value):
            new = LinkType(value)
            field.linkType = new

        combobox = QComboBox()
        column = self._linked_column(field)
        if column is not None and column.isMultiple:
            combobox.addItems([str(val) for val in _form_link_type_multiple])
        elif column is not None:
            combobox.addItems([str(val) for val in _form_link_type_singular])
        else:
            combobox.addItems([str(val) for val in LinkType.items.values()])
        combobox.setCurrentText(str(field.linkType))
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

    @property
    def _linked_table(self):
        if self.elem._tag_name == 'tableEntry':
            return self.elem
        else:
            None

    def _linked_column(self, field):
        try:
            return next(
                (
                    col for col in self._linked_table.columns
                    if col.rowName == field.rowName
                ), None
            )
        except AttributeError:
            return None

    def _add_actions(self, row):
        def on_up():
            self._swap_rows(row, row - 1)

        def on_down():
            self._swap_rows(row, row + 1)

        def on_delete():
            self.ui.table.removeRow(row)
            del self.form.fields[row]
            for i in range(self.ui.table.rowCount()):
                self._add_actions(row)

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
        down.setDisabled(row == len(self.form.fields) - 1)
        down.clicked.connect(on_down)
        layout.addWidget(down)

        if self.unlocked:
            delete = QPushButton()
            delete.setIcon(QIcon(':/icons/delete.png'))
            delete.clicked.connect(on_delete)
            layout.addWidget(delete)

        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.table.setCellWidget(row, self.ACTIONS, actions)

    @_block_signals
    def _swap_rows(self, a, b):
        cols = self.ui.table.columnCount()
        for col in range(cols):
            item = self.ui.table.takeItem(a, col)
            self.ui.table.setItem(a, col, self.ui.table.takeItem(b, col))
            self.ui.table.setItem(b, col, item)

        self.form.fields[a], self.form.fields[b] = self.form.fields[
            b], self.form.fields[a]

        self.ui.table.removeCellWidget(a, self.LINK_TYPE)
        self.ui.table.removeCellWidget(b, self.LINK_TYPE)

        if self.form.fields[a]._tag_name == 'linkedField':
            self._add_link_type(a, self.form.fields[a])
        if self.form.fields[b]._tag_name == 'linkedField':
            self._add_link_type(b, self.form.fields[b])
        if self.unlocked:
            self._add_table_column(a)
            self._add_table_column(b)
        self._add_actions(a)
        self._add_actions(b)

    def _on_cell_changed(self, row, col):
        cb = self.COLUMNS_CB.get(col, None)
        if cb is not None:
            state = self.ui.table.item(row, col).checkState()
            setattr(self.form.fields[row], cb, bool(state))
            return
        attr = self.COLUMNS.get(col, None)
        if attr is not None:
            value = self.ui.table.item(row, col).text()
            setattr(self.form.fields[row], attr, value)
        if col == self.GROUP or col == 0:
            self._update_groups()

    def _update_groups(self):
        groups = {}
        for i in range(self.ui.table.rowCount()):
            group = self.ui.table.item(i, self.GROUP).text()
            if not self.unlocked:
                row_name = self.ui.table.item(i, 0).text()
            else:
                row_name = self.ui.table.cellWidget(i, 0).currentText()
            try:
                groups[group].append(row_name)
            except KeyError:
                groups[group] = [row_name]

        self.form.groups = FormGroups(
            [
                FormGroup(legend=group, rows=RowNames(rows))
                for group, rows in groups.items()
            ]
        )

    def _on_add(self):
        field = SimpleField(text='New Field')
        self._on_add_field(field)

    def _on_add_linked(self):
        field = LinkedField(text='New Linked Field')
        self._on_add_field(field)

    def _on_add_field(self, field):
        self.form.fields.append(field)
        self._update_groups()
        index = len(self.form.fields) - 1
        self.ui.table.setRowCount(index + 1)
        self._set_row(index, field)
        self._add_actions(index - 1)
