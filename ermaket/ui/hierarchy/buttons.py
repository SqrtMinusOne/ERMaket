from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QComboBox, QHBoxLayout, QHeaderView, QPushButton, QTableWidgetItem, QWidget
)

from ermaket.api.system.hierarchy import Button, Buttons, Location, SystemAction
from ermaket.api.system.hierarchy.scripts import _locations
from ermaket.ui.ui_compiled.hierarchy.buttons import Ui_ButtonsTable

__all__ = ['ButtonTable']


class ButtonTable(QWidget):
    COLUMNS = {0: 'text', 2: 'icon', 4: 'tooltip'}
    LOCATION = 1
    VARIANT = 3
    SCRIPT_ID = 5
    SYSTEM_ACTION = 6
    ACTIONS = 7

    VARIANTS = [
        'primary', 'secondary', 'success', 'danger', 'warning', 'info',
        'light', 'dark', 'outline-primary', 'outline-secondary',
        'outline-success', 'outline-danger', 'outline-warning', 'outline-info',
        'outline-light', 'outline-dark', 'link'
    ]

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent=None)
        self.ui = Ui_ButtonsTable()
        self.ui.setupUi(self)
        self.ui.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )

        self._scripts = None
        self.ui.table.setEnabled(False)
        self.ui.add_button.setEnabled(False)
        self._connect_ui()

    def _block_signals(func):
        def decorate(self, *args, **kwargs):
            self.ui.table.blockSignals(True)
            res = func(self, *args, **kwargs)
            self.ui.table.blockSignals(False)
            return res

        return decorate

    def set_elem(self, elem):
        self.elem = elem
        if self.elem._tag_name == 'section':
            self.ui.table.setEnabled(False)
            self.ui.add_button.setEnabled(False)
        else:
            self.ui.table.setEnabled(True)
            self.ui.add_button.setEnabled(True)
        self._locations = [
            *_locations['all'], *_locations.get(elem._tag_name, [])
        ]
        self._set_rows()

    def set_scripts(self, scripts):
        self._scripts = scripts
        self._set_rows()

    def _connect_ui(self):
        self.ui.add_button.clicked.connect(self._on_add)
        self.ui.table.cellChanged.connect(self._on_cell_changed)

    @_block_signals
    def _set_rows(self):
        self.ui.table.setRowCount(0)
        if self.elem.buttonList is None:
            return
        self.ui.table.setRowCount(len(self.elem.buttonList))
        for row, button in enumerate(self.elem.buttonList):
            self._set_row(row, button)

    @_block_signals
    def _set_row(self, row, button):
        for col, attr, in self.COLUMNS.items():
            item = QTableWidgetItem(getattr(button, attr))
            self.ui.table.setItem(row, col, item)

        self._add_location(row)
        self._add_variant(row)
        self._add_action(row)
        self._add_actions(row)

    def _add_location(self, row):
        def on_current_text_changed(text):
            self.elem.buttonList[row].location = Location(text)

        combobox = QComboBox()
        combobox.addItems([str(loc) for loc in self._locations])
        combobox.setCurrentText(str(self.elem.buttonList[row].location))
        combobox.currentTextChanged.connect(on_current_text_changed)
        self.ui.table.setCellWidget(row, self.LOCATION, combobox)

    def _add_variant(self, row):
        def on_current_text_changed(text):
            self.elem.buttonList[row].variant = text

        combobox = QComboBox()
        combobox.addItems(self.VARIANTS)
        combobox.setCurrentText(self.elem.buttonList[row].variant)
        combobox.currentTextChanged.connect(on_current_text_changed)
        self.ui.table.setCellWidget(row, self.VARIANT, combobox)

    def _add_action(self, row):
        def on_current_text_changed(text):
            if text == "":
                item = QTableWidgetItem()
            else:
                self.elem.buttonList[row].scriptId = None
                self.elem.buttonList[row].action = SystemAction(text)
                item = QTableWidgetItem()
                item.setFlags(Qt.NoItemFlags)
            self.ui.table.setItem(row, self.SCRIPT_ID, item)

        action_combobox = QComboBox()
        action_combobox.addItems(
            ["", *[str(item) for item in SystemAction.items.values()]]
        )
        button = self.elem.buttonList[row]
        if button.action:
            action_combobox.setCurrentText(str(button.action))
            item = QTableWidgetItem()
            item.setFlags(Qt.NoItemFlags)
        else:
            if button.scriptId is None:
                button.scriptId = 0
            item = QTableWidgetItem(str(button.scriptId))
            action_combobox.setEnabled(False)
        action_combobox.currentTextChanged.connect(on_current_text_changed)
        self.ui.table.setItem(row, self.SCRIPT_ID, item)
        self.ui.table.setCellWidget(row, self.SYSTEM_ACTION, action_combobox)

    def _add_actions(self, row):
        def on_up():
            self._swap_rows(row, row - 1)

        def on_down():
            self._swap_rows(row, row + 1)

        def on_delete():
            self.ui.table.removeRow(row)
            del self.elem.buttonList[row]
            for i in range(self.ui.table.rowCount()):
                self._add_actions(row)
            if len(self.elem.buttonList) == 0:
                self.elem.buttonList = None

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
        down.setDisabled(row == len(self.elem.buttonList) - 1)
        down.clicked.connect(on_down)
        layout.addWidget(down)

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

        self.elem.buttonList[a], self.elem.buttonList[
            b] = self.elem.buttonList[b], self.elem.buttonList[a]

        for i in [a, b]:
            self._add_location(i)
            self._add_variant(i)
            self._add_action(i)
            self._add_actions(i)

    def _on_cell_changed(self, row, col):
        attr = self.COLUMNS.get(col, None)
        if attr is not None:
            value = self.ui.table.item(row, col).text()
            setattr(self.elem.buttonList[row], attr, value)

        if col == self.SCRIPT_ID:
            script_id = self.ui.table.item(row, col).text()
            if script_id == "":
                self.ui.table.cellWidget(row,
                                         self.SYSTEM_ACTION).setEnabled(True)
            else:
                try:
                    script_id = int(script_id)
                    self.elem.buttonList[row].scriptId = script_id
                    self.elem.buttonList[row].action = None
                    w = self.ui.table.cellWidget(row, self.SYSTEM_ACTION)
                    w.setEnabled(False)
                except ValueError:
                    self.ui.table.item(row, col).setText(
                        str(self.elem.buttonList[row].scriptId)
                    )

    def _on_add(self):
        if self.elem.buttonList is None:
            self.elem.buttonList = Buttons()
        button = Button(
            text='New button',
            location=self._locations[0],
            variant=self.VARIANTS[0]
        )
        index = len(self.elem.buttonList)
        self.elem.buttonList.append(button)
        self.ui.table.setRowCount(index + 1)
        self._set_row(index, button)
        self._add_actions(index - 1)
