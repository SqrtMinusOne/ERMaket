import copy

from PyQt5.QtWidgets import QDialog

from ui.ui_compiled.hierarchy.column_dialog import Ui_ColumnDialog

__all__ = ['ColumnDialog']


class ColumnDialog(QDialog):
    def __init__(self, columns, row, parent=None):
        super(ColumnDialog, self).__init__(parent)
        self.ui = Ui_ColumnDialog()
        self.ui.setupUi(self)
        self.column = copy.deepcopy(columns[row])
        self._columns = columns
        self._row = row
