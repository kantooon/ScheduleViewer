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


import os, sys, glob, io
from PyQt4 import QtCore
from database import FlightsDatabase


class  DatabaseThread(QtCore.QThread):
    
    def __init__(self,  parent=None):
        QtCore.QThread.__init__(self, parent)
        self.db=FlightsDatabase()

    
    def __del__(self):
        del self.db
        self.exit(1)
    
    
    def run(self):
        self.exec_()

    
    def importFleet(self, filename):
        fr=open(filename, 'rb')
        content= fr.readlines()
        for line in content:
            if line.find('#')==0 or len(line)<2:
                continue
            stubs=line.split()
            stubs=stubs[1:]
            stubs[5]=stubs[5].rstrip('\n')
            self.db.addFleet(stubs)
            self.db.commitTransaction()
    
    
    def importAircraft(self, filename):
        fr=open(filename, 'rb')
        content= fr.readlines()
        for line in content:
            if line.find('#')==0 or len(line)<2:
                continue
            stubs=line.split()
            stubs.reverse()
            stubs[0]=stubs[0].rstrip('\n')
            stubs.reverse()
            length=len(stubs)
            if length <8:
                for i in range(0, 8-length ):
                    stubs.append("")
            self.db.addAircraft(stubs)
            self.db.commitTransaction()
    
    
    def importConfs(self, path, recurse):
        expr="os.path.join(path,"
        
        for i in range(0, recurse):
            expr=expr+"'*',"
        expr=expr+"'*.conf')"
        conf_files=glob.glob(eval(expr))
        #print conf_files
        if conf_files==None or len(conf_files)==0:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Import failed: no files found')
            return
        progress_overall=0
        progress_overall_step=100 / len(conf_files)
        try:
            for conf in conf_files:
                fr=open(conf,'rb')
                content= fr.readlines()
                for line in content:
                    if line.find('#')==0 or len(line)<2:
                        continue
                    stubs1=line.split("   ")
                    ## do not add individual daily flights, add weekly ones
                    ac_type=stubs1[9].rstrip('\n')
                    flight=[stubs1[1],stubs1[2],stubs1[3],stubs1[5],stubs1[7],stubs1[4],stubs1[6],ac_type,stubs1[8]]
                    self.db.addFlight(flight)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                    """
                    for i in stubs1[3]:
                        if i.isdigit():
                            ac_type=stubs1[9].rstrip('\n')
                            flight=[stubs1[1],stubs1[2],i,stubs1[5],stubs1[7],stubs1[4],stubs1[6],ac_type,stubs1[8]]
                            self.db.addFlight(flight)
                            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                    """
                self.db.commitTransaction()
                progress_overall=progress_overall+progress_overall_step
                self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            self.emit(QtCore.SIGNAL('import_progress'), 100)
            self.emit(QtCore.SIGNAL('message_success'), 'Info','Flights have been imported')
            self.getNrFlights()
        except:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Flights could not be imported')
            self.emit(QtCore.SIGNAL('import_progress'), 0)
        
    
    
    def exportConfs(self, path, separate_airlines, what):
        ##separate airline files option
        if separate_airlines==True:
            ## all database exported
            if len(what)==0:
                flights=self.db.getAllFlights()
                airlines=[]
                for flight in flights:
                    airline=str(flight[8][4:])
                    if airline not in airlines:
                        airlines.append(airline)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                progress_overall=0
                progress_overall_step=100 / len(airlines)
                for airline in airlines:
                    airline = airline[0:3]
                    fw=open(os.path.join(path,airline+'.conf'),'wb')
                    buf=''
                    params=dict({'airline':airline})
                    flights=self.db.queryFlights(params)
                    for flight in flights:
                        conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                        +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                        buf=buf+conf
                        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                    file_content="########Flt.No      Flt.Rules Days    Departure       Arrival         FltLev. A/C type\n"+\
                    "################### ######### ####### ############### ############### #################\n\n"+buf
                    fw.write(file_content)
                    fw.close()
                    progress_overall=progress_overall+progress_overall_step
                    self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                self.emit(QtCore.SIGNAL('import_progress'), 100)
                self.emit(QtCore.SIGNAL('message_success'), 'Info','Database flights have been exported successfully')
            ## only flights in view
            else:
                flights=what
                airlines=[]
                for flight in flights:
                    airline=str(flight[8][4:])
                    if airline not in airlines:
                        airlines.append(airline)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                progress_overall=0
                progress_overall_step=100 / len(airlines)
                for airline in airlines:
                    airline = airline[0:3]
                    fw=open(os.path.join(path,airline+'.conf'),'wb')
                    buf=''
                    for flight in flights:
                        if str(flight[8][4:])==airline:
                            conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                            +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                            buf=buf+conf
                        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                    file_content="########Flt.No      Flt.Rules Days    Departure       Arrival         FltLev. A/C type\n"+\
                    "################### ######### ####### ############### ############### #################\n\n"+buf
                    fw.write(file_content)
                    fw.close()
                    progress_overall=progress_overall+progress_overall_step
                    self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                self.emit(QtCore.SIGNAL('import_progress'), 100)
                self.emit(QtCore.SIGNAL('message_success'), 'Info','Database flights have been exported successfully')
        
        ## one large file with all flights
        else:
            ## all database flights exported
            if len(what)==0:
                flights=self.db.getAllFlights()
                progress_overall=0
                progress_overall_step=100 / len(flights)
                fw=open(os.path.join(path,'view.conf'),'wb')
                buf=''
                for flight in flights:
                    conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                    +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                    buf=buf+conf
                    progress_overall=progress_overall+progress_overall_step
                    self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                file_content="########Flt.No      Flt.Rules Days    Departure       Arrival         FltLev. A/C type\n"+\
                "################### ######### ####### ############### ############### #################\n\n"+buf
                fw.write(file_content)
                fw.close()
                self.emit(QtCore.SIGNAL('import_progress'), 100)
                self.emit(QtCore.SIGNAL('message_success'), 'Info','Database flights have been exported successfully')
            ## only flights in view
            else:
                flights=what
                progress_overall=0
                progress_overall_step=100 / len(flights)
                fw=open(os.path.join(path,'view.conf'),'wb')
                buf=''
                for flight in flights:
                    conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                    +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                    buf=buf+conf
                    progress_overall=progress_overall+progress_overall_step
                    self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                file_content="########Flt.No      Flt.Rules Days    Departure       Arrival         FltLev. A/C type\n"+\
                "################### ######### ####### ############### ############### #################\n\n"+buf
                fw.write(file_content)
                fw.close()
                self.emit(QtCore.SIGNAL('import_progress'), 100)
                self.emit(QtCore.SIGNAL('message_success'), 'Info','Database flights have been exported successfully')
    
    
    def exportFleet(self, dir_path):
        fleets=self.db.getAllFleets()
        progress_overall=0
        progress_overall_step=100 / len(fleets)
        fw=open(os.path.join(dir_path,'fleetinfo.txt'),'wb')
        buf=''
        for fleet in fleets:
            conf = "ENTRY   "+str(fleet[1])+"   "+str(fleet[2])+"   "+str(fleet[3])+"   "+str(fleet[4])+"   "+str(fleet[5])+"   "+str(fleet[6])+"\n"
            buf=buf+conf
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        file_content="###Airline   Ac. Type   Nr. Aircraft     Hubs     Callsign    Designation\n"+\
        "######### ######### ####### ############### ############### #################\n\n"+buf
        fw.write(file_content)
        fw.close()
        self.emit(QtCore.SIGNAL('import_progress'), 100)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Fleets have been exported successfully')
    
    
    def exportAircraft(self, dir_path):
        aircraft=self.db.getAllAircraft()
        progress_overall=0
        progress_overall_step=100 / len(aircraft)
        fw=open(os.path.join(dir_path,'aircraft.txt'),'wb')
        buf=''
        for ac in aircraft:
            conf = str(ac[1])+"   "+str(ac[2])+"   "+str(ac[3])+"   "+str(ac[4])+"   "+str(ac[5])+"   "+str(ac[6])+"   "+str(ac[7])+"   "+str(ac[8])+"\n"
            buf=buf+conf
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        #file_content="###Airline   Ac. Type   Nr. Aircraft     Hubs     Callsign    Designation\n"+\
        #"######### ######### ####### ############### ############### #################\n\n"+buf
        file_content=buf
        fw.write(file_content)
        fw.close()
        self.emit(QtCore.SIGNAL('import_progress'), 100)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Aircraft have been exported successfully')
    
    
    def runQuery(self, params):
        res=self.db.queryFlights(params)
        self.emit(QtCore.SIGNAL('ready_results'), res)
    
    
    def runQueryFleet(self, params):
        res=self.db.queryFleet(params)
        self.emit(QtCore.SIGNAL('ready_results_fleet'), res)
    
    
    def runQueryAircraft(self, params):
        res=self.db.queryAircraft(params)
        self.emit(QtCore.SIGNAL('ready_results_aircraft'), res)
    
    
    def getNrFlights(self):
        res=self.db.getNrFlights()
        self.emit(QtCore.SIGNAL('show_total_nr'), str(res))
    
    
    def getNrFleets(self):
        res=self.db.getNrFleets()
        self.emit(QtCore.SIGNAL('show_total_nr_fleets'), str(res))
    
    
    def getNrAircraft(self):
        res=self.db.getNrAircraft()
        self.emit(QtCore.SIGNAL('show_total_nr_aircraft'), str(res))
    
    
    def deleteFlights(self, flightlist):
        if flightlist==None or len(flightlist)==0:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','No flights selected')
            return
        for flight in flightlist:
            self.db.deleteFlight(flight)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.db.commitTransaction()
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Flights have been deleted')
        self.emit(QtCore.SIGNAL('update_required'))
    
    
    def deleteFleets(self, fleetlist):
        if fleetlist==None or len(fleetlist)==0:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','No fleets selected')
            return
        for fleet in fleetlist:
            self.db.deleteFleet(fleet)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.db.commitTransaction()
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Fleets have been deleted')
        self.emit(QtCore.SIGNAL('update_required_fleet'))
    
    
    def deleteAircraft(self, aclist):
        if aclist==None or len(aclist)==0:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','No aircraft selected')
            return
        for ac in aclist:
            self.db.deleteAircraft(ac)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.db.commitTransaction()
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Aircraft have been deleted')
        self.emit(QtCore.SIGNAL('update_required_aircraft'))
    
    
    def emptyFlights(self):
        self.db.emptyFlights()
        self.emit(QtCore.SIGNAL('message_success'), 'Info',  'Flights have been deleted')
        self.emit(QtCore.SIGNAL('show_total_nr'), '0')
    
    
    def emptyFleet(self):
        self.db.emptyFleet()
        self.emit(QtCore.SIGNAL('message_success'), 'Info',  'Fleets have been deleted')
        self.emit(QtCore.SIGNAL('show_total_nr'), '0')
    
    
    def emptyAircraft(self):
        self.db.emptyAircraft()
        self.emit(QtCore.SIGNAL('message_success'), 'Info',  'All Aircraft have been deleted')
        self.emit(QtCore.SIGNAL('show_total_nr'), '0')

    
    def editFlight(self, params):
        self.db.editFlight(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Flight saved')
    
    
    def editFleet(self, params):
        self.db.editFleet(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Fleet saved')
    
    
    def editAircraft(self, params):
        self.db.editAircraft(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Aircraft saved')

