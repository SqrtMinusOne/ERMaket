import logging
import os

from PyQt5.QtWidgets import QFileDialog, QMainWindow

from api.system import HierachyManager
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
        handler = StatusBarHandler(self.ui.statusbar)
        logger.addHandler(handler)
        self._mgr = HierachyManager(save=False)

    def _setup_ui(self):
        self.ui.main_splitter.setSizes([1, 3])

    def _connect_ui(self):
        self.ui.action_open.triggered.connect(self._on_action_open)
        self.ui.action_save.triggered.connect(self._on_action_save)
        self.ui.action_exit.triggered.connect(self._on_action_exit)

    def _on_action_open(self):
        self._filename, _ = QFileDialog.getOpenFileName(
            self, "Open file", os.getcwd(), "XML files (*.xml)"
        )
        self.ui.statusbar.showMessage(self._filename)

    def _on_action_save(self):
        pass  # TODO

    def _on_action_exit(self):
        pass  # TODO
