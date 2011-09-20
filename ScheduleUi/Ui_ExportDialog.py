# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/adrian/python/fg-ai-flightplan/ScheduleViewer/ScheduleUi/ExportDialog.ui'
#
# Created: Tue Sep 20 13:36:47 2011
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(508, 356)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/document-edit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setModal(True)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(135, 305, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayoutWidget = QtGui.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 40, 476, 246))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtGui.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.pathEdit = QtGui.QLineEdit(self.gridLayoutWidget)
        self.pathEdit.setReadOnly(True)
        self.pathEdit.setObjectName("pathEdit")
        self.gridLayout.addWidget(self.pathEdit, 0, 1, 1, 1)
        self.browseButton = QtGui.QPushButton(self.gridLayoutWidget)
        self.browseButton.setObjectName("browseButton")
        self.gridLayout.addWidget(self.browseButton, 0, 2, 1, 1)
        self.airlinesCheckBox = QtGui.QCheckBox(self.gridLayoutWidget)
        self.airlinesCheckBox.setChecked(True)
        self.airlinesCheckBox.setObjectName("airlinesCheckBox")
        self.gridLayout.addWidget(self.airlinesCheckBox, 1, 0, 1, 1)
        self.selectedRadioButton = QtGui.QRadioButton(self.gridLayoutWidget)
        self.selectedRadioButton.setObjectName("selectedRadioButton")
        self.gridLayout.addWidget(self.selectedRadioButton, 2, 1, 1, 1)
        self.allRadioButton = QtGui.QRadioButton(self.gridLayoutWidget)
        self.allRadioButton.setChecked(True)
        self.allRadioButton.setObjectName("allRadioButton")
        self.gridLayout.addWidget(self.allRadioButton, 2, 0, 1, 1)
        self.databaseRadioButton = QtGui.QRadioButton(self.gridLayoutWidget)
        self.databaseRadioButton.setObjectName("databaseRadioButton")
        self.gridLayout.addWidget(self.databaseRadioButton, 2, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Export schedules in conf format", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Export directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("Dialog", "Browse...", None, QtGui.QApplication.UnicodeUTF8))
        self.airlinesCheckBox.setText(QtGui.QApplication.translate("Dialog", "Separate airline files", None, QtGui.QApplication.UnicodeUTF8))
        self.selectedRadioButton.setText(QtGui.QApplication.translate("Dialog", "Selected flights only", None, QtGui.QApplication.UnicodeUTF8))
        self.allRadioButton.setText(QtGui.QApplication.translate("Dialog", "All flights in view", None, QtGui.QApplication.UnicodeUTF8))
        self.databaseRadioButton.setText(QtGui.QApplication.translate("Dialog", "All flights in database", None, QtGui.QApplication.UnicodeUTF8))

import resources_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Dialog = QtGui.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

