from PyQt5.QtWidgets import QMainWindow

from ermaket.ui.ui_compiled.main import Ui_MainWindow

__all__ = ['MainWindow']


class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
