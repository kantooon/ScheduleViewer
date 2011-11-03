# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adrian/python/fg-ai-flightplan/ScheduleViewer/ScheduleUi/HubsDialog.ui'
#
# Created: Thu Nov  3 19:16:57 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/application-x-siag.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 250, 351, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.hboxlayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName("hboxlayout")
        spacerItem = QtGui.QSpacerItem(131, 31, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.hboxlayout.addItem(spacerItem)
        self.okButton = QtGui.QPushButton(self.layoutWidget)
        self.okButton.setObjectName("okButton")
        self.hboxlayout.addWidget(self.okButton)
        self.hubsTableWidget = QtGui.QTableWidget(Dialog)
        self.hubsTableWidget.setGeometry(QtCore.QRect(10, 10, 371, 226))
        self.hubsTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.hubsTableWidget.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.hubsTableWidget.setAlternatingRowColors(True)
        self.hubsTableWidget.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.hubsTableWidget.setObjectName("hubsTableWidget")
        self.hubsTableWidget.setColumnCount(2)
        self.hubsTableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.hubsTableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.hubsTableWidget.setHorizontalHeaderItem(1, item)
        self.hubsTableWidget.horizontalHeader().setDefaultSectionSize(150)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Airline hubs", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "&OK", None, QtGui.QApplication.UnicodeUTF8))
        self.hubsTableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Dialog", "Airport", None, QtGui.QApplication.UnicodeUTF8))
        self.hubsTableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Dialog", "Number of flights", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

