# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/hierarchy/buttons.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ButtonsTable(object):
    def setupUi(self, ButtonsTable):
        ButtonsTable.setObjectName("ButtonsTable")
        ButtonsTable.resize(737, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(ButtonsTable)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.add_button = QtWidgets.QPushButton(ButtonsTable)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(ButtonsTable)
        self.table.setObjectName("table")
        self.table.setColumnCount(8)
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
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(ButtonsTable)
        QtCore.QMetaObject.connectSlotsByName(ButtonsTable)

    def retranslateUi(self, ButtonsTable):
        _translate = QtCore.QCoreApplication.translate
        ButtonsTable.setWindowTitle(_translate("ButtonsTable", "Form"))
        self.add_button.setText(_translate("ButtonsTable", "Add"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("ButtonsTable", "Text"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("ButtonsTable", "Location"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("ButtonsTable", "Icon"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("ButtonsTable", "Variant"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("ButtonsTable", "Tooltip"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("ButtonsTable", "Script Id"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("ButtonsTable", "System Action"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("ButtonsTable", "Actions"))
