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
import Ui_MainWindow, Messages
#, AboutDialog, HelpDialog
from Logic.database_thread import DatabaseThread
import os, io, time

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)

        self.databaseThread=DatabaseThread()
        self.startDBThread()
        self.page=0

        self.connect(self.ui.actionImport, QtCore.SIGNAL("triggered()"), self.showImportDialog)
        #self.connect(self.ui.actionExport, QtCore.SIGNAL("triggered()"), self.showExportDialog)
        #self.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.showAboutDialog)
        #self.connect(self.ui.actionHelp, QtCore.SIGNAL("triggered()"), self.showHelpDialog)
        self.connect(self.ui.showButton, QtCore.SIGNAL("clicked()"), self.sendQuery)
        self.connect(self.ui.clearButton, QtCore.SIGNAL("clicked()"), self.clearFlights)


    
    def showImportDialog(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,"Open Directory",  os.getcwd(), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        if len(dir)==0 or dir=='':
            return
        self.emit(QtCore.SIGNAL('import'), str(dir))


    """
    def showAboutDialog(self):
        self.aboutDialog=AboutDialog.AboutDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.aboutDialog, QtCore.SLOT('close()'))
    
    
    def showHelpDialog(self):
        self.helpDialog=HelpDialog.HelpDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.helpDialog, QtCore.SLOT('close()'))
    """
 
    def startDBThread(self):
        #self.databaseThread.setTable('flights')
        self.databaseThread.start()
        
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results"), self.updateFlights, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("show_total_nr"), self.showNrFlights, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('message_success'), self.popMessage, QtCore.Qt.QueuedConnection)

        self.connect(self, QtCore.SIGNAL('import'), self.databaseThread.importConfs, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('nr_flights'), self.databaseThread.getNrFlights, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('export'), self.databaseThread.exportConfs, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query'), self.databaseThread.runQuery, QtCore.Qt.QueuedConnection)
        
        self.emit(QtCore.SIGNAL('nr_flights'))
  

    def popMessage(self, type, message): 
        
        self.messageBox=Messages.MessageBox()
        self.messageBox.setMessage(type, message)
        self.messageBox.show()
    
    
    def showNrFlights(self, nr):
        self.ui.labelTotalFlights.setText(nr)
    
    
    def sendQuery(self):
        param_list=[]
        if self.ui.callsignEdit.text()!='':
            param_list.append(('callsign', str(self.ui.callsignEdit.text())))
        if self.ui.depAirportEdit.text()!='':
            param_list.append(('dep_airport', str(self.ui.depAirportEdit.text()).upper()))
        if self.ui.depTimeEdit.text()!='':
            param_list.append(('dep_time', str(self.ui.depTimeEdit.text())))
        if self.ui.depDayEdit.text()!='':
            param_list.append(('dep_day', str(self.ui.depDayEdit.text())))
        if self.ui.acTypeEdit.text()!='':
            param_list.append(('ac_type', str(self.ui.acTypeEdit.text()).upper()))
        if self.ui.airlineEdit.text()!='':
            param_list.append(('airline', str(self.ui.airlineEdit.text()).upper()))
        if self.ui.arrAirportEdit.text()!='':
            param_list.append(('arr_airport', str(self.ui.arrAirportEdit.text()).upper()))
        if self.ui.arrTimeEdit.text()!='':
            param_list.append(('arr_time', str(self.ui.arrTimeEdit.text())))
        
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query'), parameters)
    
    
    def updateFlights(self, flightlist):
        
        if flightlist==None:
            self.popMessage('Error', 'No results found')
            return
        nr_flights=len(flightlist)
        if nr_flights==0:
            self.popMessage('Error', 'No results found')
        self.ui.labelSelectedFlights.setText(str(nr_flights))
        self.clearFlights()
        table=self.ui.tableWidget
        table.setRowCount(nr_flights)
        r=0
        for flight in flightlist:
            
            callsign=QtGui.QTableWidgetItem(str(flight[1]), 0)
            callsign.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            flt_rules=QtGui.QTableWidgetItem(str(flight[2]), 0)
            flt_rules.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            dep_day=QtGui.QTableWidgetItem(str(flight[3]), 0)
            dep_day.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            dep_airport=QtGui.QTableWidgetItem(str(flight[4]), 0)
            dep_airport.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            arr_airport=QtGui.QTableWidgetItem(str(flight[5]), 0)
            arr_airport.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            dep_time=QtGui.QTableWidgetItem(str(flight[6]), 0)
            dep_time.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            arr_time=QtGui.QTableWidgetItem(str(flight[7]), 0)
            arr_time.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            ac_type=QtGui.QTableWidgetItem(str(flight[8]), 0)
            ac_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            flt_level=QtGui.QTableWidgetItem(str(flight[9]), 0)
            flt_level.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            table.setItem(r, 0, callsign)
            table.setItem(r, 1, flt_rules)
            table.setItem(r, 6, dep_day)
            table.setItem(r, 2, dep_airport)
            table.setItem(r, 3, arr_airport)
            table.setItem(r, 4, dep_time)
            table.setItem(r, 5, arr_time)
            table.setItem(r, 7, ac_type)
            table.setItem(r, 8, flt_level)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            r=r+1
    
    
    def clearFlights(self):
        self.page=0
        table=self.ui.tableWidget
        #table.clear()
        table.setRowCount(0)
    
    
