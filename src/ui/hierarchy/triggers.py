from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QHBoxLayout, QHeaderView, QPushButton,
                             QTableWidgetItem, QWidget)

from api.system.hierarchy import Activation, Trigger, Triggers
from api.system.hierarchy.scripts import _activations
from ui.ui_compiled.hierarchy.triggers import Ui_TriggersTable


class TriggersTable(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.ui = Ui_TriggersTable()
        self.ui.setupUi(self)
        self.ui.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        self._connect_ui()
        self._scripts = None
        self.ui.add_button.setEnabled(False)

    def _connect_ui(self):
        self.ui.add_button.clicked.connect(self._on_add)
        self.ui.table.cellChanged.connect(self._on_cell_changed)

    def set_elem(self, elem):
        self._elem = elem
        self._activations = [
            *_activations["all"], *_activations.get(elem._tag_name, [])
        ]
        self._set_columns()
        self.ui.add_button.setEnabled(True)

    def set_scripts(self, scripts):
        self._scripts = scripts
        self._set_columns()

    def _set_columns(self):
        self.ui.table.setRowCount(0)
        if self._elem.triggerList is None:
            return
        self.ui.table.setRowCount(len(self._elem.triggerList))
        for row in range(len(self._elem.triggerList)):
            self._add_activation(row)
            self._add_scripts(row)
            self._add_actions(row)

    def _add_activation(self, row):
        def on_text_changed(text):
            self._elem.triggerList[row].activation = Activation(text)

        activation = QComboBox()
        activation.addItems([str(item) for item in self._activations])
        activation.setCurrentText(str(self._elem.triggerList[row].activation))
        activation.currentTextChanged.connect(on_text_changed)
        self.ui.table.setCellWidget(row, 0, activation)

    def _add_scripts(self, row):
        def on_text_changed(text):
            self._elem.triggerList[row].scriptId = int(text)

        if self._scripts is None:
            item = QTableWidgetItem()
            item.setText(str(self._elem.triggerList[row].scriptId))
            self.ui.table.setItem(row, 1, item)
        else:
            scripts = QComboBox()
            scripts.addItems([str(script.id) for script in self._scripts])
            scripts.setCurrentText(self._elem.triggerList[row].scriptId)
            scripts.currentTextChanged.connect(on_text_changed)
            self.ui.table.setCellWidget(row, 1, scripts)

    def _add_actions(self, row):
        def on_delete():
            self.ui.table.removeRow(row)
            del self._elem.triggerList[row]
            for i in range(self.ui.table.rowCount()):
                self._add_actions(row)
            if len(self._elem.triggerList) == 0:
                self._elem.triggerList = None

        actions = QWidget()
        layout = QHBoxLayout()
        actions.setLayout(layout)

        delete = QPushButton()
        delete.setIcon(QIcon(':/icons/delete.png'))
        delete.clicked.connect(on_delete)
        layout.addWidget(delete)

        layout.setContentsMargins(0, 0, 0, 0)
        self.ui.table.setCellWidget(row, 2, actions)

    def _on_cell_changed(self, row, col):
        if col == 1:
            script_id = self.ui.table.item(row, col).text()
            try:
                script_id = int(script_id)
            except ValueError:
                self.ui.table.item(row, col).setText(
                    str(self._elem.triggerList[row].scriptId)
                )
                return
            self._elem.triggerList[row].scriptId = script_id

    def _on_add(self):
        if self._elem.triggerList is None:
            self._elem.triggerList = Triggers()
        trigger = Trigger(activation=self._activations[0], scriptId=0)
        self._elem.triggerList.append(trigger)
        index = len(self._elem.triggerList) - 1
        self.ui.table.setRowCount(index + 1)
        self._add_activation(index)
        self._add_scripts(index)
        self._add_actions(index)
