# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adrian/python/fg-ai-flightplan/ScheduleViewer/ScheduleUi/MainWindow.ui'
#
# Created: Thu Sep 22 17:12:22 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1070, 740)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/main.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(5, 15, 1061, 651))
        self.tabWidget.setObjectName("tabWidget")
        self.flightsTab = QtGui.QWidget()
        self.flightsTab.setObjectName("flightsTab")
        self.tableWidget = QtGui.QTableWidget(self.flightsTab)
        self.tableWidget.setGeometry(QtCore.QRect(5, 180, 1041, 431))
        self.tableWidget.setMinimumSize(QtCore.QSize(840, 291))
        self.tableWidget.setMaximumSize(QtCore.QSize(1200, 436))
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(9, item)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(100)
        self.tableWidget.verticalHeader().setVisible(False)
        self.groupBox = QtGui.QGroupBox(self.flightsTab)
        self.groupBox.setGeometry(QtCore.QRect(5, 5, 1041, 176))
        self.groupBox.setObjectName("groupBox")
        self.gridLayoutWidget = QtGui.QWidget(self.groupBox)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 30, 991, 91))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.callsignEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.callsignEdit.setObjectName("callsignEdit")
        self.gridLayout.addWidget(self.callsignEdit, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.depAirportEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.depAirportEdit.setObjectName("depAirportEdit")
        self.gridLayout.addWidget(self.depAirportEdit, 0, 3, 1, 1)
        self.label_3 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        self.depTimeEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.depTimeEdit.setObjectName("depTimeEdit")
        self.gridLayout.addWidget(self.depTimeEdit, 0, 5, 1, 1)
        self.label_4 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 0, 6, 1, 1)
        self.depDayEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.depDayEdit.setObjectName("depDayEdit")
        self.gridLayout.addWidget(self.depDayEdit, 0, 7, 1, 1)
        self.label_5 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 0, 8, 1, 1)
        self.acTypeEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.acTypeEdit.setObjectName("acTypeEdit")
        self.gridLayout.addWidget(self.acTypeEdit, 0, 9, 1, 1)
        self.arrTimeEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.arrTimeEdit.setObjectName("arrTimeEdit")
        self.gridLayout.addWidget(self.arrTimeEdit, 1, 5, 1, 1)
        self.label_7 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 1, 4, 1, 1)
        self.arrAirportEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.arrAirportEdit.setObjectName("arrAirportEdit")
        self.gridLayout.addWidget(self.arrAirportEdit, 1, 3, 1, 1)
        self.label_6 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 1, 0, 1, 1)
        self.airlineEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.airlineEdit.setObjectName("airlineEdit")
        self.gridLayout.addWidget(self.airlineEdit, 1, 1, 1, 1)
        self.showButton = QtGui.QPushButton(self.gridLayoutWidget)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/dialog-ok-apply.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showButton.setIcon(icon1)
        self.showButton.setAutoDefault(False)
        self.showButton.setDefault(True)
        self.showButton.setObjectName("showButton")
        self.gridLayout.addWidget(self.showButton, 1, 7, 1, 1)
        self.clearButton = QtGui.QPushButton(self.gridLayoutWidget)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icons/icons/user-busy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon2)
        self.clearButton.setObjectName("clearButton")
        self.gridLayout.addWidget(self.clearButton, 1, 9, 1, 1)
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBox)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(525, 126, 476, 46))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.horizontalLayout = QtGui.QHBoxLayout(self.verticalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.editButton = QtGui.QPushButton(self.verticalLayoutWidget)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icons/icons/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon3)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        self.deleteButton = QtGui.QPushButton(self.verticalLayoutWidget)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/icons/icons/application-exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon4)
        self.deleteButton.setObjectName("deleteButton")
        self.horizontalLayout.addWidget(self.deleteButton)
        self.truncateButton = QtGui.QPushButton(self.verticalLayoutWidget)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/icons/icons/system-reboot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.truncateButton.setIcon(icon5)
        self.truncateButton.setObjectName("truncateButton")
        self.horizontalLayout.addWidget(self.truncateButton)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(10, 125, 116, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(10, 150, 106, 16))
        self.label_10.setObjectName("label_10")
        self.labelTotalFlights = QtGui.QLabel(self.groupBox)
        self.labelTotalFlights.setGeometry(QtCore.QRect(140, 125, 56, 15))
        self.labelTotalFlights.setText("")
        self.labelTotalFlights.setObjectName("labelTotalFlights")
        self.labelSelectedFlights = QtGui.QLabel(self.groupBox)
        self.labelSelectedFlights.setGeometry(QtCore.QRect(140, 150, 66, 16))
        self.labelSelectedFlights.setText("")
        self.labelSelectedFlights.setObjectName("labelSelectedFlights")
        self.tabWidget.addTab(self.flightsTab, "")
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        self.tabWidget.addTab(self.tab, "")
        self.aircraftTab = QtGui.QWidget()
        self.aircraftTab.setObjectName("aircraftTab")
        self.tabWidget.addTab(self.aircraftTab, "")
        self.progressBar = QtGui.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(False)
        self.progressBar.setGeometry(QtCore.QRect(10, 670, 1051, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1070, 21))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtGui.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionImport = QtGui.QAction(MainWindow)
        self.actionImport.setObjectName("actionImport")
        self.actionExport = QtGui.QAction(MainWindow)
        self.actionExport.setObjectName("actionExport")
        self.actionQuit = QtGui.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionHelp = QtGui.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionImport_fleet = QtGui.QAction(MainWindow)
        self.actionImport_fleet.setObjectName("actionImport_fleet")
        self.actionImport_aircraft = QtGui.QAction(MainWindow)
        self.actionImport_aircraft.setObjectName("actionImport_aircraft")
        self.actionExport_fleet = QtGui.QAction(MainWindow)
        self.actionExport_fleet.setObjectName("actionExport_fleet")
        self.actionExport_aircraft = QtGui.QAction(MainWindow)
        self.actionExport_aircraft.setObjectName("actionExport_aircraft")
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuFile.addAction(self.actionImport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_fleet)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionImport_aircraft)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_fleet)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExport_aircraft)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionQuit)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.actionQuit, QtCore.SIGNAL("activated()"), MainWindow.close)
        QtCore.QObject.connect(self.callsignEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.arrAirportEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.acTypeEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.airlineEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.arrTimeEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.depAirportEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.depDayEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QObject.connect(self.depTimeEdit, QtCore.SIGNAL("returnPressed()"), self.showButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Flightgear AI schedule manager", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setSortingEnabled(True)
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("MainWindow", "Callsign", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("MainWindow", "Flight rules", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("MainWindow", "Dep. airport", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("MainWindow", "Arr. airport", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(4).setText(QtGui.QApplication.translate("MainWindow", "Dep. time", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(5).setText(QtGui.QApplication.translate("MainWindow", "Arr. time", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(6).setText(QtGui.QApplication.translate("MainWindow", "Dep. day", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(7).setText(QtGui.QApplication.translate("MainWindow", "Aircraft type", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(8).setText(QtGui.QApplication.translate("MainWindow", "Flt. level", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(9).setText(QtGui.QApplication.translate("MainWindow", "id", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("MainWindow", "Filters", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Callsign", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Dep. airport", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Dep. time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", "Dep. day", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("MainWindow", "Ac. type", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("MainWindow", "Arr. time", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("MainWindow", "Arr. airport", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("MainWindow", "Airline", None, QtGui.QApplication.UnicodeUTF8))
        self.showButton.setText(QtGui.QApplication.translate("MainWindow", "Show", None, QtGui.QApplication.UnicodeUTF8))
        self.clearButton.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.editButton.setText(QtGui.QApplication.translate("MainWindow", "Edit flight", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteButton.setText(QtGui.QApplication.translate("MainWindow", "Delete flights", None, QtGui.QApplication.UnicodeUTF8))
        self.truncateButton.setText(QtGui.QApplication.translate("MainWindow", "Empty database", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("MainWindow", "Total nr. of flights:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("MainWindow", "Selected flights:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.flightsTab), QtGui.QApplication.translate("MainWindow", "Flights", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "Fleet", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aircraftTab), QtGui.QApplication.translate("MainWindow", "Aircraft", None, QtGui.QApplication.UnicodeUTF8))
        self.menuEdit.setTitle(QtGui.QApplication.translate("MainWindow", "Edit", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setText(QtGui.QApplication.translate("MainWindow", "&Import schedules...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "&Export schedules...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setText(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHelp.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+H", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "A&bout", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+B", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_fleet.setText(QtGui.QApplication.translate("MainWindow", "Import &fleet...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionImport_aircraft.setText(QtGui.QApplication.translate("MainWindow", "Import &aircraft...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_fleet.setText(QtGui.QApplication.translate("MainWindow", "Export fleet", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_aircraft.setText(QtGui.QApplication.translate("MainWindow", "Export aircraft", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

