import logging
import os

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QSplitter

from api.system import HierachyManager
from api.system.hierarchy import PrebuiltPageType
from ui.hierarchy import HierachyTree
from ui.ui_compiled.hirerachy_edtior import Ui_HierarchyEditor

from .statusbar_handler import StatusBarHandler

__all__ = ['HierachyEditor']


def to_check(state):
    if not state:
        return 0
    return 2


def from_check(check):
    return check > 0


class HierachyEditor(QMainWindow):
    def __init__(self, parent=None):
        super(QMainWindow, self).__init__(parent=parent)
        self.ui = Ui_HierarchyEditor()
        self.ui.setupUi(self)
        self._setup_ui()
        self._connect_ui()

        logger = logging.getLogger()
        handler = StatusBarHandler(self.ui.statusbar, timeout=10**4)
        logger.addHandler(handler)
        self._mgr = HierachyManager(save=False)

        self._update_tree()

    def _setup_ui(self):
        self.ui.main_splitter = QSplitter(self)
        self.ui.tree = HierachyTree(self)
        self.ui.main_splitter.addWidget(self.ui.tree)
        self.ui.main_splitter.addWidget(self.ui.main_tab_widget)
        self.setCentralWidget(self.ui.main_splitter)
        self.ui.main_splitter.setSizes([1, 2])
        self.ui.page_type_combobox.insertItems(
            0, PrebuiltPageType.items.values()
        )

        self.ui.common_group_box.setEnabled(False)
        self._hide_boxes()

    def _hide_boxes(self):
        self.ui.table_db_box.setVisible(False)
        self.ui.page_group_box.setVisible(False)
        self.ui.prebuilt_page_box.setVisible(False)
        self.ui.table_display_box.setVisible(False)
        self.ui.form_box.setVisible(False)

    def _connect_ui(self):
        self.ui.action_open.triggered.connect(self._on_action_open)
        self.ui.action_save.triggered.connect(self._on_action_save)
        self.ui.action_exit.triggered.connect(self._on_action_exit)
        self.ui.tree.order_updated.connect(self._on_tree_order_updated)
        self.ui.tree.currentItemChanged.connect(self._on_element_selected)

        self.ui.display_name_edit.textEdited.connect(self._on_name_edited)
        self.ui.icon_edit.textEdited.connect(self._on_icon_edited)
        self.ui.schema_edit.textEdited.connect(
            lambda schema: setattr(self._item.elem, 'schema', schema)
        )
        self.ui.tablename_edit.textEdited.connect(
            lambda name: setattr(self._item.elem, 'tableName', name)
        )
        self.ui.hidden_checkbox.stateChanged.connect(
            lambda state:
            setattr(self._item.elem, 'hidden', from_check(state))
        )
        self.ui.add_card_checkbox.stateChanged.connect(
            lambda state:
            setattr(self._item.elem, 'addCard', from_check(state))
        )
        self.ui.page_name_edit.textEdited.connect(
            lambda name: setattr(self._item.elem, 'pageName', name)
        )
        self.ui.page_type_combobox.currentIndexChanged.connect(
            lambda type:
            setattr(self._item.elem, 'type', PrebuiltPageType(type))
        )
        self.ui.pagination_checkbox.stateChanged.connect(
            lambda state:
            setattr(self._item.elem, 'pagination', from_check(state))
        )
        self.ui.lines_on_page_spinbox.valueChanged.connect(
            lambda value: setattr(self._item.elem, 'linesOnPage', int(value))
        )

    def _on_action_open(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Open file", os.getcwd(), "XML files (*.xml)"
        )
        self._mgr.set_path(filename)
        self._mgr.read(reload=True)
        self._update_tree()

    def _update_tree(self):
        self.ui.tree.set_hirearchy(self._mgr.h)

    def _on_tree_order_updated(self):
        print(self._mgr.h.pretty_xml())

    def _on_element_selected(self, item):
        self._item = item
        self.ui.common_group_box.setEnabled(True)
        self.ui.nothing_box.setVisible(False)
        self._hide_boxes()

        self.ui.id_spin_box.setValue(item.elem.id)
        self.ui.display_name_edit.setText(item.elem.name)
        self.ui.icon_edit.setText(item.elem.overrideIcon)

        if item.elem._tag_name == 'tableEntry':
            self.ui.table_db_box.setVisible(True)
            self.ui.table_display_box.setVisible(True)
            self.ui.schema_edit.setText(item.elem.schema)
            self.ui.tablename_edit.setText(item.elem.tableName)
            self.ui.hidden_checkbox.setCheckState(to_check(item.elem.hidden))
            self.ui.pagination_checkbox.setCheckState(
                to_check(item.elem.pagination)
            )
            self.ui.lines_on_page_spinbox.setValue(item.elem.linesOnPage)
        elif item.elem._tag_name == 'formEntry':
            self.ui.form_box.setVisible(True)
        elif item.elem._tag_name == 'page':
            self.ui.page_group_box.setVisible(True)
            self.ui.add_card_checkbox.setCheckState(to_check(item.addCard))
            self.ui.page_name_edit.setText(item.elem.pageName)
        elif item.elem._tag_name == 'prebuiltPageEntry':
            self.ui.prebuilt_page_box.setVisible(True)
            self.ui.page_type_combobox.setCurrentText(str(item.elem.type))
        else:
            self.ui.nothing_box.setVisible(True)

    def _on_name_edited(self, name):
        self._item.elem.name = name
        self._item.update_ui()

    def _on_icon_edited(self, icon):
        if icon != "":
            self._item.elem.overrideIcon = icon
        else:
            self._item.elem.overrideIcon = None

    def _on_action_save(self):
        self._mgr.save()

    def _on_action_exit(self):
        pass  # TODO
