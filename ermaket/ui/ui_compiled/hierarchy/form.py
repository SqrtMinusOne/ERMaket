# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/hierarchy/form.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FormColumns(object):
    def setupUi(self, FormColumns):
        FormColumns.setObjectName("FormColumns")
        FormColumns.resize(761, 385)
        self.verticalLayout = QtWidgets.QVBoxLayout(FormColumns)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout.addItem(spacerItem)
        self.add_button = QtWidgets.QPushButton(FormColumns)
        self.add_button.setObjectName("add_button")
        self.horizontalLayout.addWidget(self.add_button)
        self.add_linked_button = QtWidgets.QPushButton(FormColumns)
        self.add_linked_button.setObjectName("add_linked_button")
        self.horizontalLayout.addWidget(self.add_linked_button)
        self.unlock_button = QtWidgets.QPushButton(FormColumns)
        self.unlock_button.setObjectName("unlock_button")
        self.horizontalLayout.addWidget(self.unlock_button)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.table = QtWidgets.QTableWidget(FormColumns)
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

        self.retranslateUi(FormColumns)
        QtCore.QMetaObject.connectSlotsByName(FormColumns)

    def retranslateUi(self, FormColumns):
        _translate = QtCore.QCoreApplication.translate
        FormColumns.setWindowTitle(_translate("FormColumns", "Form"))
        self.add_button.setText(_translate("FormColumns", "Add field"))
        self.add_linked_button.setText(
            _translate("FormColumns", "Add linked field")
        )
        self.unlock_button.setText(
            _translate("FormColumns", "Unlock system edit")
        )
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("FormColumns", "Table Column"))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("FormColumns", "Text"))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("FormColumns", "Group"))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("FormColumns", "Link Type"))
        item = self.table.horizontalHeaderItem(4)
        item.setText(_translate("FormColumns", "Editable"))
        item = self.table.horizontalHeaderItem(5)
        item.setText(_translate("FormColumns", "Visible"))
        item = self.table.horizontalHeaderItem(6)
        item.setText(_translate("FormColumns", "Hint"))
        item = self.table.horizontalHeaderItem(7)
        item.setText(_translate("FormColumns", "Help"))
        item = self.table.horizontalHeaderItem(8)
        item.setText(_translate("FormColumns", "Actions"))
