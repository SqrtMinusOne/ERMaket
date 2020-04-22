import copy

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QDialog

from api.system import HierachyManager
from api.system.hierarchy import (DefaultSort, DisplayColumn, DisplayColumns,
                                  SortColumn, SortOrder)
from api.system.hierarchy.table import _link_type_multiple, _link_type_singular
from ui.ui_compiled.hierarchy.column_dialog import Ui_ColumnDialog

__all__ = ['ColumnDialog']


class ColumnDialog(QDialog):
    saved = pyqtSignal()

    LOCKED = [
        'name_edit', 'type_edit', 'db_properties_box', 'link_db_mapping_box',
        'link_properties_box'
    ]
    LINK_DISABLED = [
        'type_edit', 'default_edit', 'default_sort_combobox', 'sort_checkbox',
        'filter_checkbox', 'pk_checkbox', 'auto_inc_checkbox'
    ]
    MODEL = {
        'line':
            {
                'rowName': 'name_edit',
                'type': 'type_edit',
                'text': 'text_edit',
                'default': 'default_edit',
            },
        'checkbox':
            {
                'isPk': 'pk_checkbox',
                'isRequired': 'required_checkbox',
                'isSort': 'sort_checkbox',
                'isFilter': 'filter_checkbox',
                'isEditable': 'editable_checkbox',
                'isUnique': 'unique_checkbox',
                'isVisible': 'visible_checkbox',
                'isAuto': 'auto_inc_checkbox'
            },
        'combobox': {}
    }
    LINKED_MODEL = {
        'line': {
            'linkName': 'link_name_edit',
            'fkName': 'fk_name_edit'
        },
        'checkbox':
            {
                'isMultiple': 'multiple_checkbox',
                'linkMultiple': 'link_multiple_checkbox',
                'linkRequired': 'link_required_checkbox'
            },
        'combobox':
            {
                'linkType': 'link_combo_box',
                'linkSchema': 'target_link_schema_combobox',
                'linkTableName': 'link_table_name_combobox'
            }
    }

    def __init__(self, elem, row, parent=None):
        super(ColumnDialog, self).__init__(parent)
        self.ui = Ui_ColumnDialog()
        self.ui.setupUi(self)
        self._old_elem = elem
        self._elem = copy.deepcopy(elem)
        self.column = self._elem.columns[row]
        self._row = row
        self._mgr = HierachyManager()

        self._setup_ui()
        self._connect_ui()

    def _setup_ui(self):
        if self.column._tag_name != 'linkedColumn':
            self.ui.linked_tab.setEnabled(False)
            self.ui.link_combo_box.setEnabled(False)
        else:
            self.ui.default_sort_combobox.setEnabled(False)
            self._on_multiple_changed()

        if self._elem.defaultSort is not None:
            col = next(
                (
                    s for s in self._elem.defaultSort
                    if s.rowName == self.column.rowName
                ), None
            )
            if col is not None:
                self.ui.default_sort_combobox.setCurrentText(str(col.sort))

    def _set_display_column(self):
        display_col = next(
            (
                s for s in self._elem.displayColumns
                if s.rowName == self.column.rowName
            ), None
        )

        if display_col is not None:
            self.ui.display_row_name.setCurrentText(display_col.linkRowName)

    def _connect_ui(self):
        self.ui.unlock_button.clicked.connect(self._unlock_system)
        self._connect_model(self.MODEL)

        if self.column._tag_name == 'linkedColumn':
            self._connect_model(self.LINKED_MODEL)
            self.ui.multiple_checkbox.stateChanged.connect(
                lambda state: self._on_multiple_changed()
            )
            self._set_linked_schemas()
            self._set_linked_tables()
            self._set_display_columns()
            self._set_display_column()
            self.ui.target_link_schema_combobox.currentTextChanged.connect(
                lambda text: self._set_linked_tables()
            )
            self.ui.target_link_schema_combobox.currentTextChanged.connect(
                lambda text: self._set_display_columns()
            )
            self.ui.link_table_name_combobox.currentTextChanged.connect(
                lambda text: self._set_display_columns()
            )

        self.ui.default_sort_combobox.currentTextChanged.connect(
            self._on_default_sort_changed
        )
        self.ui.display_row_name.currentTextChanged.connect(
            self._on_display_column_changed
        )
        self.ui.cancel_button.clicked.connect(self._on_cancel)
        self.ui.ok_button.clicked.connect(self._on_ok)

    def _on_multiple_changed(self):
        self.ui.link_combo_box.clear()
        if self.column.isMultiple:
            self.ui.link_combo_box.addItems(
                [str(val) for val in _link_type_multiple]
            )
            self.ui.sort_checkbox.setCheckState(False)
            self.ui.sort_checkbox.setEnabled(False)
            self.ui.filter_checkbox.setCheckState(False)
            self.ui.filter_checkbox.setEnabled(False)
        else:
            self.ui.link_combo_box.addItems(
                [str(val) for val in _link_type_singular]
            )
            self.ui.sort_checkbox.setEnabled(True)
            self.ui.filter_checkbox.setEnabled(True)

    def _on_default_sort_changed(self, sort):
        if self._elem.defaultSort is None:
            values = []
        else:
            values = [
                sort for sort in self._elem.defaultSort
                if sort.rowName != self.column.rowName
            ]

        if sort == 'asc':
            values.append(
                SortColumn(rowName=self.column.rowName, sort=SortOrder.ASC)
            )
        elif sort == 'desc':
            values.append(
                SortColumn(rowName=self.column.rowName, sort=SortOrder.DESC)
            )
        if len(values) > 0:
            self._elem.defaultSort = DefaultSort(values)
        else:
            self._elem.defaultSort = None

    def _on_display_column_changed(self, column):
        values = [
            col for col in self._elem.displayColumns
            if col.rowName != self.column.rowName
        ]
        if len(column) > 0:
            values.append(
                DisplayColumn(
                    rowName=self.column.rowName,
                    linkRowName=column,
                    isMultiple=self.column.isMultiple
                )
            )
        self._elem.displayColumns = DisplayColumns(values)

    def _connect_model(self, model):
        for attr, elem in model['line'].items():
            self._line_edit_model(attr, elem)

        for attr, elem in model['checkbox'].items():
            self._checkbox_model(attr, elem)

        for attr, elem in model['combobox'].items():
            self._combobox_model(attr, elem)

    def _line_edit_model(self, attr, elem):
        def on_text_changed(text):
            if text == '':
                setattr(self.column, attr, None)
            else:
                setattr(self.column, attr, text)

        elem = getattr(self.ui, elem)
        elem.setText(getattr(self.column, attr))
        elem.textEdited.connect(on_text_changed)

    def _checkbox_model(self, attr, elem):
        def on_state_changed(state):
            setattr(self.column, attr, state != 0)

        elem = getattr(self.ui, elem)
        if getattr(self.column, attr):
            elem.setCheckState(Qt.Checked)
        else:
            elem.setCheckState(Qt.Unchecked)

        elem.stateChanged.connect(on_state_changed)

    def _combobox_model(self, attr, elem):
        cast = type(getattr(self.column, attr))

        def on_current_text_changed(text):
            setattr(self.column, attr, cast(text))

        elem = getattr(self.ui, elem)
        elem.setCurrentText(str(getattr(self.column, attr)))
        elem.currentTextChanged.connect(on_current_text_changed)

    def _set_linked_schemas(self):
        self.ui.target_link_schema_combobox.blockSignals(True)
        schemas = set([table.schema for table in self._mgr.h.tables])
        self.ui.target_link_schema_combobox.clear()
        self.ui.target_link_schema_combobox.addItems(schemas)
        self.ui.target_link_schema_combobox.setCurrentText(self._elem.schema)
        self.ui.target_link_schema_combobox.blockSignals(False)

    def _set_linked_tables(self):
        schema = self.ui.target_link_schema_combobox.currentText()
        tables = set(
            [
                table.tableName
                for table in self._mgr.h.tables if table.schema == schema
            ]
        )
        text = self.ui.link_table_name_combobox.currentText()
        self.ui.link_table_name_combobox.clear()
        self.ui.link_table_name_combobox.addItems(tables)
        self.ui.link_table_name_combobox.setCurrentText(text)

    def _set_display_columns(self):
        self.ui.display_row_name.clear()
        schema = self.ui.target_link_schema_combobox.currentText()
        table_name = self.ui.link_table_name_combobox.currentText()
        table = next(
            (
                t for t in self._mgr.h.tables
                if t.schema == schema and t.tableName == table_name
            ), None
        )
        if table is None:
            return
        self.ui.display_row_name.addItems(
            [
                "", *[
                    column.rowName for column in table.columns
                    if column._tag_name != 'linkedColumn'
                ]
            ]
        )

    def _unlock_system(self):
        [getattr(self.ui, elem).setEnabled(True) for elem in self.LOCKED]
        self.ui.unlock_button.setEnabled(False)

    def _on_cancel(self):
        self.close()

    def _on_ok(self):
        self._old_elem.columns[self._row] = self._elem.columns[self._row]
        self._old_elem.displayColumns = self._elem.displayColumns
        self._old_elem.defaultSort = self._elem.defaultSort
        self.saved.emit()
        self.close()
