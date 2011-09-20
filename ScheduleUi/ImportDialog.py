# -*-python-*- ScheduleViewer - Copyright (C) 2011 Adrian Musceac
#
# This file is part of ScheduleViewer
#
# ScheduleViewer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# ScheduleViewer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with ScheduleViewer.  If not, see <http://www.gnu.org/licenses/>.
#


from PyQt4 import QtCore, QtGui
import Ui_ImportDialog
import MainWindow
import os


class ImportDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui=Ui_ImportDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.doImport)
        self.connect(self.ui.browseButton, QtCore.SIGNAL("clicked()"), self.browseDir)
    
    
    def browseDir(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,"Import from Directory",  os.getcwd(), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        if dir==None or len(dir)==0 or dir=='':
            return 
        else:
            self.ui.pathEdit.setText(dir)
    
    
    def doImport(self):
        dir=str(self.ui.pathEdit.text())
        if dir==None or dir=='':
            print 'Import: No files specified'
            return
        recurse=str(self.ui.recurseEdit.text())
        if recurse =='' or recurse==None:
            recurse=0
        else:
            recurse=int(recurse)
        self.emit(QtCore.SIGNAL('start_import'), dir, recurse)
        self.close()
