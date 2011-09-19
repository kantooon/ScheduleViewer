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
        del self.db
        return
    
    
    def importConfs(self, path):
        conf_files=glob.glob(path+'/*/*.conf')
        try:
            for conf in conf_files:
                fr=open(conf,'rb')
                content= fr.readlines()
                for line in content:
                    if line.find('#')==0 or len(line)<2:
                        continue
                    stubs1=line.split("   ")
                    for i in stubs1[3]:
                        if i.isdigit():
                            flight=[stubs1[1],stubs1[2],i,stubs1[5],stubs1[7],stubs1[4],stubs1[6],stubs1[9],stubs1[8]]
                            self.db.addFlight(flight)
            self.emit(QtCore.SIGNAL('message_success'), 'Info','Flights have been imported')
        except:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Flights could not be imported')
        
    
    
    def exportConfs(self, path):
        pass 
    
    
    def runQuery(self, params):
        res=self.db.queryFlights(params)
        self.emit(QtCore.SIGNAL('ready_results'), res)
    
    
    def getNrFlights(self):
        res=self.db.getNrFlights()
        self.emit(QtCore.SIGNAL('show_total_nr'), str(res))
    
    
    def deleteFlights(self, flightlist):
        for flight in flightlist:
            self.db.deleteFlight(flight)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Flights have been deleted')
        
    
    def emptyFlights(self):
        self.db.emptyFlights()
        self.emit(QtCore.SIGNAL('message_success'), 'Info',  'Flights have been deleted')

    
