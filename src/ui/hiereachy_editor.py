import logging
import os

from PyQt5.QtWidgets import QFileDialog, QMainWindow, QSplitter

from api.system import HierachyManager
from ui.hierarchy import HierachyTree
from ui.ui_compiled.hirerachy_edtior import Ui_HierarchyEditor

from .statusbar_handler import StatusBarHandler

__all__ = ['HierachyEditor']


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
        self.ui.main_splitter.setSizes([1, 3])

    def _connect_ui(self):
        self.ui.action_open.triggered.connect(self._on_action_open)
        self.ui.action_save.triggered.connect(self._on_action_save)
        self.ui.action_exit.triggered.connect(self._on_action_exit)
        self.ui.tree.order_updated.connect(self._on_tree_order_updated)

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

    def _on_action_save(self):
        self._mgr.save()

    def _on_action_exit(self):
        pass  # TODO
