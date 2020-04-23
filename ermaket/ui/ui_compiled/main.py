# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/pavel/Programming/ERMaket_Experiment/src/ui/ui_source/main.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(671, 489)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.mainTabWidget.setObjectName("mainTabWidget")
        self.mainTab = QtWidgets.QWidget()
        self.mainTab.setObjectName("mainTab")
        self.groupBox = QtWidgets.QGroupBox(self.mainTab)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 301, 331))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(0, 30, 121, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 121, 16))
        self.label_2.setObjectName("label_2")
        self.configPathLineEdiit = QtWidgets.QLineEdit(self.groupBox)
        self.configPathLineEdiit.setGeometry(QtCore.QRect(10, 100, 163, 24))
        self.configPathLineEdiit.setReadOnly(True)
        self.configPathLineEdiit.setObjectName("configPathLineEdiit")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 191, 16))
        self.label_3.setObjectName("label_3")
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setGeometry(QtCore.QRect(10, 50, 251, 26))
        self.widget.setObjectName("widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pathLineEdiit = QtWidgets.QLineEdit(self.widget)
        self.pathLineEdiit.setReadOnly(True)
        self.pathLineEdiit.setObjectName("pathLineEdiit")
        self.horizontalLayout_2.addWidget(self.pathLineEdiit)
        self.openButton = QtWidgets.QPushButton(self.widget)
        self.openButton.setObjectName("openButton")
        self.horizontalLayout_2.addWidget(self.openButton)
        self.widget1 = QtWidgets.QWidget(self.groupBox)
        self.widget1.setGeometry(QtCore.QRect(10, 150, 251, 26))
        self.widget1.setObjectName("widget1")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.widget1)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.hierarchyPathLineEdiit = QtWidgets.QLineEdit(self.widget1)
        self.hierarchyPathLineEdiit.setReadOnly(True)
        self.hierarchyPathLineEdiit.setObjectName("hierarchyPathLineEdiit")
        self.horizontalLayout_3.addWidget(self.hierarchyPathLineEdiit)
        self.pushButton = QtWidgets.QPushButton(self.widget1)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.mainTabWidget.addTab(self.mainTab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.mainTabWidget.addTab(self.tab_2, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.mainTabWidget.addTab(self.tab, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.mainTabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.mainTabWidget.addTab(self.tab_4, "")
        self.horizontalLayout.addWidget(self.mainTabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 671, 21))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.menu.addAction(self.actionExit)
        self.menubar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.mainTabWidget.setCurrentIndex(0)
        self.actionExit.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Application"))
        self.label.setText(_translate("MainWindow", "Path to src/"))
        self.label_2.setText(_translate("MainWindow", "Path to config.json"))
        self.label_3.setText(
            _translate("MainWindow", "Path to the hierarchy file")
        )
        self.openButton.setText(_translate("MainWindow", "Open"))
        self.pushButton.setText(_translate("MainWindow", "Open"))
        self.mainTabWidget.setTabText(
            self.mainTabWidget.indexOf(self.mainTab),
            _translate("MainWindow", "Main")
        )
        self.mainTabWidget.setTabText(
            self.mainTabWidget.indexOf(self.tab_2),
            _translate("MainWindow", "Database")
        )
        self.mainTabWidget.setTabText(
            self.mainTabWidget.indexOf(self.tab),
            _translate("MainWindow", "Hierarchy")
        )
        self.mainTabWidget.setTabText(
            self.mainTabWidget.indexOf(self.tab_3),
            _translate("MainWindow", "ERD")
        )
        self.mainTabWidget.setTabText(
            self.mainTabWidget.indexOf(self.tab_4),
            _translate("MainWindow", "Scripts")
        )
        self.menu.setTitle(_translate("MainWindow", "File"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
