# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/hierarchy/table_columns.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TableColumns(object):
    def setupUi(self, TableColumns):
        TableColumns.setObjectName("TableColumns")
        TableColumns.resize(776, 467)
        self.verticalLayout = QtWidgets.QVBoxLayout(TableColumns)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.add_button = QtWidgets.QPushButton(TableColumns)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.add_linked_button = QtWidgets.QPushButton(TableColumns)
        self.add_linked_button.setObjectName("add_linked_button")
        self.horizontalLayout.addWidget(self.add_linked_button)
        self.unlock_button = QtWidgets.QPushButton(TableColumns)
        self.unlock_button.setObjectName("unlock_button")
        self.horizontalLayout.addWidget(self.unlock_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(TableColumns)
        self.table.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.table.setObjectName("table")
        self.table.setColumnCount(9)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(8, item)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setDefaultSectionSize(90)
        self.table.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(TableColumns)
        QtCore.QMetaObject.connectSlotsByName(TableColumns)

    def retranslateUi(self, TableColumns):
        _translate = QtCore.QCoreApplication.translate
        TableColumns.setWindowTitle(
            _translate("TableColumns", "Table Columns")
        )
        self.add_button.setText(_translate("TableColumns", "Add column"))
        self.add_linked_button.setText(
            _translate("TableColumns", "Add linked column")
        )
        self.unlock_button.setText(
            _translate("TableColumns", "Unlock system edit")
        )
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("TableColumns", "Name"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("TableColumns", "Type"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("TableColumns", "Link Type"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("TableColumns", "Text"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("TableColumns", "Sort"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("TableColumns", "Filter"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("TableColumns", "Editable"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("TableColumns", "Visible"))
        item = self.table.horizontalHeaderItem(8)
        item.setText(_translate("TableColumns", "Actions"))
