# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adrian/python/fg-ai-flightplan/ScheduleViewer/ScheduleUi/AboutDialog.ui'
#
# Created: Mon Sep 26 14:38:17 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(398, 348)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/dialog-information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        self.tabWidget = QtGui.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(5, 10, 391, 286))
        self.tabWidget.setObjectName("tabWidget")
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        self.aboutTextEdit = QtGui.QTextEdit(self.tab1)
        self.aboutTextEdit.setGeometry(QtCore.QRect(0, 0, 381, 256))
        self.aboutTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.aboutTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.aboutTextEdit.setObjectName("aboutTextEdit")
        self.tabWidget.addTab(self.tab1, "")
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName("tab2")
        self.thanksTextEdit = QtGui.QTextEdit(self.tab2)
        self.thanksTextEdit.setGeometry(QtCore.QRect(0, 0, 381, 256))
        self.thanksTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.thanksTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.thanksTextEdit.setObjectName("thanksTextEdit")
        self.tabWidget.addTab(self.tab2, "")
        self.tab3 = QtGui.QWidget()
        self.tab3.setObjectName("tab3")
        self.licenseTextEdit = QtGui.QTextEdit(self.tab3)
        self.licenseTextEdit.setGeometry(QtCore.QRect(0, 0, 381, 256))
        self.licenseTextEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.licenseTextEdit.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.licenseTextEdit.setObjectName("licenseTextEdit")
        self.tabWidget.addTab(self.tab3, "")
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setGeometry(QtCore.QRect(150, 310, 97, 24))
        self.okButton.setObjectName("okButton")

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.okButton, QtCore.SIGNAL("clicked()"), Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "About ScheduleViewer", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QtGui.QApplication.translate("Dialog", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), QtGui.QApplication.translate("Dialog", "Authors and thanks", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab3), QtGui.QApplication.translate("Dialog", "License Agreement", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "OK", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

