# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/hierarchy/column_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ColumnDialog(object):
    def setupUi(self, ColumnDialog):
        ColumnDialog.setObjectName("ColumnDialog")
        ColumnDialog.setWindowModality(QtCore.Qt.WindowModal)
        ColumnDialog.resize(383, 509)
        ColumnDialog.setModal(True)
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(ColumnDialog)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.tabWidget = QtWidgets.QTabWidget(ColumnDialog)
        self.tabWidget.setObjectName("tabWidget")
        self.general_tab = QtWidgets.QWidget()
        self.general_tab.setObjectName("general_tab")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.general_tab)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.groupBox_3 = QtWidgets.QGroupBox(self.general_tab)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(self.groupBox_3)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.name_edit = QtWidgets.QLineEdit(self.groupBox_3)
        self.name_edit.setEnabled(False)
        self.name_edit.setObjectName("name_edit")
        self.verticalLayout_2.addWidget(self.name_edit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.type_edit = QtWidgets.QLineEdit(self.groupBox_3)
        self.type_edit.setEnabled(False)
        self.type_edit.setObjectName("type_edit")
        self.verticalLayout.addWidget(self.type_edit)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_14.addWidget(self.groupBox_3)
        self.groupBox_6 = QtWidgets.QGroupBox(self.general_tab)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_4 = QtWidgets.QLabel(self.groupBox_6)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.text_edit = QtWidgets.QLineEdit(self.groupBox_6)
        self.text_edit.setObjectName("text_edit")
        self.verticalLayout_6.addWidget(self.text_edit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox_6)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.link_combo_box = QtWidgets.QComboBox(self.groupBox_6)
        self.link_combo_box.setObjectName("link_combo_box")
        self.verticalLayout_5.addWidget(self.link_combo_box)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.verticalLayout_9.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout()
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_3 = QtWidgets.QLabel(self.groupBox_6)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_11.addWidget(self.label_3)
        self.default_edit = QtWidgets.QLineEdit(self.groupBox_6)
        self.default_edit.setObjectName("default_edit")
        self.verticalLayout_11.addWidget(self.default_edit)
        self.horizontalLayout_7.addLayout(self.verticalLayout_11)
        self.verticalLayout_12 = QtWidgets.QVBoxLayout()
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_10 = QtWidgets.QLabel(self.groupBox_6)
        self.label_10.setObjectName("label_10")
        self.verticalLayout_12.addWidget(self.label_10)
        self.default_sort_combobox = QtWidgets.QComboBox(self.groupBox_6)
        self.default_sort_combobox.setObjectName("default_sort_combobox")
        self.default_sort_combobox.addItem("")
        self.default_sort_combobox.setItemText(0, "")
        self.default_sort_combobox.addItem("")
        self.default_sort_combobox.addItem("")
        self.verticalLayout_12.addWidget(self.default_sort_combobox)
        self.horizontalLayout_7.addLayout(self.verticalLayout_12)
        self.verticalLayout_9.addLayout(self.horizontalLayout_7)
        self.verticalLayout_14.addWidget(self.groupBox_6)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.general_tab)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.sort_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.sort_checkbox.setObjectName("sort_checkbox")
        self.verticalLayout_3.addWidget(self.sort_checkbox)
        self.filter_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.filter_checkbox.setObjectName("filter_checkbox")
        self.verticalLayout_3.addWidget(self.filter_checkbox)
        self.visible_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.visible_checkbox.setObjectName("visible_checkbox")
        self.verticalLayout_3.addWidget(self.visible_checkbox)
        self.editable_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.editable_checkbox.setObjectName("editable_checkbox")
        self.verticalLayout_3.addWidget(self.editable_checkbox)
        self.horizontalLayout_3.addWidget(self.groupBox)
        self.db_properties_box = QtWidgets.QGroupBox(self.general_tab)
        self.db_properties_box.setEnabled(False)
        self.db_properties_box.setObjectName("db_properties_box")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.db_properties_box)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pk_checkbox = QtWidgets.QCheckBox(self.db_properties_box)
        self.pk_checkbox.setObjectName("pk_checkbox")
        self.verticalLayout_4.addWidget(self.pk_checkbox)
        self.unique_checkbox = QtWidgets.QCheckBox(self.db_properties_box)
        self.unique_checkbox.setObjectName("unique_checkbox")
        self.verticalLayout_4.addWidget(self.unique_checkbox)
        self.required_checkbox = QtWidgets.QCheckBox(self.db_properties_box)
        self.required_checkbox.setObjectName("required_checkbox")
        self.verticalLayout_4.addWidget(self.required_checkbox)
        self.auto_inc_checkbox = QtWidgets.QCheckBox(self.db_properties_box)
        self.auto_inc_checkbox.setObjectName("auto_inc_checkbox")
        self.verticalLayout_4.addWidget(self.auto_inc_checkbox)
        self.horizontalLayout_3.addWidget(self.db_properties_box)
        self.verticalLayout_14.addLayout(self.horizontalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_14.addItem(spacerItem)
        self.tabWidget.addTab(self.general_tab, "")
        self.linked_tab = QtWidgets.QWidget()
        self.linked_tab.setObjectName("linked_tab")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.linked_tab)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.link_db_mapping_box = QtWidgets.QGroupBox(self.linked_tab)
        self.link_db_mapping_box.setEnabled(False)
        self.link_db_mapping_box.setObjectName("link_db_mapping_box")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.link_db_mapping_box)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_6 = QtWidgets.QLabel(self.link_db_mapping_box)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.target_link_schema_combobox = QtWidgets.QComboBox(
            self.link_db_mapping_box
        )
        self.target_link_schema_combobox.setEditable(True)
        self.target_link_schema_combobox.setObjectName(
            "target_link_schema_combobox"
        )
        self.verticalLayout_7.addWidget(self.target_link_schema_combobox)
        self.label_7 = QtWidgets.QLabel(self.link_db_mapping_box)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_7.addWidget(self.label_7)
        self.link_table_name_combobox = QtWidgets.QComboBox(
            self.link_db_mapping_box
        )
        self.link_table_name_combobox.setEditable(True)
        self.link_table_name_combobox.setObjectName("link_table_name_combobox")
        self.verticalLayout_7.addWidget(self.link_table_name_combobox)
        self.label_9 = QtWidgets.QLabel(self.link_db_mapping_box)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_7.addWidget(self.label_9)
        self.link_name_edit = QtWidgets.QLineEdit(self.link_db_mapping_box)
        self.link_name_edit.setObjectName("link_name_edit")
        self.verticalLayout_7.addWidget(self.link_name_edit)
        self.horizontalLayout_4.addWidget(self.link_db_mapping_box)
        self.link_properties_box = QtWidgets.QGroupBox(self.linked_tab)
        self.link_properties_box.setEnabled(False)
        self.link_properties_box.setObjectName("link_properties_box")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.link_properties_box)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_8 = QtWidgets.QLabel(self.link_properties_box)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_8.addWidget(self.label_8)
        self.fk_name_edit = QtWidgets.QLineEdit(self.link_properties_box)
        self.fk_name_edit.setObjectName("fk_name_edit")
        self.verticalLayout_8.addWidget(self.fk_name_edit)
        self.multiple_checkbox = QtWidgets.QCheckBox(self.link_properties_box)
        self.multiple_checkbox.setObjectName("multiple_checkbox")
        self.verticalLayout_8.addWidget(self.multiple_checkbox)
        self.link_multiple_checkbox = QtWidgets.QCheckBox(
            self.link_properties_box
        )
        self.link_multiple_checkbox.setObjectName("link_multiple_checkbox")
        self.verticalLayout_8.addWidget(self.link_multiple_checkbox)
        self.link_required_checkbox = QtWidgets.QCheckBox(
            self.link_properties_box
        )
        self.link_required_checkbox.setObjectName("link_required_checkbox")
        self.verticalLayout_8.addWidget(self.link_required_checkbox)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 10, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_8.addItem(spacerItem1)
        self.horizontalLayout_4.addWidget(self.link_properties_box)
        self.verticalLayout_15.addLayout(self.horizontalLayout_4)
        self.groupBox_7 = QtWidgets.QGroupBox(self.linked_tab)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.label_11 = QtWidgets.QLabel(self.groupBox_7)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_10.addWidget(self.label_11)
        self.display_row_name = QtWidgets.QComboBox(self.groupBox_7)
        self.display_row_name.setEditable(True)
        self.display_row_name.setObjectName("display_row_name")
        self.verticalLayout_10.addWidget(self.display_row_name)
        self.verticalLayout_15.addWidget(self.groupBox_7)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 112, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_15.addItem(spacerItem2)
        self.tabWidget.addTab(self.linked_tab, "")
        self.verticalLayout_13.addWidget(self.tabWidget)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_5.addItem(spacerItem3)
        self.unlock_button = QtWidgets.QPushButton(ColumnDialog)
        self.unlock_button.setObjectName("unlock_button")
        self.horizontalLayout_5.addWidget(self.unlock_button)
        self.cancel_button = QtWidgets.QPushButton(ColumnDialog)
        self.cancel_button.setObjectName("cancel_button")
        self.horizontalLayout_5.addWidget(self.cancel_button)
        self.ok_button = QtWidgets.QPushButton(ColumnDialog)
        self.ok_button.setObjectName("ok_button")
        self.horizontalLayout_5.addWidget(self.ok_button)
        self.verticalLayout_13.addLayout(self.horizontalLayout_5)

        self.retranslateUi(ColumnDialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(ColumnDialog)

    def retranslateUi(self, ColumnDialog):
        _translate = QtCore.QCoreApplication.translate
        ColumnDialog.setWindowTitle(_translate("ColumnDialog", "Edit Column"))
        self.groupBox_3.setTitle(
            _translate("ColumnDialog", "DB Column Mapping")
        )
        self.label.setText(_translate("ColumnDialog", "Name"))
        self.label_2.setText(_translate("ColumnDialog", "Type"))
        self.groupBox_6.setTitle(_translate("ColumnDialog", "Column Settings"))
        self.label_4.setText(_translate("ColumnDialog", "Text"))
        self.label_5.setText(_translate("ColumnDialog", "Link Type"))
        self.label_3.setText(_translate("ColumnDialog", "Default value"))
        self.label_10.setText(_translate("ColumnDialog", "Default sort"))
        self.default_sort_combobox.setItemText(
            1, _translate("ColumnDialog", "asc")
        )
        self.default_sort_combobox.setItemText(
            2, _translate("ColumnDialog", "desc")
        )
        self.groupBox.setTitle(_translate("ColumnDialog", "Display settings"))
        self.sort_checkbox.setText(_translate("ColumnDialog", "Sort enabled"))
        self.filter_checkbox.setText(
            _translate("ColumnDialog", "Filter enabled")
        )
        self.visible_checkbox.setText(_translate("ColumnDialog", "Visible"))
        self.editable_checkbox.setText(_translate("ColumnDialog", "Editable"))
        self.db_properties_box.setTitle(
            _translate("ColumnDialog", "DB Column Properties")
        )
        self.pk_checkbox.setText(_translate("ColumnDialog", "Primary Key"))
        self.unique_checkbox.setText(_translate("ColumnDialog", "Unique"))
        self.required_checkbox.setText(_translate("ColumnDialog", "Required"))
        self.auto_inc_checkbox.setText(
            _translate("ColumnDialog", "Autoincrement")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.general_tab),
            _translate("ColumnDialog", "General")
        )
        self.link_db_mapping_box.setTitle(
            _translate("ColumnDialog", "Link Database Mapping")
        )
        self.label_6.setText(_translate("ColumnDialog", "Target Table Schema"))
        self.label_7.setText(_translate("ColumnDialog", "Target Table Name"))
        self.label_9.setText(_translate("ColumnDialog", "Link Name"))
        self.link_properties_box.setTitle(
            _translate("ColumnDialog", "Link Properties")
        )
        self.label_8.setText(_translate("ColumnDialog", "Foreign Key Column"))
        self.multiple_checkbox.setText(_translate("ColumnDialog", "Multiple"))
        self.link_multiple_checkbox.setText(
            _translate("ColumnDialog", "Other Side Multiple")
        )
        self.link_required_checkbox.setText(
            _translate("ColumnDialog", "Other Side Required")
        )
        self.groupBox_7.setTitle(
            _translate("ColumnDialog", "Link Display Settings")
        )
        self.label_11.setText(
            _translate("ColumnDialog", "Display Column Name")
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.linked_tab),
            _translate("ColumnDialog", "Linked")
        )
        self.unlock_button.setText(
            _translate("ColumnDialog", "Unlock system settings")
        )
        self.cancel_button.setText(_translate("ColumnDialog", "Cancel"))
        self.ok_button.setText(_translate("ColumnDialog", "OK"))