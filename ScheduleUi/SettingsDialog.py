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
import Ui_SettingsDialog
import MainWindow
import os


class SettingsDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui=Ui_SettingsDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.connect(self.ui.buttonBox, QtCore.SIGNAL("accepted()"), self.doSave)
        self.connect(self.ui.browseButton, QtCore.SIGNAL("clicked()"), self.browseDir)
        self.connect(self.ui.browseBinaryButton, QtCore.SIGNAL("clicked()"), self.browseBinaryDir)
        self.fgdata_path=''
        self.fgviewer_path=''
        self.move_flpl=''
        home=os.getenv('HOME')
        if home!=None:
            try:
                os.stat(os.path.join(home,'.aisched'))
            except:
                shutil.copy(os.path.join(os.getcwd(),'settings'), os.path.join(home,'.aisched'))
            f_settings=open(os.path.join(home,'.aisched'),'rb')
        else:
            f_settings=open(os.path.join(os.getcwd(),'settings'),'rb')
        settings=f_settings.readlines()
        f_settings.close()
        for line in settings:
            if line.find('fgdata_path=')!=-1:
                tmp=line.split('=')
                path=tmp[1].rstrip('\n')
                path=path.lstrip()
                self.fgdata_path=path.rstrip()
            if line.find('fgviewer_path=')!=-1:
                tmp=line.split('=')
                viewer_path=tmp[1].rstrip('\n')
                viewer_path=viewer_path.lstrip()
                self.fgviewer_path=viewer_path.rstrip()
            if line.find('move_flightplans=')!=-1:
                tmp=line.split('=')
                move=tmp[1].rstrip('\n')
                move=move.lstrip()
                self.move_flpl=move.rstrip()
        self.ui.pathEdit.setText(self.fgdata_path)
        self.ui.binaryPathEdit.setText(self.fgviewer_path)
        if self.move_flpl=='true':
            self.ui.moveCheckBox.setChecked(True)
        else:
            self.ui.moveCheckBox.setChecked(False)
    
    
    def browseDir(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,"FGDATA directory",  os.getcwd(), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        if dir==None or len(dir)==0 or dir=='':
            return 
        else:
            self.ui.pathEdit.setText(dir)
    
    
    def browseBinaryDir(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,"FGViewer directory",  os.getcwd(), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        if dir==None or len(dir)==0 or dir=='':
            return 
        else:
            self.ui.binaryPathEdit.setText(dir)
    
    
    def doSave(self):
        dir=str(self.ui.pathEdit.text())
        binary_dir=str(self.ui.binaryPathEdit.text())
        move=self.ui.moveCheckBox.isChecked()
        if move==True:
            move='true'
        else:
            move='false'
        if dir==None or dir=='':
            print 'No FGDATA directory specified'
            return
        home=os.getenv('HOME')
        if home!=None:
            try:
                os.stat(os.path.join(home,'.aisched'))
            except:
                shutil.copy(os.path.join(os.getcwd(),'settings'), os.path.join(home,'.aisched'))
            f_settings=open(os.path.join(home,'.aisched'),'rb')
        else:
            f_settings=open(os.path.join(os.getcwd(),'settings'),'rb')
        settings=f_settings.readlines()
        f_settings.close()
        buf=''
        add=0
        binary_add=0
        mv=0
        for line in settings:
            if line.find('fgdata_path=')!=-1:
                line='fgdata_path='+dir+'\n'
                add=1
            if line.find('fgviewer_path=')!=-1:
                line='fgviewer_path='+binary_dir+'\n'
                binary_add=1
            if line.find('move_flightplans=')!=-1:
                line='move_flightplans='+move+'\n'
                mv=1
            buf=buf+line
        if add==0:
            buf=buf+'fgdata_path='+dir+'\n'
        if binary_add==0:
            buf=buf+'fgviewer_path='+binary_dir+'\n'
        if mv==0:
            buf=buf+'move_flightplans='+move+'\n'
        home=os.getenv('HOME')
        if home!=None:
            try:
                os.stat(os.path.join(home,'.aisched'))
            except:
                shutil.copy(os.path.join(os.getcwd(),'settings'), os.path.join(home,'.aisched'))
            fw=open(os.path.join(home,'.aisched'),'wb')
        else:
            fw=open(os.path.join(os.getcwd(),'settings'),'wb')
        fw.write(buf)
        fw.close()
        self.close()
