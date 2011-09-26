# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adrian/python/fg-ai-flightplan/ScheduleViewer/ScheduleUi/HelpDialog.ui'
#
# Created: Mon Sep 26 14:38:16 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(836, 604)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/system-help.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Form.setWindowIcon(icon)
        self.textBrowser = QtGui.QTextBrowser(Form)
        self.textBrowser.setGeometry(QtCore.QRect(20, 30, 796, 506))
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName("textBrowser")
        self.closeButton = QtGui.QPushButton(Form)
        self.closeButton.setGeometry(QtCore.QRect(715, 565, 97, 24))
        self.closeButton.setDefault(True)
        self.closeButton.setObjectName("closeButton")

        self.retranslateUi(Form)
        QtCore.QObject.connect(self.closeButton, QtCore.SIGNAL("clicked()"), Form.close)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "ScheduleViewer Help", None, QtGui.QApplication.UnicodeUTF8))
        self.closeButton.setText(QtGui.QApplication.translate("Form", "Close", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

