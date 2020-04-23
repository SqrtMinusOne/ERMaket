# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/hierarchy/triggers.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TriggersTable(object):
    def setupUi(self, TriggersTable):
        TriggersTable.setObjectName("TriggersTable")
        TriggersTable.resize(460, 353)
        self.verticalLayout = QtWidgets.QVBoxLayout(TriggersTable)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.add_button = QtWidgets.QPushButton(TriggersTable)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(TriggersTable)
        self.table.setObjectName("table")
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        self.verticalLayout.addWidget(self.table)

        self.retranslateUi(TriggersTable)
        QtCore.QMetaObject.connectSlotsByName(TriggersTable)

    def retranslateUi(self, TriggersTable):
        _translate = QtCore.QCoreApplication.translate
        TriggersTable.setWindowTitle(_translate("TriggersTable", "Form"))
        self.add_button.setText(_translate("TriggersTable", "Add"))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("TriggersTable", "Activation"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("TriggersTable", "Script Id"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("TriggersTable", "Actions"))
