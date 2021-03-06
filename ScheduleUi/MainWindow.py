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
import Ui_MainWindow, Messages,  ImportDialog,  ExportDialog, AboutDialog, HelpDialog,  ConfirmDialog, SettingsDialog, DuplicatesDialog, HubsDialog, AcTypesDialog
from Logic.database_thread import DatabaseThread
from QTableWidgetNumericItem import QTableWidgetNumericItem
import os, io, random, re

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow.Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.progressBar.setVisible(False)
        self.databaseThread=DatabaseThread()
        self.startDBThread()
        self.page=0
        self.flightlist=[]
        self.fleetlist=[]
        self.aircraftlist=[]
        self.flightlist_selected=[]
        self.fleetlist_selected=[]
        self.del_shortcut=QtGui.QShortcut(self.ui.tableWidget)
        self.del_shortcut.setKey(QtGui.QKeySequence(QtGui.QKeySequence.Delete))
        self.del_shortcut.setAutoRepeat(False)
        self.del_shortcut.setContext(QtCore.Qt.WidgetShortcut)
        self.del_fleet_shortcut=QtGui.QShortcut(self.ui.fleetTableWidget)
        self.del_fleet_shortcut.setKey(QtGui.QKeySequence(QtGui.QKeySequence.Delete))
        self.del_fleet_shortcut.setAutoRepeat(False)
        self.del_fleet_shortcut.setContext(QtCore.Qt.WidgetShortcut)
        self.del_aircraft_shortcut=QtGui.QShortcut(self.ui.aircraftTableWidget)
        self.del_aircraft_shortcut.setKey(QtGui.QKeySequence(QtGui.QKeySequence.Delete))
        self.del_aircraft_shortcut.setAutoRepeat(False)
        self.del_aircraft_shortcut.setContext(QtCore.Qt.WidgetShortcut)
        self.prev_aircraft_shortcut=QtGui.QShortcut(self.ui.fleetTableWidget)
        self.prev_aircraft_shortcut.setKey(QtGui.QKeySequence(QtCore.Qt.Key_P))
        self.prev_aircraft_shortcut.setAutoRepeat(False)
        self.prev_aircraft_shortcut.setContext(QtCore.Qt.WidgetShortcut)
    
        ## menu actions
        self.connect(self.ui.actionImport, QtCore.SIGNAL("triggered()"), self.showImportDialog)
        self.connect(self.ui.actionImport_fleet, QtCore.SIGNAL("triggered()"), self.importFleet)
        self.connect(self.ui.actionImport_aircraft, QtCore.SIGNAL("triggered()"), self.importAircraft)
        self.connect(self.ui.actionExport, QtCore.SIGNAL("triggered()"), self.showExportDialog)
        self.connect(self.ui.actionExport_fleet, QtCore.SIGNAL("triggered()"), self.exportFleet)
        self.connect(self.ui.actionExport_aircraft, QtCore.SIGNAL("triggered()"), self.exportAircraft)
        self.connect(self.ui.actionDump_database, QtCore.SIGNAL("triggered()"), self.databaseThread.dumpDatabase, QtCore.Qt.QueuedConnection)
        self.connect(self.ui.actionLoad_database, QtCore.SIGNAL("triggered()"), self.loadDBFromSQL)
        self.connect(self.ui.actionSettings, QtCore.SIGNAL("triggered()"), self.showSettingsDialog)
        self.connect(self.ui.actionAbout, QtCore.SIGNAL("triggered()"), self.showAboutDialog)
        self.connect(self.ui.actionHelp, QtCore.SIGNAL("triggered()"), self.showHelpDialog)
        
        ## flights tab
        self.connect(self.ui.showButton, QtCore.SIGNAL("clicked()"), self.sendQuery)
        self.connect(self.ui.clearButton, QtCore.SIGNAL("clicked()"), self.clearFlights)
        self.connect(self.ui.deleteButton, QtCore.SIGNAL("clicked()"), self.deleteFlights)
        self.connect(self.del_shortcut, QtCore.SIGNAL("activated()"), self.ui.deleteButton, QtCore.SLOT('click()'))
        self.connect(self.ui.truncateButton, QtCore.SIGNAL("clicked()"), self.confirmDeleteFlights)
        self.connect(self.ui.addButton, QtCore.SIGNAL("clicked()"), self.addFlight)
        self.connect(self.ui.findDupesButton, QtCore.SIGNAL("clicked()"), self.confirmFindDupes)
        self.connect(self.ui.deleteDuplicatesButton, QtCore.SIGNAL("clicked()"), self.showDeleteDuplicatesTreshhold)
        self.connect(self.ui.findHubsButton, QtCore.SIGNAL("clicked()"), self.findHubs)
        self.connect(self.ui.findAcTypesButton, QtCore.SIGNAL("clicked()"), self.findAcTypes)
        
        ## airline fleets tab
        self.connect(self.ui.showButton_fleet, QtCore.SIGNAL("clicked()"), self.sendQueryFleet)
        self.connect(self.ui.clearButton_fleet, QtCore.SIGNAL("clicked()"), self.clearFleet)
        self.connect(self.ui.deleteFleetButton, QtCore.SIGNAL("clicked()"), self.deleteFleets)
        self.connect(self.del_fleet_shortcut, QtCore.SIGNAL("activated()"), self.ui.deleteFleetButton, QtCore.SLOT('click()'))
        self.connect(self.ui.truncateFleetButton, QtCore.SIGNAL("clicked()"), self.confirmDeleteFleet)
        self.connect(self.ui.addFleetButton, QtCore.SIGNAL("clicked()"), self.addFleet)
        self.connect(self.ui.generateAircraftFleetButton, QtCore.SIGNAL("clicked()"), self.generateAircraftFleetTable)
        self.connect(self.ui.generateFlightplansButton, QtCore.SIGNAL("clicked()"), self.generateFlightplans)
        self.connect(self.ui.previewModelButton, QtCore.SIGNAL("clicked()"), self.previewModel)
        self.connect(self.prev_aircraft_shortcut, QtCore.SIGNAL("activated()"), self.ui.previewModelButton, QtCore.SLOT('click()'))
        
        ## aircraft types tab
        self.connect(self.ui.showButton_aircraft, QtCore.SIGNAL("clicked()"), self.sendQueryAircraft)
        self.connect(self.ui.clearButton_aircraft, QtCore.SIGNAL("clicked()"), self.clearAircraft)
        self.connect(self.ui.deleteAircraftButton, QtCore.SIGNAL("clicked()"), self.deleteAircraft)
        self.connect(self.del_aircraft_shortcut, QtCore.SIGNAL("activated()"), self.ui.deleteAircraftButton, QtCore.SLOT('click()'))
        self.connect(self.ui.truncateAircraftButton, QtCore.SIGNAL("clicked()"), self.confirmDeleteAircraft)
        self.connect(self.ui.addAircraftButton, QtCore.SIGNAL("clicked()"), self.addAircraft)
        self.connect(self.ui.addMissingAircraftButton, QtCore.SIGNAL("clicked()"), self.databaseThread.getMissingAircraft, QtCore.Qt.QueuedConnection)
        
        ## aircraft fleet tab
        self.connect(self.ui.showButton_aircraft_fleet, QtCore.SIGNAL("clicked()"), self.sendQueryAircraftFleet)
        self.connect(self.ui.clearButton_aircraft_fleet, QtCore.SIGNAL("clicked()"), self.clearAircraftFleet)
        self.connect(self.ui.truncateAircraftFleetButton, QtCore.SIGNAL("clicked()"), self.confirmDeleteAircraftFleet)
        self.connect(self.ui.generateAircraftButton, QtCore.SIGNAL("clicked()"), self.generateAircraftFleet)
        
        
        #self.connect(self.ui.tableWidget, QtCore.SIGNAL("cellChanged(int,int)"), self.itemModified)

    
    def startDBThread(self):
        
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results"), self.updateFlights, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results_fleet"), self.updateFleet, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results_aircraft"), self.updateAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results_aircraft_fleet"), self.updateAircraftFleet, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results_hubs"), self.showHubs, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("ready_results_ac_types"), self.showAcTypes, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("show_total_nr"), self.showNrFlights, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("show_total_nr_fleets"), self.showNrFleets, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("show_total_nr_aircraft"), self.showNrAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL("show_total_nr_aircraft_fleet"), self.showNrAircraftFleet, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('message_success'), self.popMessage, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('import_progress'), self.trackProgress, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('update_required'), self.sendQuery, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('update_required_fleet'), self.sendQueryFleet, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('update_required_aircraft'), self.sendQueryAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('update_required_aircraft_fleet'), self.sendQueryAircraftFleet, QtCore.Qt.QueuedConnection)
        self.connect(self.databaseThread, QtCore.SIGNAL('fleet_airlines'), self.fillAirlines, QtCore.Qt.QueuedConnection)

        self.connect(self, QtCore.SIGNAL('nr_flights'), self.databaseThread.getNrFlights, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('nr_fleets'), self.databaseThread.getNrFleets, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('nr_aircraft'), self.databaseThread.getNrAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('nr_aircraft_fleet'), self.databaseThread.getNrAircraftFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('export'), self.databaseThread.exportConfs, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('export_fleet'), self.databaseThread.exportFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('export_aircraft'), self.databaseThread.exportAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query'), self.databaseThread.runQuery, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query_fleet'), self.databaseThread.runQueryFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query_aircraft'), self.databaseThread.runQueryAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query_aircraft_fleet'), self.databaseThread.runQueryAircraftFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query_hubs'), self.databaseThread.runQueryHubs, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('run_query_ac_types'), self.databaseThread.runQueryAcTypes, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("delete_flights"), self.databaseThread.deleteFlights, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("delete_fleets"), self.databaseThread.deleteFleets, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("delete_aircraft"), self.databaseThread.deleteAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("edit_flight"), self.databaseThread.editFlight, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("edit_fleet"), self.databaseThread.editFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("edit_aircraft"), self.databaseThread.editAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("add_flight"), self.databaseThread.addFlight, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("add_fleet"), self.databaseThread.addFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("add_aircraft"), self.databaseThread.addAircraft, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('import_fleet'), self.databaseThread.importFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL('import_aircraft'), self.databaseThread.importAircraft, QtCore.Qt.QueuedConnection)
        
        self.connect(self, QtCore.SIGNAL("generate_aircraft"), self.databaseThread.generateAircraftFleet, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("generate_aircraft_fleet"), self.databaseThread.generateAircraftFleetTable, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("generate_all_aircraft"), self.databaseThread.generateAllAircraftFleets, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("generate_all_aircraft_fleet"), self.databaseThread.generateAllAircraftFleetsTable, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("generate_flightplans"), self.databaseThread.generateAirlineXML, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("generate_all_flightplans"), self.databaseThread.generateAllAirlinesXML, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("find_duplicate_candidates"), self.databaseThread.dupeCandidates, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("load_sql_db"), self.databaseThread.loadDBFromSQL, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("get_fleet_airlines"), self.databaseThread.getAirlines, QtCore.Qt.QueuedConnection)
        self.connect(self, QtCore.SIGNAL("preview_model"), self.databaseThread.previewModel, QtCore.Qt.QueuedConnection)
        
        self.databaseThread.start()
        
        self.emit(QtCore.SIGNAL('nr_flights'))
        self.emit(QtCore.SIGNAL('nr_fleets'))
        self.emit(QtCore.SIGNAL('nr_aircraft'))
        self.emit(QtCore.SIGNAL('nr_aircraft_fleet'))
        self.emit(QtCore.SIGNAL('get_fleet_airlines'))
    
    
    def showAboutDialog(self):
        self.aboutDialog=AboutDialog.AboutDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.aboutDialog, QtCore.SLOT('close()'))
    
    
    def showHelpDialog(self):
        self.helpDialog=HelpDialog.HelpDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.helpDialog, QtCore.SLOT('close()'))

    
    def showSettingsDialog(self):
        self.settingsDialog=SettingsDialog.SettingsDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.settingsDialog, QtCore.SLOT('close()'))
        self.settingsDialog.show()
    
    
    def showDeleteDuplicatesTreshhold(self):
        self.deleteDuplicatesDialog=DuplicatesDialog.DuplicatesDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.deleteDuplicatesDialog, QtCore.SLOT('close()'))
        self.connect(self.deleteDuplicatesDialog, QtCore.SIGNAL("delete_duplicates"), self.databaseThread.deleteDuplicateFlights, QtCore.Qt.QueuedConnection)
        self.deleteDuplicatesDialog.show()
    
    
    def popMessage(self, type, message): 
        self.messageBox=Messages.MessageBox()
        self.messageBox.setMessage(type, message)
        self.messageBox.show()
    
    
    def fillAirlines(self, airlines):
        self.ui.airlineComboBox.clear()
        self.ui.airlineComboBox.addItem('- all')
        self.ui.airlineComboBox.addItems(airlines)
        self.connect(self.ui.airlineComboBox, QtCore.SIGNAL("currentIndexChanged(const QString&)"), self.sendQueryFleetAirline)
    
    
    def trackProgress(self, nr):
        self.ui.progressBar.setValue(nr)
        if nr==100:
            self.ui.progressBar.setVisible(False)
            self.ui.progressBar.setEnabled(False)
    
    
    def dumpDatabase(self):
        self.emit(QtCore.SIGNAL('dump_database'))
    
    
    def loadDBFromSQL(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"SQL file",  os.getcwd(), "SQL files (*.sql)")
        if filename==None or filename=='':
            return
        self.emit(QtCore.SIGNAL('load_sql_db'), str(filename))
    
    
    def confirmDeleteFlights(self):
        self.confirmDialog = ConfirmDialog.ConfirmDialog()
        self.connect(self.confirmDialog, QtCore.SIGNAL("accepted()"), self.databaseThread.emptyFlights, QtCore.Qt.QueuedConnection)
    
    
    def confirmDeleteFleet(self):
        self.confirmDialog = ConfirmDialog.ConfirmDialog()
        self.connect(self.confirmDialog, QtCore.SIGNAL("accepted()"), self.databaseThread.emptyFleet, QtCore.Qt.QueuedConnection)
    
    
    def confirmDeleteAircraft(self):
        self.confirmDialog = ConfirmDialog.ConfirmDialog()
        self.connect(self.confirmDialog, QtCore.SIGNAL("accepted()"), self.databaseThread.emptyAircraft, QtCore.Qt.QueuedConnection)
    
    
    def confirmDeleteAircraftFleet(self):
        self.confirmDialog = ConfirmDialog.ConfirmDialog()
        self.connect(self.confirmDialog, QtCore.SIGNAL("accepted()"), self.databaseThread.emptyAircraftFleet, QtCore.Qt.QueuedConnection)
    
    
    def importFleet(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Import fleet info",  os.getcwd(), "Text files (*.txt)")
        if filename==None or filename=='':
            return
        self.emit(QtCore.SIGNAL('import_fleet'), str(filename))
    
    
    def importAircraft(self):
        filename = QtGui.QFileDialog.getOpenFileName(self,"Import aircraft info",  os.getcwd(), "Text files (*.txt)")
        if filename==None or filename=='':
            return
        self.emit(QtCore.SIGNAL('import_aircraft'), str(filename))
    
    
    def showImportDialog(self):
        self.importDialog=ImportDialog.ImportDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.importDialog, QtCore.SLOT('close()'))
        self.connect(self.importDialog, QtCore.SIGNAL('start_import'), self.databaseThread.importConfs, QtCore.Qt.QueuedConnection)
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
        self.importDialog.show()
    
    
    def showExportDialog(self):
        self.exportDialog=ExportDialog.ExportDialog()
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.exportDialog, QtCore.SLOT('close()'))
        self.connect(self.exportDialog, QtCore.SIGNAL('start_export'), self.exportConfs, QtCore.Qt.QueuedConnection)
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
        self.exportDialog.show()
    
    
    def exportFleet(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,"Export to Directory",  os.path.join(os.getcwd(), 'fleet_info'), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        if dir==None or dir=='':
            dir=os.path.join(os.getcwd(), 'fleet_info')
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
        self.emit(QtCore.SIGNAL('export_fleet'), str(dir))
    
    
    def exportAircraft(self):
        dir = QtGui.QFileDialog.getExistingDirectory(self,"Export to Directory",  os.path.join(os.getcwd(), 'fleet_info'), QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)
        if dir==None or dir=='':
            dir=os.path.join(os.getcwd(), 'fleet_info')
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
        self.emit(QtCore.SIGNAL('export_aircraft'), str(dir))
    
    
    
    def showNrFlights(self, nr, dupes):
        self.ui.labelTotalFlights.setText('<b>'+nr+'</b>')
        self.ui.labelDuplicates.setText('<b>'+dupes+'</b>')
    
    
    def showNrFleets(self, nr):
        self.ui.labelTotalFleet.setText('<b>'+nr+'</b>')
    
    
    def showNrAircraft(self, nr):
        self.ui.labelTotalAircraft.setText('<b>'+nr+'</b>')
    
    
    def showNrAircraftFleet(self, nr):
        self.ui.labelTotalAircraftFleet.setText('<b>'+nr+'</b>')
    
    
    def showHubs(self, hubs):
        self.hubsDialog=HubsDialog.HubsDialog(hubs)
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.hubsDialog, QtCore.SLOT('close()'))
    
    
    def showAcTypes(self, ac):
        self.actypesDialog=AcTypesDialog.AcTypesDialog(ac)
        self.connect(self, QtCore.SIGNAL('destroyed()'), self.actypesDialog, QtCore.SLOT('close()'))
    
    
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
    
    
    def findHubs(self):
        param_list=[]
        if self.ui.acTypeEdit.text()!='':
            param_list.append(('ac_type', str(self.ui.acTypeEdit.text()).upper()))
        if self.ui.airlineEdit.text()!='':
            param_list.append(('airline', str(self.ui.airlineEdit.text()).upper()))
        
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query_hubs'), parameters)
    
    
    def findAcTypes(self):
        param_list=[]
        if self.ui.airlineEdit.text()!='':
            param_list.append(('airline', str(self.ui.airlineEdit.text()).upper()))
        else:
            return
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query_ac_types'), parameters)
    
    
    def sendQueryFleet(self):
        param_list=[]
        if self.ui.callsignEdit_fleet.text()!='':
            param_list.append(('callsign', str(self.ui.callsignEdit_fleet.text())))
        if self.ui.designationEdit_fleet.text()!='':
            param_list.append(('designation', str(self.ui.designationEdit_fleet.text()).upper()))
        if self.ui.nrAircraftEdit_fleet.text()!='':
            param_list.append(('nr_ac', str(self.ui.nrAircraftEdit_fleet.text())))
        if self.ui.hubsEdit_fleet.text()!='':
            param_list.append(('hubs', str(self.ui.hubsEdit_fleet.text())))
        if self.ui.acTypeEdit_fleet.text()!='':
            param_list.append(('ac_type', str(self.ui.acTypeEdit_fleet.text()).upper()))
        if self.ui.airlineEdit_fleet.text()!='':
            param_list.append(('airline', str(self.ui.airlineEdit_fleet.text()).upper()))
        
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query_fleet'), parameters)
    
    
    def sendQueryFleetAirline(self, airline):
        param_list=[]
        if airline!='' and airline!=None and airline!='- all':
            param_list.append(('airline', str(airline).upper()))
        
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query_fleet'), parameters)
    

    def sendQueryAircraft(self):
        param_list=[]
        if self.ui.acTypeEdit_aircraft.text()!='':
            param_list.append(('ac_type', str(self.ui.acTypeEdit_aircraft.text())))
        if self.ui.designationEdit_aircraft.text()!='':
            param_list.append(('designation', str(self.ui.designationEdit_aircraft.text()).upper()))
        if self.ui.offsetEdit_aircraft.text()!='':
            param_list.append(('offset', str(self.ui.offsetEdit_aircraft.text())))
        if self.ui.radiusEdit_aircraft.text()!='':
            param_list.append(('radius', str(self.ui.radiusEdit_aircraft.text())))
        if self.ui.flTypeEdit_aircraft.text()!='':
            param_list.append(('fl_type', str(self.ui.flTypeEdit_aircraft.text())))
        if self.ui.perfClassEdit_aircraft.text()!='':
            param_list.append(('perf_class', str(self.ui.perfClassEdit_aircraft.text())))
        if self.ui.heavyEdit_aircraft.text()!='':
            param_list.append(('heavy', str(self.ui.heavyEdit_aircraft.text())))
        if self.ui.modelEdit_aircraft.text()!='':
            param_list.append(('model', str(self.ui.modelEdit_aircraft.text())))
        
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query_aircraft'), parameters)
    
    
    def sendQueryAircraftFleet(self):
        param_list=[]
        if self.ui.homeportEdit_aircraft_fleet.text()!='':
            param_list.append(('homeport', str(self.ui.homeportEdit_aircraft_fleet.text()).upper()))
        if self.ui.regEdit_aircraft_fleet.text()!='':
            param_list.append(('reg_nr', str(self.ui.regEdit_aircraft_fleet.text()).upper()))
        if self.ui.acTypeEdit_aircraft_fleet.text()!='':
            param_list.append(('ac_type', str(self.ui.acTypeEdit_aircraft_fleet.text())))
        if self.ui.designationEdit_aircraft_fleet.text()!='':
            param_list.append(('designation', str(self.ui.designationEdit_aircraft_fleet.text()).upper()))
        if self.ui.airlineEdit_aircraft_fleet.text()!='':
            param_list.append(('airline', str(self.ui.airlineEdit_aircraft_fleet.text()).upper()))
        if self.ui.liveryEdit_aircraft_fleet.text()!='':
            param_list.append(('livery', str(self.ui.liveryEdit_aircraft_fleet.text()).upper()))
        if self.ui.offsetEdit_aircraft_fleet.text()!='':
            param_list.append(('offset', str(self.ui.offsetEdit_aircraft_fleet.text())))
        if self.ui.radiusEdit_aircraft_fleet.text()!='':
            param_list.append(('radius', str(self.ui.radiusEdit_aircraft_fleet.text())))
        if self.ui.flTypeEdit_aircraft_fleet.text()!='':
            param_list.append(('fl_type', str(self.ui.flTypeEdit_aircraft_fleet.text())))
        if self.ui.perfClassEdit_aircraft_fleet.text()!='':
            param_list.append(('perf_class', str(self.ui.perfClassEdit_aircraft_fleet.text())))
        if self.ui.heavyEdit_aircraft_fleet.text()!='':
            param_list.append(('heavy', str(self.ui.heavyEdit_aircraft_fleet.text())))
        if self.ui.modelEdit_aircraft_fleet.text()!='':
            param_list.append(('model', str(self.ui.modelEdit_aircraft_fleet.text())))
        
        parameters=dict(param_list)
        self.emit(QtCore.SIGNAL('run_query_aircraft_fleet'), parameters)
    
    
    def updateFlights(self, flightlist):
        self.ui.tableWidget.setSortingEnabled(False)
        self.disconnect(self.ui.tableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.itemModified)
        if flightlist==None:
            self.popMessage('Error', 'No results found')
            return
        nr_flights=len(flightlist)
        if nr_flights==0:
            self.popMessage('Error', 'No results found')
        self.flightlist=flightlist
        self.ui.labelSelectedFlights.setText('<b>'+str(nr_flights)+'</b>')
        table=self.ui.tableWidget
        table.setRowCount(0)
        table.setRowCount(nr_flights)
        r=0
        for flight in flightlist:
            #id=QtGui.QTableWidgetItem(str(flight[0]), 0)
            id=QTableWidgetNumericItem(str(flight[0]), 0)
            id.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            id.setFlags(QtCore.Qt.NoItemFlags)
            
            callsign=QtGui.QTableWidgetItem(str(flight[1]), 0)
            callsign.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='' and flight[10]!='None':
                color=255 - 36 * int(flight[10])
                callsign.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            flt_rules=QtGui.QTableWidgetItem(str(flight[2]), 0)
            flt_rules.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                flt_rules.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            dep_day=QtGui.QTableWidgetItem(str(flight[3]).replace('.', '#'), 0)
            dep_day.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                dep_day.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            dep_airport=QtGui.QTableWidgetItem(str(flight[4]), 0)
            dep_airport.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                dep_airport.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            arr_airport=QtGui.QTableWidgetItem(str(flight[5]), 0)
            arr_airport.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                arr_airport.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            dep_time=QtGui.QTableWidgetItem(str(flight[6]), 0)
            dep_time.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                dep_time.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            arr_time=QtGui.QTableWidgetItem(str(flight[7]), 0)
            arr_time.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                arr_time.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            ac_type=QtGui.QTableWidgetItem(str(flight[8]), 0)
            ac_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                ac_type.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            flt_level=QtGui.QTableWidgetItem(str(flight[9]), 0)
            flt_level.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if flight[10]!=None and flight[10]!='':
                color=255 - 36 * int(flight[10])
                flt_level.setBackgroundColor(QtGui.QColor(255, 0, color, 127))
            
            table.setItem(r, 0, callsign)
            table.setItem(r, 1, flt_rules)
            table.setItem(r, 6, dep_day)
            table.setItem(r, 2, dep_airport)
            table.setItem(r, 3, arr_airport)
            table.setItem(r, 4, dep_time)
            table.setItem(r, 5, arr_time)
            table.setItem(r, 7, ac_type)
            table.setItem(r, 8, flt_level)
            table.setItem(r, 9, id)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            r=r+1
        self.connect(self.ui.tableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.itemModified)
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.sortItems(9, QtCore.Qt.AscendingOrder)
    
    
    def updateFleet(self, fleetlist):
        self.ui.fleetTableWidget.setSortingEnabled(False)
        self.disconnect(self.ui.fleetTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.itemModifiedFleet)
        if fleetlist==None:
            self.popMessage('Error', 'No results found')
            return
        nr_fleet=len(fleetlist)
        if nr_fleet==0:
            self.popMessage('Error', 'No results found')
        self.fleetlist=fleetlist
        self.ui.labelSelectedFleet.setText('<b>'+str(nr_fleet)+'</b>')
        table=self.ui.fleetTableWidget
        table.setRowCount(0)
        table.setRowCount(nr_fleet)
        r=0
        for fleet in fleetlist:
            #id=QtGui.QTableWidgetItem(str(fleet[0]), 0)
            id=QTableWidgetNumericItem(str(fleet[0]), 0)
            id.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            id.setFlags(QtCore.Qt.NoItemFlags)
            
            airline=QtGui.QTableWidgetItem(str(fleet[1]), 0)
            airline.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            ac_type=QtGui.QTableWidgetItem(str(fleet[2]), 0)
            ac_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            #nr_ac=QtGui.QTableWidgetItem(str(fleet[3]), 0)
            nr_ac=QTableWidgetNumericItem(str(fleet[3]), 0)
            nr_ac.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            hubs=QtGui.QTableWidgetItem(str(fleet[4]), 0)
            hubs.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            callsign=QtGui.QTableWidgetItem(str(fleet[5]), 0)
            callsign.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            designation=QtGui.QTableWidgetItem(str(fleet[6]), 0)
            designation.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            if fleet[7]==1:
                designation.setBackgroundColor(QtGui.QColor(0, 255, 0, 127))
            else:
                designation.setBackgroundColor(QtGui.QColor(255, 0, 0, 127))
            
            table.setItem(r, 0, airline)
            table.setItem(r, 1, ac_type)
            table.setItem(r, 2, nr_ac)
            table.setItem(r, 3, hubs)
            table.setItem(r, 4, callsign)
            table.setItem(r, 5, designation)
            table.setItem(r, 6, id)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            r=r+1
        self.connect(self.ui.fleetTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.itemModifiedFleet)
        self.ui.fleetTableWidget.setSortingEnabled(True)
        self.ui.fleetTableWidget.sortItems(6, QtCore.Qt.AscendingOrder)
    
    
    def updateAircraft(self, aclist):
        self.ui.aircraftTableWidget.setSortingEnabled(False)
        self.disconnect(self.ui.aircraftTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.itemModifiedAircraft)
        if aclist==None:
            self.popMessage('Error', 'No results found')
            return
        nr_ac=len(aclist)
        if nr_ac==0:
            self.popMessage('Error', 'No results found')
        self.aircraftlist=aclist
        self.ui.labelSelectedAircraft.setText('<b>'+str(nr_ac)+'</b>')
        table=self.ui.aircraftTableWidget
        table.setRowCount(0)
        table.setRowCount(nr_ac)
        r=0
        for ac in aclist:
            #id=QtGui.QTableWidgetItem(str(ac[0]), 0)
            id=QTableWidgetNumericItem(str(ac[0]), 0)
            id.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            id.setFlags(QtCore.Qt.NoItemFlags)
            
            ac_type=QtGui.QTableWidgetItem(str(ac[1]), 0)
            ac_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            designation=QtGui.QTableWidgetItem(str(ac[2]), 0)
            designation.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            offset=QtGui.QTableWidgetItem(str(ac[3]), 0)
            offset.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            radius=QtGui.QTableWidgetItem(str(ac[4]), 0)
            radius.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            fl_type=QtGui.QTableWidgetItem(str(ac[5]), 0)
            fl_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            perf_class=QtGui.QTableWidgetItem(str(ac[6]), 0)
            perf_class.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            heavy=QtGui.QTableWidgetItem(str(ac[7]), 0)
            heavy.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            model=QtGui.QTableWidgetItem(str(ac[8]), 0)
            model.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            table.setItem(r, 0, ac_type)
            table.setItem(r, 1, designation)
            table.setItem(r, 2, offset)
            table.setItem(r, 3, radius)
            table.setItem(r, 4, fl_type)
            table.setItem(r, 5, perf_class)
            table.setItem(r, 6, heavy)
            table.setItem(r, 7, model)
            table.setItem(r, 8, id)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            r=r+1
        self.connect(self.ui.aircraftTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.itemModifiedAircraft)
        self.ui.aircraftTableWidget.setSortingEnabled(True)
        self.ui.aircraftTableWidget.sortItems(8, QtCore.Qt.AscendingOrder)
    
    
    def updateAircraftFleet(self, aclist):
        self.ui.aircraftFleetTableWidget.setSortingEnabled(False)
        if aclist==None:
            self.popMessage('Error', 'No results found')
            return
        nr_ac=len(aclist)
        if nr_ac==0:
            self.popMessage('Error', 'No results found')
        self.ui.labelSelectedAircraftFleet.setText('<b>'+str(nr_ac)+'</b>')
        table=self.ui.aircraftFleetTableWidget
        table.setRowCount(0)
        table.setRowCount(nr_ac)
        r=0
        for ac in aclist:
            id=QTableWidgetNumericItem(str(ac[0]), 0)
            id.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            id.setFlags(QtCore.Qt.NoItemFlags)
            
            homeport=QtGui.QTableWidgetItem(str(ac[1]), 0)
            homeport.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            reg_nr=QtGui.QTableWidgetItem(str(ac[2]), 0)
            reg_nr.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            ac_type=QtGui.QTableWidgetItem(str(ac[3]), 0)
            ac_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            designation=QtGui.QTableWidgetItem(str(ac[4]), 0)
            designation.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            airline=QtGui.QTableWidgetItem(str(ac[5]), 0)
            airline.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            livery=QtGui.QTableWidgetItem(str(ac[6]), 0)
            livery.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            offset=QtGui.QTableWidgetItem(str(ac[7]), 0)
            offset.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            radius=QtGui.QTableWidgetItem(str(ac[8]), 0)
            radius.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            fl_type=QtGui.QTableWidgetItem(str(ac[9]), 0)
            fl_type.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            perf_class=QtGui.QTableWidgetItem(str(ac[10]), 0)
            perf_class.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            heavy=QtGui.QTableWidgetItem(str(ac[11]), 0)
            heavy.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            model=QtGui.QTableWidgetItem(str(ac[12]), 0)
            model.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            table.setItem(r, 0, homeport)
            table.setItem(r, 1, reg_nr)
            table.setItem(r, 2, ac_type)
            table.setItem(r, 3, designation)
            table.setItem(r, 4, airline)
            table.setItem(r, 5, livery)
            table.setItem(r, 6, offset)
            table.setItem(r, 7, radius)
            table.setItem(r, 8, fl_type)
            table.setItem(r, 9, perf_class)
            table.setItem(r, 10, heavy)
            table.setItem(r, 11, model)
            table.setItem(r, 12, id)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            r=r+1
        self.ui.aircraftFleetTableWidget.setSortingEnabled(True)
        self.ui.aircraftFleetTableWidget.sortItems(8, QtCore.Qt.AscendingOrder)
    
    
    def clearFlights(self):
        self.page=0
        table=self.ui.tableWidget
        #table.clear()
        table.setRowCount(0)
        self.ui.callsignEdit.setText('')
        self.ui.depAirportEdit.setText('')
        self.ui.depTimeEdit.setText('')
        self.ui.depDayEdit.setText('')
        self.ui.acTypeEdit.setText('')
        self.ui.airlineEdit.setText('')
        self.ui.arrAirportEdit.setText('')
        self.ui.arrTimeEdit.setText('')
        self.ui.labelSelectedFlights.setText('<b>0</b>')
    
    
    def clearFleet(self):
        self.page=0
        table=self.ui.fleetTableWidget
        table.setRowCount(0)
        self.ui.callsignEdit_fleet.setText('')
        self.ui.designationEdit_fleet.setText('')
        self.ui.nrAircraftEdit_fleet.setText('')
        self.ui.hubsEdit_fleet.setText('')
        self.ui.acTypeEdit_fleet.setText('')
        self.ui.airlineEdit_fleet.setText('')
        self.ui.labelSelectedFleet.setText('<b>0</b>')
    

    def clearAircraft(self):
        self.page=0
        table=self.ui.aircraftTableWidget
        table.setRowCount(0)
        self.ui.acTypeEdit_aircraft.setText('')
        self.ui.designationEdit_aircraft.setText('')
        self.ui.offsetEdit_aircraft.setText('')
        self.ui.radiusEdit_aircraft.setText('')
        self.ui.flTypeEdit_aircraft.setText('')
        self.ui.perfClassEdit_aircraft.setText('')
        self.ui.heavyEdit_aircraft.setText('')
        self.ui.modelEdit_aircraft.setText('')
        self.ui.labelSelectedAircraft.setText('<b>0</b>')
    
    
    def clearAircraftFleet(self):
        self.page=0
        table=self.ui.aircraftFleetTableWidget
        table.setRowCount(0)
        self.ui.homeportEdit_aircraft_fleet.setText('')
        self.ui.regEdit_aircraft_fleet.setText('')
        self.ui.acTypeEdit_aircraft_fleet.setText('')
        self.ui.designationEdit_aircraft_fleet.setText('')
        self.ui.airlineEdit_aircraft_fleet.setText('')
        self.ui.liveryEdit_aircraft_fleet.setText('')
        self.ui.offsetEdit_aircraft_fleet.setText('')
        self.ui.radiusEdit_aircraft_fleet.setText('')
        self.ui.flTypeEdit_aircraft_fleet.setText('')
        self.ui.perfClassEdit_aircraft_fleet.setText('')
        self.ui.heavyEdit_aircraft_fleet.setText('')
        self.ui.modelEdit_aircraft_fleet.setText('')
        self.ui.labelSelectedAircraftFleet.setText('<b>0</b>')
    
    
    def exportConfs(self, dir,  separate_airlines, what):
        
        if what=='view':
            if len(self.flightlist)==0:
                self.popMessage('Error', 'No flights in current view')
                self.ui.progressBar.setVisible(False)
                self.ui.progressBar.setEnabled(False)
                return
            flightlist=self.flightlist
        elif what=='selected':
            if len(self.flightlist)==0:
                self.popMessage('Error', 'No flights in current view')
                self.ui.progressBar.setVisible(False)
                self.ui.progressBar.setEnabled(False)
                return
            table=self.ui.tableWidget
            sel_ranges=table.selectedRanges()
            for sel_range in sel_ranges:
                if sel_range.topRow()== sel_range.bottomRow():
                    row=sel_range.topRow()
                    item=table.item(row, 9)
                    if item==0:
                        continue
                    id=int(item.text())
                    for flight in self.flightlist:
                        if id==flight[0]:
                            self.flightlist_selected.append(flight)
                        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                else:
                    for row in range(sel_range.topRow(), sel_range.bottomRow()+1):
                        item=table.item(row, 9)
                        if item==0:
                            continue
                        id=int(item.text())
                        for flight in self.flightlist:
                            if id==flight[0]:
                                self.flightlist_selected.append(flight)
                            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            
            if len(self.flightlist_selected)==0:
                self.popMessage('Error', 'No flights are currently selected')
                self.ui.progressBar.setVisible(False)
                self.ui.progressBar.setEnabled(False)
                return
            flightlist=self.flightlist_selected
            self.flightlist_selected=[]
        elif what=='database':
            flightlist=[]
        self.emit(QtCore.SIGNAL('export'), dir, separate_airlines, flightlist)
    
    
    def deleteFlights(self):
        ids=[]
        rows=[]
        table=self.ui.tableWidget
        sel_ranges=table.selectedRanges()
        for sel_range in sel_ranges:
            if sel_range.topRow()== sel_range.bottomRow():
                row=sel_range.topRow()
                item=table.item(row, 9)
                if item==0:
                    continue
                id=int(item.text())
                if id not in ids:
                    ids.append(id)
                QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            else:
                for row in range(sel_range.topRow(), sel_range.bottomRow()+1):
                    item=table.item(row, 9)
                    if item==0:
                        continue
                    id=int(item.text())
                    if id not in ids:
                        ids.append(id)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.emit(QtCore.SIGNAL('delete_flights'), ids)
    
    
    def deleteFleets(self):
        ids=[]
        rows=[]
        table=self.ui.fleetTableWidget
        sel_ranges=table.selectedRanges()
        for sel_range in sel_ranges:
            if sel_range.topRow()== sel_range.bottomRow():
                row=sel_range.topRow()
                item=table.item(row, 6)
                if item==0:
                    continue
                id=int(item.text())
                if id not in ids:
                    ids.append(id)
                QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            else:
                for row in range(sel_range.topRow(), sel_range.bottomRow()+1):
                    item=table.item(row, 6)
                    if item==0:
                        continue
                    id=int(item.text())
                    if id not in ids:
                        ids.append(id)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.emit(QtCore.SIGNAL('delete_fleets'), ids)
    
    
    def deleteAircraft(self):
        ids=[]
        rows=[]
        table=self.ui.aircraftTableWidget
        sel_ranges=table.selectedRanges()
        for sel_range in sel_ranges:
            if sel_range.topRow()== sel_range.bottomRow():
                row=sel_range.topRow()
                item=table.item(row, 8)
                if item==0:
                    continue
                id=int(item.text())
                if id not in ids:
                    ids.append(id)
                QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            else:
                for row in range(sel_range.topRow(), sel_range.bottomRow()+1):
                    item=table.item(row, 8)
                    if item==0:
                        continue
                    id=int(item.text())
                    if id not in ids:
                        ids.append(id)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.emit(QtCore.SIGNAL('delete_aircraft'), ids)
    
    
    def itemModified(self, item):
        table=self.ui.tableWidget
        column=item.column()
        if column==9:
            #we don't like them messing with our precious ids
            self.sendQuery()
            return
        row=item.row()
        new_data=str(item.text())
        param_list=[]
        if column==0:
            param_list.append(('callsign', new_data))
        elif column==1:
            param_list.append(('flt_rules', new_data))
        elif column==2:
            param_list.append(('dep_airport', new_data))
        elif column==3:
            param_list.append(('arr_airport', new_data))
        elif column==4:
            param_list.append(('dep_time', new_data))
        elif column==5:
            param_list.append(('arr_time', new_data))
        elif column==6:
            new_data=new_data.replace('#','.')
            param_list.append(('dep_day', new_data))
        elif column==7:
            param_list.append(('ac_type', new_data))
        elif column==8:
            param_list.append(('flt_level', new_data))
        item_id=table.item(row, 9)
        
        id=int(item_id.text())
        #print id,  new_data
        param_list.append(('id', id))
        self.emit(QtCore.SIGNAL('edit_flight'), param_list)
    
    
    def itemModifiedFleet(self, item):
        table=self.ui.fleetTableWidget
        column=item.column()
        if column==6:
            #we don't like them messing with our precious ids
            self.sendQueryFleet()
            return
        row=item.row()
        new_data=str(item.text())
        param_list=[]
        if column==0:
            param_list.append(('airline', new_data))
        elif column==1:
            param_list.append(('ac_type', new_data))
        elif column==2:
            param_list.append(('nr_ac', new_data))
        elif column==3:
            param_list.append(('hubs', new_data))
        elif column==4:
            param_list.append(('callsign', new_data))
        elif column==5:
            param_list.append(('designation', new_data))
        item_id=table.item(row, 6)
        
        id=int(item_id.text())
        #print id,  new_data
        param_list.append(('id', id))
        self.emit(QtCore.SIGNAL('edit_fleet'), param_list)
    
    
    def itemModifiedAircraft(self, item):
        table=self.ui.aircraftTableWidget
        column=item.column()
        if column==8:
            #we don't like them messing with our precious ids
            self.sendQueryAircraft()
            return
        row=item.row()
        new_data=str(item.text())
        param_list=[]
        if column==0:
            param_list.append(('ac_type', new_data))
        elif column==1:
            param_list.append(('designation', new_data))
        elif column==2:
            param_list.append(('offset', new_data))
        elif column==3:
            param_list.append(('radius', new_data))
        elif column==4:
            param_list.append(('fl_type', new_data))
        elif column==5:
            param_list.append(('perf_class', new_data))
        elif column==6:
            param_list.append(('heavy', new_data))
        elif column==7:
            param_list.append(('model', new_data))
        item_id=table.item(row, 8)
        
        id=int(item_id.text())
        #print id,  new_data
        param_list.append(('id', id))
        self.emit(QtCore.SIGNAL('edit_aircraft'), param_list)
    
    #TODO: implement a more thorough check of fields via re
    def addFlight(self):
        param_list=[]
        if self.ui.callsignEdit.text()!='':
            param_list.append( str(self.ui.callsignEdit.text()))
        if self.ui.callsignEdit.text()!='':
            param_list.append( 'IFR')
        if self.ui.depDayEdit.text()!='':
            param_list.append( str(self.ui.depDayEdit.text()))
        if self.ui.depAirportEdit.text()!='' and len(str(self.ui.depAirportEdit.text()).upper())==4:
            param_list.append(str(self.ui.depAirportEdit.text()).upper())
        if self.ui.arrAirportEdit.text()!='' and len(str(self.ui.arrAirportEdit.text()).upper())==4:
            param_list.append( str(self.ui.arrAirportEdit.text()).upper())
        if self.ui.depTimeEdit.text()!='' and len(str(self.ui.depTimeEdit.text()))==5:
            param_list.append( str(self.ui.depTimeEdit.text()))
        if self.ui.arrTimeEdit.text()!='' and len(str(self.ui.arrTimeEdit.text()))==5:
            param_list.append( str(self.ui.arrTimeEdit.text()))
        if self.ui.acTypeEdit.text()!='' and self.ui.airlineEdit.text()!='' \
            and  len(str(self.ui.acTypeEdit.text()).upper())==3 and len(str(self.ui.airlineEdit.text()).upper())==3:
            param_list.append( str(self.ui.acTypeEdit.text()).upper() + str(self.ui.airlineEdit.text()).upper() )
        altitudes_jet=(280,290,300,310,320,330,340,350)
        altitudes_prop=(150,160,170,180,190,200,210,220)
        req_aircraft=str(self.ui.acTypeEdit.text()).upper()
        if req_aircraft=='AT7' or req_aircraft=='J31' or req_aircraft=='ATR' or req_aircraft=='AT4' or req_aircraft=='FRJ' or req_aircraft=='D38' \
            or req_aircraft=='F50' or req_aircraft=='AT4' or req_aircraft=='AT5' or req_aircraft=='EM2':
            cruise_alt=str(random.choice(altitudes_prop))
        else:
            cruise_alt=str(random.choice(altitudes_jet))
        param_list.append(cruise_alt)
        if len(param_list)!=9:
            self.popMessage('Error', 'You must fill all fields correctly')
            return

        self.emit(QtCore.SIGNAL('add_flight'), param_list)
    
    #TODO: implement a more thorough check of fields via re
    def addFleet(self):
        param_list=[]
        if self.ui.airlineEdit_fleet.text()!='' and len(str(self.ui.airlineEdit_fleet.text()).upper())==3:
            param_list.append( str(self.ui.airlineEdit_fleet.text()).upper())
        if self.ui.acTypeEdit_fleet.text()!='' and len(str(self.ui.acTypeEdit_fleet.text()).upper())==3:
            param_list.append( str(self.ui.acTypeEdit_fleet.text()).upper())
        if self.ui.nrAircraftEdit_fleet.text()!='' and str(self.ui.nrAircraftEdit_fleet.text()).isdigit()==True:
            param_list.append( str(self.ui.nrAircraftEdit_fleet.text()))
        if self.ui.hubsEdit_fleet.text()!='':
            param_list.append( str(self.ui.hubsEdit_fleet.text()))
        if self.ui.callsignEdit_fleet.text()!='':
            param_list.append( str(self.ui.callsignEdit_fleet.text()))
        if self.ui.designationEdit_fleet.text()!='':
            param_list.append( str(self.ui.designationEdit_fleet.text()).upper())
        
        if len(param_list)!=6:
            self.popMessage('Error', 'You must fill all fields correctly')
            return

        self.emit(QtCore.SIGNAL('add_fleet'), param_list)
    
    #TODO: implement a more thorough check of fields via re
    def addAircraft(self):
        param_list=[]
        if self.ui.acTypeEdit_aircraft.text()!='' and len(str(self.ui.acTypeEdit_aircraft.text()))==3:
            param_list.append(str(self.ui.acTypeEdit_aircraft.text()))
        if self.ui.designationEdit_aircraft.text()!='':
            param_list.append( str(self.ui.designationEdit_aircraft.text()).upper())
        if self.ui.offsetEdit_aircraft.text()!='' and str(self.ui.offsetEdit_aircraft.text()).isdigit()==True:
            param_list.append( str(self.ui.offsetEdit_aircraft.text()))
        if self.ui.radiusEdit_aircraft.text()!='' and str(self.ui.radiusEdit_aircraft.text()).isdigit()==True:
            param_list.append( str(self.ui.radiusEdit_aircraft.text()))
        if self.ui.flTypeEdit_aircraft.text()!='':
            param_list.append( str(self.ui.flTypeEdit_aircraft.text()))
        if self.ui.perfClassEdit_aircraft.text()!='':
            param_list.append( str(self.ui.perfClassEdit_aircraft.text()))
        if self.ui.heavyEdit_aircraft.text()!='' and (str(self.ui.heavyEdit_aircraft.text())=='true' or str(self.ui.heavyEdit_aircraft.text())=='false'):
            param_list.append( str(self.ui.heavyEdit_aircraft.text()))
        if self.ui.modelEdit_aircraft.text()!='':
            param_list.append( str(self.ui.modelEdit_aircraft.text()))
        if len(param_list)!=8:
            self.popMessage('Error', 'You must fill all fields correctly')
            return

        self.emit(QtCore.SIGNAL('add_aircraft'), param_list)
    
    
    def generateAircraftFleet(self):
        if self.ui.airlineEdit_aircraft_fleet.text()!='':
            airline=str(self.ui.airlineEdit_aircraft_fleet.text()).upper()
            self.emit(QtCore.SIGNAL('generate_aircraft'), airline)
        else:
            self.emit(QtCore.SIGNAL('generate_all_aircraft'))
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
    
    
    def generateAircraftFleetTable(self):
        if self.ui.airlineEdit_fleet.text()!='':
            airline=str(self.ui.airlineEdit_fleet.text()).upper()
            self.emit(QtCore.SIGNAL('generate_aircraft_fleet'), airline)
        else:
            self.emit(QtCore.SIGNAL('generate_all_aircraft_fleet'))
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
    
    
    def generateFlightplans(self):
        if self.ui.airlineEdit_aircraft_fleet.text()!='':
            airline=str(self.ui.airlineEdit_aircraft_fleet.text()).upper()
            self.emit(QtCore.SIGNAL('generate_flightplans'), airline)
        else:
            self.emit(QtCore.SIGNAL('generate_all_flightplans'))
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
    
    
    def findDupes(self):
        self.ui.progressBar.setVisible(True)
        self.ui.progressBar.setEnabled(True)
        if self.ui.airlineEdit.text()!='':
            airline=str(self.ui.airlineEdit.text()).upper()
            self.emit(QtCore.SIGNAL('find_duplicate_candidates'), airline)
        else:
            self.emit(QtCore.SIGNAL('find_duplicate_candidates'), None)
            
    
    def confirmFindDupes(self):
        self.confirmDialog = ConfirmDialog.ConfirmDialog()
        self.connect(self.confirmDialog, QtCore.SIGNAL("accepted()"), self.findDupes, QtCore.Qt.QueuedConnection)
    
    
    def previewModel(self):
        ids=[]
        rows=[]
        table=self.ui.fleetTableWidget
        sel_ranges=table.selectedRanges()
        if len(sel_ranges) !=1:
            return
        if sel_ranges[0].topRow()== sel_ranges[0].bottomRow():
            row=sel_ranges[0].topRow()
            item=table.item(row, 6)
            if item==0:
                return
            id=int(item.text())
        self.emit(QtCore.SIGNAL('preview_model'), id)
    
