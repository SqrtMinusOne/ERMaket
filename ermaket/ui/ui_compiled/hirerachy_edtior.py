# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/hirerachy_edtior.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_HierarchyEditor(object):
    def setupUi(self, HierarchyEditor):
        HierarchyEditor.setObjectName("HierarchyEditor")
        HierarchyEditor.resize(1066, 739)
        self.centralwidget = QtWidgets.QWidget(HierarchyEditor)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.main_tab_widget = QtWidgets.QTabWidget(self.centralwidget)
        self.main_tab_widget.setObjectName("main_tab_widget")
        self.tab_settings = QtWidgets.QWidget()
        self.tab_settings.setObjectName("tab_settings")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.tab_settings)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout()
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.common_group_box = QtWidgets.QGroupBox(self.tab_settings)
        self.common_group_box.setObjectName("common_group_box")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.common_group_box)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.common_group_box)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.display_name_edit = QtWidgets.QLineEdit(self.common_group_box)
        self.display_name_edit.setObjectName("display_name_edit")
        self.verticalLayout_3.addWidget(self.display_name_edit)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.common_group_box)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.id_spin_box = QtWidgets.QSpinBox(self.common_group_box)
        self.id_spin_box.setEnabled(True)
        self.id_spin_box.setReadOnly(True)
        self.id_spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.id_spin_box.setObjectName("id_spin_box")
        self.verticalLayout.addWidget(self.id_spin_box)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.common_group_box)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.icon_edit = QtWidgets.QLineEdit(self.common_group_box)
        self.icon_edit.setObjectName("icon_edit")
        self.verticalLayout_2.addWidget(self.icon_edit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout_10.addWidget(self.common_group_box)
        self.table_db_box = QtWidgets.QGroupBox(self.tab_settings)
        self.table_db_box.setObjectName("table_db_box")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.table_db_box)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.table_db_box)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_6.addWidget(self.label_7)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.schema_edit = QtWidgets.QLineEdit(self.table_db_box)
        self.schema_edit.setEnabled(False)
        self.schema_edit.setObjectName("schema_edit")
        self.horizontalLayout_6.addWidget(self.schema_edit)
        self.unlock_schema_button = QtWidgets.QPushButton(self.table_db_box)
        self.unlock_schema_button.setObjectName("unlock_schema_button")
        self.horizontalLayout_6.addWidget(self.unlock_schema_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_6)
        self.label_8 = QtWidgets.QLabel(self.table_db_box)
        self.label_8.setObjectName("label_8")
        self.verticalLayout_6.addWidget(self.label_8)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.tablename_edit = QtWidgets.QLineEdit(self.table_db_box)
        self.tablename_edit.setEnabled(False)
        self.tablename_edit.setObjectName("tablename_edit")
        self.horizontalLayout_7.addWidget(self.tablename_edit)
        self.unlock_tablename_button = QtWidgets.QPushButton(self.table_db_box)
        self.unlock_tablename_button.setObjectName("unlock_tablename_button")
        self.horizontalLayout_7.addWidget(self.unlock_tablename_button)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.hidden_checkbox = QtWidgets.QCheckBox(self.table_db_box)
        self.hidden_checkbox.setObjectName("hidden_checkbox")
        self.verticalLayout_6.addWidget(self.hidden_checkbox)
        self.verticalLayout_10.addWidget(self.table_db_box)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_10.addItem(spacerItem)
        self.horizontalLayout_4.addLayout(self.verticalLayout_10)
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.nothing_box = QtWidgets.QGroupBox(self.tab_settings)
        self.nothing_box.setObjectName("nothing_box")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.nothing_box)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.label_9 = QtWidgets.QLabel(self.nothing_box)
        self.label_9.setObjectName("label_9")
        self.verticalLayout_11.addWidget(self.label_9)
        self.verticalLayout_8.addWidget(self.nothing_box)
        self.page_group_box = QtWidgets.QGroupBox(self.tab_settings)
        self.page_group_box.setEnabled(True)
        self.page_group_box.setObjectName("page_group_box")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.page_group_box)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.add_card_checkbox = QtWidgets.QCheckBox(self.page_group_box)
        self.add_card_checkbox.setObjectName("add_card_checkbox")
        self.verticalLayout_4.addWidget(self.add_card_checkbox)
        self.label_4 = QtWidgets.QLabel(self.page_group_box)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.page_name_edit = QtWidgets.QLineEdit(self.page_group_box)
        self.page_name_edit.setObjectName("page_name_edit")
        self.verticalLayout_4.addWidget(self.page_name_edit)
        self.verticalLayout_8.addWidget(self.page_group_box)
        self.prebuilt_page_box = QtWidgets.QGroupBox(self.tab_settings)
        self.prebuilt_page_box.setObjectName("prebuilt_page_box")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.prebuilt_page_box)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.prebuilt_page_box)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_5.addWidget(self.label_5)
        self.page_type_combobox = QtWidgets.QComboBox(self.prebuilt_page_box)
        self.page_type_combobox.setObjectName("page_type_combobox")
        self.verticalLayout_5.addWidget(self.page_type_combobox)
        self.verticalLayout_8.addWidget(self.prebuilt_page_box)
        self.table_display_box = QtWidgets.QGroupBox(self.tab_settings)
        self.table_display_box.setObjectName("table_display_box")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.table_display_box)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.pagination_checkbox = QtWidgets.QCheckBox(self.table_display_box)
        self.pagination_checkbox.setChecked(True)
        self.pagination_checkbox.setObjectName("pagination_checkbox")
        self.verticalLayout_7.addWidget(self.pagination_checkbox)
        self.label_6 = QtWidgets.QLabel(self.table_display_box)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_7.addWidget(self.label_6)
        self.lines_on_page_spinbox = QtWidgets.QSpinBox(self.table_display_box)
        self.lines_on_page_spinbox.setMinimum(1)
        self.lines_on_page_spinbox.setMaximum(1000)
        self.lines_on_page_spinbox.setProperty("value", 20)
        self.lines_on_page_spinbox.setObjectName("lines_on_page_spinbox")
        self.verticalLayout_7.addWidget(self.lines_on_page_spinbox)
        self.columns_button = QtWidgets.QPushButton(self.table_display_box)
        self.columns_button.setObjectName("columns_button")
        self.verticalLayout_7.addWidget(self.columns_button)
        self.edit_table_form_button = QtWidgets.QPushButton(
            self.table_display_box
        )
        self.edit_table_form_button.setObjectName("edit_table_form_button")
        self.verticalLayout_7.addWidget(self.edit_table_form_button)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.display_button = QtWidgets.QPushButton(self.table_display_box)
        self.display_button.setObjectName("display_button")
        self.horizontalLayout_3.addWidget(self.display_button)
        self.default_sort_button = QtWidgets.QPushButton(
            self.table_display_box
        )
        self.default_sort_button.setObjectName("default_sort_button")
        self.horizontalLayout_3.addWidget(self.default_sort_button)
        self.verticalLayout_7.addLayout(self.horizontalLayout_3)
        self.verticalLayout_8.addWidget(self.table_display_box)
        self.form_box = QtWidgets.QGroupBox(self.tab_settings)
        self.form_box.setObjectName("form_box")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.form_box)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.edit_form_button = QtWidgets.QPushButton(self.form_box)
        self.edit_form_button.setObjectName("edit_form_button")
        self.verticalLayout_9.addWidget(self.edit_form_button)
        self.verticalLayout_8.addWidget(self.form_box)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding
        )
        self.verticalLayout_8.addItem(spacerItem1)
        self.horizontalLayout_4.addLayout(self.verticalLayout_8)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 1)
        self.main_tab_widget.addTab(self.tab_settings, "")
        self.tab_columns = QtWidgets.QWidget()
        self.tab_columns.setEnabled(True)
        self.tab_columns.setObjectName("tab_columns")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.tab_columns)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.table_columns_layout = QtWidgets.QVBoxLayout()
        self.table_columns_layout.setObjectName("table_columns_layout")
        self.verticalLayout_13.addLayout(self.table_columns_layout)
        self.main_tab_widget.addTab(self.tab_columns, "")
        self.tab_form = QtWidgets.QWidget()
        self.tab_form.setObjectName("tab_form")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.tab_form)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.form_layout = QtWidgets.QVBoxLayout()
        self.form_layout.setObjectName("form_layout")
        self.horizontalLayout_8.addLayout(self.form_layout)
        self.main_tab_widget.addTab(self.tab_form, "")
        self.tab_access = QtWidgets.QWidget()
        self.tab_access.setObjectName("tab_access")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.tab_access)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.inherit_check_box = QtWidgets.QCheckBox(self.tab_access)
        self.inherit_check_box.setObjectName("inherit_check_box")
        self.horizontalLayout_5.addWidget(self.inherit_check_box)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum
        )
        self.horizontalLayout_5.addItem(spacerItem2)
        self.add_access_button = QtWidgets.QPushButton(self.tab_access)
        self.add_access_button.setObjectName("add_access_button")
        self.horizontalLayout_5.addWidget(self.add_access_button)
        self.verticalLayout_12.addLayout(self.horizontalLayout_5)
        self.access_layout = QtWidgets.QHBoxLayout()
        self.access_layout.setObjectName("access_layout")
        self.verticalLayout_12.addLayout(self.access_layout)
        self.main_tab_widget.addTab(self.tab_access, "")
        self.tab_scripts = QtWidgets.QWidget()
        self.tab_scripts.setObjectName("tab_scripts")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.tab_scripts)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.triggers_layout = QtWidgets.QVBoxLayout()
        self.triggers_layout.setObjectName("triggers_layout")
        self.verticalLayout_14.addLayout(self.triggers_layout)
        self.main_tab_widget.addTab(self.tab_scripts, "")
        self.tab_buttons = QtWidgets.QWidget()
        self.tab_buttons.setObjectName("tab_buttons")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.tab_buttons)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.button_layout = QtWidgets.QVBoxLayout()
        self.button_layout.setObjectName("button_layout")
        self.verticalLayout_15.addLayout(self.button_layout)
        self.main_tab_widget.addTab(self.tab_buttons, "")
        self.horizontalLayout.addWidget(self.main_tab_widget)
        HierarchyEditor.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(HierarchyEditor)
        self.statusbar.setObjectName("statusbar")
        HierarchyEditor.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(HierarchyEditor)
        self.toolBar.setObjectName("toolBar")
        HierarchyEditor.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.menubar = QtWidgets.QMenuBar(HierarchyEditor)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1066, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuHierarchy = QtWidgets.QMenu(self.menubar)
        self.menuHierarchy.setObjectName("menuHierarchy")
        HierarchyEditor.setMenuBar(self.menubar)
        self.action_open = QtWidgets.QAction(HierarchyEditor)
        icon = QtGui.QIcon()
        icon.addPixmap(
            QtGui.QPixmap(":/icons/open.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_open.setIcon(icon)
        self.action_open.setObjectName("action_open")
        self.action_save = QtWidgets.QAction(HierarchyEditor)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(
            QtGui.QPixmap(":/icons/save.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_save.setIcon(icon1)
        self.action_save.setObjectName("action_save")
        self.action_exit = QtWidgets.QAction(HierarchyEditor)
        self.action_exit.setObjectName("action_exit")
        self.action_save_as = QtWidgets.QAction(HierarchyEditor)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(
            QtGui.QPixmap(":/icons/save_as.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_save_as.setIcon(icon2)
        self.action_save_as.setObjectName("action_save_as")
        self.action_merge = QtWidgets.QAction(HierarchyEditor)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(
            QtGui.QPixmap(":/icons/merge.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_merge.setIcon(icon3)
        self.action_merge.setObjectName("action_merge")
        self.action_drop_schema = QtWidgets.QAction(HierarchyEditor)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(
            QtGui.QPixmap(":/icons/drop_schema.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_drop_schema.setIcon(icon4)
        self.action_drop_schema.setObjectName("action_drop_schema")
        self.action_clear = QtWidgets.QAction(HierarchyEditor)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(
            QtGui.QPixmap(":/icons/clear.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_clear.setIcon(icon5)
        self.action_clear.setObjectName("action_clear")
        self.action_new_section = QtWidgets.QAction(HierarchyEditor)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(
            QtGui.QPixmap(":/icons/entry.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_new_section.setIcon(icon6)
        self.action_new_section.setObjectName("action_new_section")
        self.action_new_table = QtWidgets.QAction(HierarchyEditor)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(
            QtGui.QPixmap(":/icons/table.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_new_table.setIcon(icon7)
        self.action_new_table.setObjectName("action_new_table")
        self.action_new_page = QtWidgets.QAction(HierarchyEditor)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(
            QtGui.QPixmap(":/icons/page.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_new_page.setIcon(icon8)
        self.action_new_page.setObjectName("action_new_page")
        self.action_new_prebuilt_page = QtWidgets.QAction(HierarchyEditor)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(
            QtGui.QPixmap(":/icons/prebuiltPage.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_new_prebuilt_page.setIcon(icon9)
        self.action_new_prebuilt_page.setObjectName("action_new_prebuilt_page")
        self.action_delete_current = QtWidgets.QAction(HierarchyEditor)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(
            QtGui.QPixmap(":/icons/delete.png"), QtGui.QIcon.Normal,
            QtGui.QIcon.Off
        )
        self.action_delete_current.setIcon(icon10)
        self.action_delete_current.setObjectName("action_delete_current")
        self.toolBar.addAction(self.action_open)
        self.toolBar.addAction(self.action_save)
        self.toolBar.addAction(self.action_merge)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_delete_current)
        self.toolBar.addAction(self.action_drop_schema)
        self.toolBar.addAction(self.action_clear)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_new_section)
        self.toolBar.addAction(self.action_new_table)
        self.toolBar.addAction(self.action_new_page)
        self.toolBar.addAction(self.action_new_prebuilt_page)
        self.menuFile.addAction(self.action_open)
        self.menuFile.addAction(self.action_save)
        self.menuFile.addAction(self.action_save_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.action_exit)
        self.menuHierarchy.addAction(self.action_merge)
        self.menuHierarchy.addSeparator()
        self.menuHierarchy.addAction(self.action_delete_current)
        self.menuHierarchy.addAction(self.action_drop_schema)
        self.menuHierarchy.addAction(self.action_clear)
        self.menuHierarchy.addSeparator()
        self.menuHierarchy.addAction(self.action_new_section)
        self.menuHierarchy.addAction(self.action_new_table)
        self.menuHierarchy.addAction(self.action_new_page)
        self.menuHierarchy.addAction(self.action_new_prebuilt_page)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHierarchy.menuAction())

        self.retranslateUi(HierarchyEditor)
        self.main_tab_widget.setCurrentIndex(0)
        self.pagination_checkbox.toggled['bool'].connect(
            self.lines_on_page_spinbox.setEnabled
        )
        QtCore.QMetaObject.connectSlotsByName(HierarchyEditor)

    def retranslateUi(self, HierarchyEditor):
        _translate = QtCore.QCoreApplication.translate
        HierarchyEditor.setWindowTitle(
            _translate("HierarchyEditor", "Hierarchy Editor")
        )
        self.common_group_box.setTitle(_translate("HierarchyEditor", "Common"))
        self.label_3.setText(_translate("HierarchyEditor", "Dsiplay name"))
        self.label.setText(_translate("HierarchyEditor", "Id"))
        self.label_2.setText(_translate("HierarchyEditor", "Icon class"))
        self.icon_edit.setPlaceholderText(
            _translate("HierarchyEditor", "Default icon")
        )
        self.table_db_box.setTitle(
            _translate("HierarchyEditor", "Table database settings")
        )
        self.label_7.setText(_translate("HierarchyEditor", "Schema"))
        self.unlock_schema_button.setToolTip(
            _translate(
                "HierarchyEditor",
                "This property shouldn\'t be edited unless it is absolutely necessary"
            )
        )
        self.unlock_schema_button.setText(
            _translate("HierarchyEditor", "Unlock")
        )
        self.label_8.setText(_translate("HierarchyEditor", "Table name"))
        self.unlock_tablename_button.setToolTip(
            _translate(
                "HierarchyEditor",
                "This property shouldn\'t be edited unless it is absolutely necessary"
            )
        )
        self.unlock_tablename_button.setText(
            _translate("HierarchyEditor", "Unlock")
        )
        self.hidden_checkbox.setText(_translate("HierarchyEditor", "Hidden"))
        self.nothing_box.setTitle(_translate("HierarchyEditor", "Information"))
        self.label_9.setText(
            _translate(
                "HierarchyEditor",
                "<html><head/><body><p align=\"center\">Select an element from the<br/>tree to start editing</p></body></html>"
            )
        )
        self.page_group_box.setTitle(
            _translate("HierarchyEditor", "User Page")
        )
        self.add_card_checkbox.setText(
            _translate("HierarchyEditor", "Add a card")
        )
        self.label_4.setText(_translate("HierarchyEditor", "Component name"))
        self.prebuilt_page_box.setTitle(
            _translate("HierarchyEditor", "Prebuilt Page")
        )
        self.label_5.setText(_translate("HierarchyEditor", "Type"))
        self.table_display_box.setTitle(
            _translate("HierarchyEditor", "Table display settings")
        )
        self.pagination_checkbox.setText(
            _translate("HierarchyEditor", "Pagination")
        )
        self.label_6.setText(_translate("HierarchyEditor", "Lines on page"))
        self.columns_button.setText(
            _translate("HierarchyEditor", "Edit columns")
        )
        self.edit_table_form_button.setText(
            _translate("HierarchyEditor", "Edit form")
        )
        self.display_button.setText(
            _translate("HierarchyEditor", "Display override...")
        )
        self.default_sort_button.setText(
            _translate("HierarchyEditor", "Default sort...")
        )
        self.form_box.setTitle(_translate("HierarchyEditor", "Form"))
        self.edit_form_button.setText(
            _translate("HierarchyEditor", "Edit form...")
        )
        self.main_tab_widget.setTabText(
            self.main_tab_widget.indexOf(self.tab_settings),
            _translate("HierarchyEditor", "Settings")
        )
        self.main_tab_widget.setTabText(
            self.main_tab_widget.indexOf(self.tab_columns),
            _translate("HierarchyEditor", "Table Columns")
        )
        self.main_tab_widget.setTabText(
            self.main_tab_widget.indexOf(self.tab_form),
            _translate("HierarchyEditor", "Form")
        )
        self.inherit_check_box.setText(
            _translate("HierarchyEditor", "Inherit rights")
        )
        self.add_access_button.setText(_translate("HierarchyEditor", "Add"))
        self.main_tab_widget.setTabText(
            self.main_tab_widget.indexOf(self.tab_access),
            _translate("HierarchyEditor", "Access")
        )
        self.main_tab_widget.setTabText(
            self.main_tab_widget.indexOf(self.tab_scripts),
            _translate("HierarchyEditor", "Triggers")
        )
        self.main_tab_widget.setTabText(
            self.main_tab_widget.indexOf(self.tab_buttons),
            _translate("HierarchyEditor", "Buttons")
        )
        self.toolBar.setWindowTitle(_translate("HierarchyEditor", "toolBar"))
        self.menuFile.setTitle(_translate("HierarchyEditor", "File"))
        self.menuHierarchy.setTitle(_translate("HierarchyEditor", "Hierarchy"))
        self.action_open.setText(_translate("HierarchyEditor", "Open"))
        self.action_save.setText(_translate("HierarchyEditor", "Save"))
        self.action_exit.setText(_translate("HierarchyEditor", "Exit"))
        self.action_save_as.setText(
            _translate("HierarchyEditor", "Save as...")
        )
        self.action_merge.setText(_translate("HierarchyEditor", "Merge"))
        self.action_merge.setToolTip(_translate("HierarchyEditor", "Merge..."))
        self.action_drop_schema.setText(
            _translate("HierarchyEditor", "Drop Schema")
        )
        self.action_clear.setText(_translate("HierarchyEditor", "Clear"))
        self.action_new_section.setText(
            _translate("HierarchyEditor", "New Section")
        )
        self.action_new_table.setText(
            _translate("HierarchyEditor", "New Table")
        )
        self.action_new_page.setText(
            _translate("HierarchyEditor", "New User Page")
        )
        self.action_new_prebuilt_page.setText(
            _translate("HierarchyEditor", "New Prebuilt Page")
        )
        self.action_delete_current.setText(
            _translate("HierarchyEditor", "Delete Current")
        )


from ermaket.ui.res_compiled import icons_rc
