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


import os, sys, glob, io, random, shutil
from PyQt4 import QtCore
from database import FlightsDatabase


class  DatabaseThread(QtCore.QThread):
    
    def __init__(self,  parent=None):
        QtCore.QThread.__init__(self, parent)
        self.db=FlightsDatabase()
        self.fgdata_path=''
        self.move_flightplans=''

    
    def __del__(self):
        del self.db
        self.exit(1)
    
    
    def run(self):
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
                try:
                    os.stat(self.fgdata_path)
                except:
                    self.fgdata_path=''
                    print 'Fgdata path could not be found in settings'
                    self.emit(QtCore.SIGNAL('message_success'), 'Error','Fgdata path could not be found in settings. Livery checking will not work correctly.')
                break
            else:
                print 'Fgdata path could not be found in settings'
                self.emit(QtCore.SIGNAL('message_success'), 'Error','Fgdata path could not be found in settings. Livery checking will not work correctly.')
        for line in settings:
            if line.find('move_flightplans=')!=-1:
                tmp=line.split('=')
                move=tmp[1].rstrip('\n')
                move=move.lstrip()
                self.move_flightplans=move.rstrip()
        self.exec_()

    
    def loadDBFromSQL(self, filename):
        fr=open(filename, 'rb')
        content=fr.readlines()
        progress_overall=0
        progress_overall_step=100 / len(content)
        self.db.dropTables()
        for line in content:
            self.db.execSQL(line)
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
        self.db.commitTransaction()
        self.emit(QtCore.SIGNAL('import_progress'), 100)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Database loaded succesfully')
    
    
    def dumpDatabase(self):
        self.db.dumpDatabase()
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Database dumped to text file')
    
    
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
                    if line.find('#')==0 or len(line)<2 or line.find('FLIGHT')==-1:
                        continue
                    stubs1=line.split()
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
                    bufs=[]
                    params=dict({'airline':airline})
                    flights=self.db.queryFlights(params)
                    for flight in flights:
                        conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                        +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                        bufs.append(conf)
                        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                    buf="".join(bufs)
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
                    bufs=[]
                    for flight in flights:
                        if str(flight[8][4:])==airline:
                            conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                            +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                            bufs.append(conf)
                        QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                    buf="".join(bufs)
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
                bufs=[]
                for flight in flights:
                    conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                    +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                    bufs.append(conf)
                    progress_overall=progress_overall+progress_overall_step
                    self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                buf="".join(bufs)
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
                bufs=[]
                for flight in flights:
                    conf = "FLIGHT   "+str(flight[1])+"   "+str(flight[2])+"   "+str(flight[3])+"   "+str(flight[6])+"   "+str(flight[4]) \
                    +"   "+str(flight[7])+"   "+str(flight[5])+"   "+str(flight[9])+"   "+str(flight[8])+"\n"
                    bufs.append(conf)
                    progress_overall=progress_overall+progress_overall_step
                    self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                buf="".join(bufs)
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
        bufs=[]
        for fleet in fleets:
            conf = "ENTRY   "+str(fleet[1])+"   "+str(fleet[2])+"   "+str(fleet[3])+"   "+str(fleet[4])+"   "+str(fleet[5])+"   "+str(fleet[6])+"\n"
            bufs.append(conf)
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        buf="".join(bufs)
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
        bufs=[]
        for ac in aircraft:
            conf = str(ac[1])+"   "+str(ac[2])+"   "+str(ac[3])+"   "+str(ac[4])+"   "+str(ac[5])+"   "+str(ac[6])+"   "+str(ac[7])+"   "+str(ac[8])+"\n"
            bufs.append(conf)
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        #file_content="###Airline   Ac. Type   Nr. Aircraft     Hubs     Callsign    Designation\n"+\
        #"######### ######### ####### ############### ############### #################\n\n"+buf
        buf="".join(bufs)
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
        res_f=[]
        needed_ac=[]
        for r in res:
            ac_info=self.db.getAircraftInfo(str(r[2]))
            model = str(ac_info[8])
            path=os.path.join(self.fgdata_path, 'AI', model+str(r[6])+'.xml')
            try:
                if os.stat(path)!=-1:
                    t=(r[0], r[1], r[2], r[3], r[4], r[5], r[6], 1)
            except:
                ac=model+str(r[6])+'.xml'
                if ac not in needed_ac:
                    needed_ac.append(ac)
                t=(r[0], r[1], r[2], r[3], r[4], r[5], r[6], 0)
            res_f.append(t)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.emit(QtCore.SIGNAL('ready_results_fleet'), res_f)
        if len(params)==0:
            fw=open(os.path.join(os.getcwd(), 'fleet_info','needed_aircraft.txt'),'wb')
            buf=''
            for ac in needed_ac:
                buf+= ac+'\n'
            fw.write(buf)
            fw.close()
    
    
    def runQueryAircraft(self, params):
        res=self.db.queryAircraft(params)
        self.emit(QtCore.SIGNAL('ready_results_aircraft'), res)
    
    
    def runQueryAircraftFleet(self, params):
        res=self.db.queryAircraftFleet(params)
        self.emit(QtCore.SIGNAL('ready_results_aircraft_fleet'), res)
    
    
    def getNrFlights(self):
        res=self.db.getNrFlights()
        dupes=self.db.getNrDuplicates()
        self.emit(QtCore.SIGNAL('show_total_nr'), str(res), str(dupes))
    
    
    def getNrFleets(self):
        res=self.db.getNrFleets()
        self.emit(QtCore.SIGNAL('show_total_nr_fleets'), str(res))
    
    
    def getNrAircraft(self):
        res=self.db.getNrAircraft()
        self.emit(QtCore.SIGNAL('show_total_nr_aircraft'), str(res))
    
    
    def getNrAircraftFleet(self):
        res=self.db.getNrAircraftFleet()
        self.emit(QtCore.SIGNAL('show_total_nr_aircraft_fleet'), str(res))
    
    
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
        self.emit(QtCore.SIGNAL('show_total_nr_fleets'), '0')
    
    
    def emptyAircraft(self):
        self.db.emptyAircraft()
        self.emit(QtCore.SIGNAL('message_success'), 'Info',  'All Aircraft have been deleted')
        self.emit(QtCore.SIGNAL('show_total_nr_aircraft'), '0')
    
    
    def emptyAircraftFleet(self):
        self.db.emptyAircraftFleet()
        self.emit(QtCore.SIGNAL('message_success'), 'Info',  'All Aircraft have been deleted')
        self.emit(QtCore.SIGNAL('show_total_nr_aircraft_fleet'), '0')

    
    def editFlight(self, params):
        self.db.editFlight(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Flight saved')
    
    
    def editFleet(self, params):
        self.db.editFleet(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Fleet saved')
    
    
    def editAircraft(self, params):
        self.db.editAircraft(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Aircraft saved')
    
    
    def addFlight(self, params):
        self.db.addFlight(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Flight saved')
    
    
    def addFleet(self, params):
        self.db.addFleet(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Fleet saved')
    
    
    def addAircraft(self, params):
        self.db.addAircraft(params)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Aircraft saved')
    
    
    def getMissingAircraft(self):
        self.db.missingAircraftTypes()
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Missing Aircraft added')
    
    
    def getAirlines(self):
        airlines=self.db.getDistinctAirlinesFromFleets()
        self.emit(QtCore.SIGNAL('fleet_airlines'), airlines)

    
    def generateAllAircraftFleets(self):
        airlines=self.db.getDistinctAirlinesFromFleets()
        skipped=0
        progress_overall=0
        progress_overall_step=100 / len(airlines)
        for airline in airlines:
            skip=self.generateAircraftFleet(airline, 1)
            skipped=skipped+skip
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','All aircraft fleet written in the <b>exported_aircraft</b> directory; <b>'+str(skipped)+'</b> aircraft skipped')
        self.emit(QtCore.SIGNAL('import_progress'), 100)
    
    
    def generateAllAircraftFleetsTable(self):
        airlines=self.db.getDistinctAirlinesFromFleets()
        skipped=0
        progress_overall=0
        progress_overall_step=100 / len(airlines)
        for airline in airlines:
            skip=self.generateAircraftFleetTable(airline, 1)
            skipped=skipped+skip
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','The aircraft table has been regenerated; <b>'+str(skipped)+'</b> aircraft skipped')
        self.emit(QtCore.SIGNAL('import_progress'), 100)
    
    #TODO: this code will no longer be used and will be ported to SQL below
    """ 
    def generateAircraftFleet(self, airline, everything=None):
        if len(airline)!=3:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline designation most likely wrong')
            return
        fleets=self.db.getAirlineFleets(airline)
        callsigns=[]
        skipped=0
        buf=''
        bufs=[]
        for fleet in fleets:
            for i in range(0, int(fleet[3])):
                acdata=self.db.getAircraftInfo(str(fleet[2]))
                homeports=str(fleet[4]).split(',')
                port_nr=random.randint(0, len(homeports)-1)
                homeport=homeports[port_nr]
                callsign=str(fleet[5])
                while 1:
                    callsign=str(fleet[5])
                    while callsign.find('%d')!=-1:
                        callsign=callsign.replace('%d', self.randCallsign('d'), 1)
                    while callsign.find('%s')!=-1:
                        callsign=callsign.replace('%s', self.randCallsign('s'), 1)
                    if callsign not in callsigns:
                        callsigns.append(callsign)
                        break
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                ac_designation=str(acdata[2])
                ac_type=str(fleet[2])
                airline=str(fleet[1])
                model=str(acdata[8])+str(fleet[6])+'.xml'
                try:
                    os.stat(os.path.join(self.fgdata_path, 'AI', model))
                except:
                    skipped=skipped+1
                    continue
                offset=str(acdata[3])
                radius=str(acdata[4])
                fl_type=str(acdata[5])
                perf_class=str(acdata[6])
                heavy=str(acdata[7])
                if homeport=='' or callsign=='' or ac_type=='' or ac_designation=='' or airline=='' \
                    or offset=='' or radius=='' or fl_type=='' or perf_class=='' or heavy=='' or model=='':
                    skipped=skipped+1
                    continue

                conf='AC   '+homeport+'   '+callsign+'   '+ac_type+'   '+ac_designation\
                    +'   '+airline+'   '+airline+'   '+offset+'   '+radius+'   '+fl_type\
                    +'   '+perf_class+'   '+heavy+'   '+model+'\n'
                bufs.append(conf)
        buf="".join(bufs)
        if buf=='':
            if everything==None:
                self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline '+airline+' has no valid aircraft; none written to disk')
            return
        conf_file="###HOMEP RegNo  TypeCode        Type    AirLine         Livery  Offset  Radius  FltType Perf.Class      Heavy   Model\n" +\
        "############################################################################################################################################\n\n"+buf
        fw=open(os.path.join(os.getcwd(),'exported_aircraft', str(airline)+'-ac.conf'),'wb')
        fw.write(conf_file)
        fw.close()
        if everything==None:
            self.emit(QtCore.SIGNAL('message_success'), 'Info','Airline aircraft fleet written in the <b>exported_aircraft</b> directory; <b>'+str(skipped)+'</b> aircraft skipped')
        else:
            return skipped
    """
    
    def generateAircraftFleet(self, airline, everything=None):
        if len(airline)!=3:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline designation most likely wrong')
            return
        parameters=dict([('airline', airline)])
        aircraft_fleet=self.db.queryAircraftFleet(parameters)
        buf=''
        bufs=[]
        for ac in aircraft_fleet:
            homeport=str(ac[1])
            callsign=str(ac[2])
            ac_type=str(ac[3])
            ac_designation=str(ac[4])
            airline=str(ac[5])
            livery=str(ac[6])
            offset=str(ac[7])
            radius=str(ac[8])
            fl_type=str(ac[9])
            perf_class=str(ac[10])
            heavy=str(ac[11])
            model=str(ac[12])
        
            conf='AC   '+homeport+'   '+callsign+'   '+ac_type+'   '+ac_designation\
                +'   '+airline+'   '+livery+'   '+offset+'   '+radius+'   '+fl_type\
                +'   '+perf_class+'   '+heavy+'   '+model+'\n'
            bufs.append(conf)
        buf="".join(bufs)
        if buf=='':
            if everything==None:
                self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline '+airline+' has no valid aircraft; none written to disk')
            return
        conf_file="###HOMEP RegNo  TypeCode        Type    AirLine         Livery  Offset  Radius  FltType Perf.Class      Heavy   Model\n" +\
        "############################################################################################################################################\n\n"+buf
        fw=open(os.path.join(os.getcwd(),'exported_aircraft', str(airline)+'-ac.conf'),'wb')
        fw.write(conf_file)
        fw.close()
        if everything==None:
            self.emit(QtCore.SIGNAL('message_success'), 'Info','Airline aircraft fleet written in the <b>exported_aircraft</b> directory; <b>'+str(skipped)+'</b> aircraft skipped')
        else:
            return skipped
    
    
    def generateAircraftFleetTable(self, airline, everything=None):
        if len(airline)!=3:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline designation most likely wrong')
            return
        fleets=self.db.getAirlineFleets(airline)
        callsigns=[]
        skipped=0
        buf=''
        bufs=[]
        for fleet in fleets:
            for i in range(0, int(fleet[3])):
                acdata=self.db.getAircraftInfo(str(fleet[2]))
                homeports=str(fleet[4]).split(',')
                port_nr=random.randint(0, len(homeports)-1)
                homeport=homeports[port_nr]
                callsign=str(fleet[5])
                while 1:
                    callsign=str(fleet[5])
                    while callsign.find('%d')!=-1:
                        callsign=callsign.replace('%d', self.randCallsign('d'), 1)
                    while callsign.find('%s')!=-1:
                        callsign=callsign.replace('%s', self.randCallsign('s'), 1)
                    if (callsign not in callsigns) and (self.db.checkUniqueRegNr(callsign)==0):
                        callsigns.append(callsign)
                        break
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                ac_designation=str(acdata[2])
                ac_type=str(fleet[2])
                airline=str(fleet[1])
                model=str(acdata[8])+str(fleet[6])+'.xml'
                try:
                    os.stat(os.path.join(self.fgdata_path, 'AI', model))
                except:
                    skipped=skipped+1
                    continue
                offset=str(acdata[3])
                radius=str(acdata[4])
                fl_type=str(acdata[5])
                perf_class=str(acdata[6])
                heavy=str(acdata[7])
                if homeport=='' or callsign=='' or ac_type=='' or ac_designation=='' or airline=='' \
                    or offset=='' or radius=='' or fl_type=='' or perf_class=='' or heavy=='' or model=='':
                    skipped=skipped+1
                    continue

                #conf='AC   '+homeport+'   '+callsign+'   '+ac_type+'   '+ac_designation\
                #    +'   '+airline+'   '+airline+'   '+offset+'   '+radius+'   '+fl_type\
                #   +'   '+perf_class+'   '+heavy+'   '+model+'\n'
                self.db.addAircraftFleet((homeport, callsign, ac_type, ac_designation, airline, airline, offset, radius, fl_type, perf_class, heavy, model))
        self.db.commitTransaction()
        if len(callsigns)==0:
            if everything==None:
                self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline '+airline+' has no valid aircraft; none written to disk')
            return
        if everything==None:
            self.emit(QtCore.SIGNAL('message_success'), 'Info','Aircraft fleet added to database table; <b>'+str(skipped)+'</b> aircraft skipped')
        else:
            return skipped
    
    
    def randCallsign(self, token):
        letters="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        numbers="0123456789"
        if token=='d':
            number_nr=random.randint(0, len(numbers)-1)
            number=numbers[number_nr]
            return number
        elif token=='s':
            letter_nr=random.randint(0, len(letters)-1)
            letter=letters[letter_nr]
            return letter
        else:
            return 0
    
    #TODO: this code will no longer be used and will be ported to SQL below
    def generateAircraftXML_old(self, airline):
        if len(airline)!=3:
            return ''
        fleets=self.db.getAirlineFleets(airline)
        callsigns=[]
        skipped=0
        bufs=[]
        buf=''
        for fleet in fleets:
            for i in range(0, int(fleet[3])):
                acdata=self.db.getAircraftInfo(str(fleet[2]))
                homeports=str(fleet[4]).split(',')
                port_nr=random.randint(0, len(homeports)-1)
                homeport=homeports[port_nr]
                callsign=str(fleet[5])
                while 1:
                    callsign=str(fleet[5])
                    while callsign.find('%d')!=-1:
                        callsign=callsign.replace('%d', self.randCallsign('d'), 1)
                    while callsign.find('%s')!=-1:
                        callsign=callsign.replace('%s', self.randCallsign('s'), 1)
                    if callsign not in callsigns:
                        callsigns.append(callsign)
                        break
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
                ac_designation=str(acdata[2])
                ac_type=str(fleet[2])
                airline=str(fleet[1])
                model=str(acdata[8])+str(fleet[6])+'.xml'
                try:
                    os.stat(os.path.join(self.fgdata_path, 'AI', model))
                except:
                    skipped=skipped+1
                    continue
                offset=str(acdata[3])
                radius=str(acdata[4])
                fl_type=str(acdata[5])
                perf_class=str(acdata[6])
                heavy=str(acdata[7])
                if homeport=='' or callsign=='' or ac_type=='' or ac_designation=='' or airline=='' \
                    or offset=='' or radius=='' or fl_type=='' or perf_class=='' or heavy=='' or model=='':
                    skipped=skipped+1
                    continue
                
                buf="""
        <aircraft>
            <model>"""+model+"""</model>
            <livery>"""+airline+"""</livery>
            <airline>"""+airline+"""</airline>
            <home-port>"""+homeport+"""</home-port>
            <required-aircraft>"""+ac_type+'-'+airline+"""</required-aircraft>
            <actype>"""+ac_designation+"""</actype>
            <offset>"""+offset+"""</offset>
            <radius>"""+radius+"""</radius>
            <flighttype>"""+fl_type+"""</flighttype>
            <performance-class>"""+perf_class+"""</performance-class>
            <registration>"""+callsign+"""</registration>
            <heavy>"""+heavy+"""</heavy>
        </aircraft>"""
                bufs.append(buf)
                
        res="".join(bufs)
        return res
    
    
    def generateAircraftXML(self, airline):
        if len(airline)!=3:
            return ''
        parameters=dict([('airline', airline)])
        aircraft_fleet=self.db.queryAircraftFleet(parameters)
        buf=''
        bufs=[]
        for ac in aircraft_fleet:
            homeport=str(ac[1])
            callsign=str(ac[2])
            ac_type=str(ac[3])
            ac_designation=str(ac[4])
            airline=str(ac[5])
            livery=str(ac[6])
            offset=str(ac[7])
            radius=str(ac[8])
            fl_type=str(ac[9])
            perf_class=str(ac[10])
            heavy=str(ac[11])
            model=str(ac[12])
            
            buf="""
        <aircraft>
            <model>"""+model+"""</model>
            <livery>"""+livery+"""</livery>
            <airline>"""+airline+"""</airline>
            <home-port>"""+homeport+"""</home-port>
            <required-aircraft>"""+ac_type+'-'+airline+"""</required-aircraft>
            <actype>"""+ac_designation+"""</actype>
            <offset>"""+offset+"""</offset>
            <radius>"""+radius+"""</radius>
            <flighttype>"""+fl_type+"""</flighttype>
            <performance-class>"""+perf_class+"""</performance-class>
            <registration>"""+callsign+"""</registration>
            <heavy>"""+heavy+"""</heavy>
        </aircraft>"""
            bufs.append(buf)
            
        res="".join(bufs)
        return res
    
    
    def generateFlightsXML(self, airline):
        if len(airline)!=3:
            return ''
        buf=''
        bufs=[]
        params=dict({'airline':airline})
        flights=self.db.queryFlights(params)
        for flight in flights:
            callsign=str(flight[1])
            flt_rules=str(flight[2])
            dep_days=str(flight[3])
            dep_airport=str(flight[4])
            arr_airport=str(flight[5])
            dep_time=str(flight[6])
            dep_int=int(dep_time[0:2])
            arr_time=str(flight[7])
            arr_int=int(arr_time[0:2])
            ac_type=str(flight[8])
            flt_level=str(flight[9])
            for i in dep_days:
                if i.isdigit():
                    k=i
                    if arr_int<dep_int:
                        i=int(i)
                        k=i+1
                        if k > 7:
                            k=1
                    i=str(int(i))
                    k=str(int(k))
                    if i =='7':
                        i='0'
                    if k =='7':
                        k='0'
                    buf="""
        <flight>
            <callsign>"""+callsign+"""</callsign>
            <required-aircraft>"""+ac_type+"""</required-aircraft>
            <fltrules>"""+flt_rules+"""</fltrules>
            <departure>
                <port>"""+dep_airport+"""</port>
                <time>"""+i+'/'+dep_time+""":00</time>
            </departure>
            <cruise-alt>"""+flt_level+"""</cruise-alt>
            <arrival>
                <port>"""+arr_airport+"""</port>
                <time>"""+k+'/'+arr_time+""":00</time>
            </arrival>
            <repeat>WEEK</repeat>
        </flight>"""
                    bufs.append(buf)
                    QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        res="".join(bufs)
        return res
    
    
    def generateAllAirlinesXML(self):
        airlines=self.db.getDistinctAirlinesFromFleets()
        skipped=0
        progress_overall=0
        progress_overall_step=100 / len(airlines)
        head='<?xml version="1.0"?>\n<trafficlist>'
        foot='\n</trafficlist>\n'
        for airline in airlines:
            ac=self.generateAircraftXML(airline)
            if ac=='':
                skipped=skipped+1
                continue
            flights=self.generateFlightsXML(airline)
            if flights=='':
                skipped=skipped+1
                continue
            fw=open(os.path.join(os.getcwd(),'flightplans', str(airline)+'.xml'),'wb')
            fw.write(head+ac+flights+foot)
            fw.close()
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            letter=airline[0:1].upper()
            if self.fgdata_path!='' and self.move_flightplans=='true':
                try:
                    os.stat(os.path.join(self.fgdata_path, 'AI', 'Traffic', letter))
                    shutil.copy(os.path.join(os.getcwd(),'flightplans', str(airline)+'.xml'), os.path.join(self.fgdata_path, 'AI', 'Traffic', letter))
                    self.emit(QtCore.SIGNAL('message_success'), 'Info','Flightplan <b>'+airline+'</b> moved to FGDATA directory')
                except:
                    self.emit(QtCore.SIGNAL('message_success'), 'Error','Flightplan <b>'+airline+'</b> could not be moved to FGDATA directory')
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        self.emit(QtCore.SIGNAL('message_success'), 'Info','Flightplans written in the <b>flightplans</b> directory; <b>'+str(skipped)+'</b> airlines skipped')
        self.emit(QtCore.SIGNAL('import_progress'), 100)

    
    def generateAirlineXML(self, airline):
        if len(airline)!=3:
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline doesn\'t seem to be valid')
            return 
        head='<?xml version="1.0"?>\n<trafficlist>'
        foot='\n</trafficlist>\n'
        self.emit(QtCore.SIGNAL('import_progress'), 5)
        ac=self.generateAircraftXML(airline)
        self.emit(QtCore.SIGNAL('import_progress'), 35)
        if ac=='':
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline has no available aircraft')
            return
        flights=self.generateFlightsXML(airline)
        self.emit(QtCore.SIGNAL('import_progress'), 85)
        if flights=='':
            self.emit(QtCore.SIGNAL('message_success'), 'Error','Airline has no flight schedules')
            return
        fw=open(os.path.join(os.getcwd(),'flightplans', str(airline)+'.xml'),'wb')
        fw.write(head+ac+flights+foot)
        fw.close()
        letter=airline[0:1].upper()
        if self.fgdata_path!='' and self.move_flightplans=='true':
            try:
                os.stat(os.path.join(self.fgdata_path, 'AI', 'Traffic', letter))
                shutil.copy(os.path.join(os.getcwd(),'flightplans', str(airline)+'.xml'), os.path.join(self.fgdata_path, 'AI', 'Traffic', letter))
                self.emit(QtCore.SIGNAL('message_success'), 'Info','Flightplan <b>'+airline+'</b> moved to FGDATA directory')
            except:
                self.emit(QtCore.SIGNAL('message_success'), 'Error','Flightplan <b>'+airline+'</b> could not be moved to FGDATA directory')
        else:
            self.emit(QtCore.SIGNAL('message_success'), 'Info','Flightplan <b>'+airline+'</b> written in the <b>flightplans</b> directory')
        self.emit(QtCore.SIGNAL('import_progress'), 100)
    
    
    def dupeCandidates(self, airline):
        flights1=[]
        if airline!=None:
            params=dict({'airline':airline})
            flights1=self.db.queryFlights(params)
        else:
            flights1=self.db.getAllFlights()
        if len(flights1) < 1:
            return
        flights2=[]
        searched=[]
        rows=self.db.getAllDuplicates()
        duplicate_ids=[row[1] for row in rows ]
        progress_overall=0
        progress_overall_step=float(100) / float(len(flights1))
        for flight in flights1:
            ##don't try to find dupes for the dupes
            if int(str(flight[0])) in searched or int(str(flight[0])) in duplicate_ids:
                progress_overall=progress_overall+progress_overall_step
                self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
                continue
            ac_type1=str(flight[8])
            ac_type=ac_type1[0:3]
            airline=ac_type1[4:]
            days=str(flight[3])
            numeric_days=[]
            for day in days:
                if day.isdigit():
                    numeric_days.append(day)
            line=( str(flight[0]),  str(flight[1]), str(flight[2]), str(flight[3]), str(flight[4]), str(flight[5]), str(flight[6]), str(flight[7]), str(flight[8]), str(flight[9]), str(flight[10]) )
            conditions=[]
            conditions.append(('dep_airport', str(flight[4])))
            conditions.append(('arr_airport', str(flight[5])))
            conditions.append(('dep_time', str(flight[6])))
            #conditions.append(('ac_type', ac_type))
            conditions.append(('not_id', int(str(flight[0]))))
            conditions.append(('airline', airline))
            params=dict(conditions)
            res=self.db.queryFlights(params)
            
            for row in res:
                if int(str(row[0])) in searched:
                    continue
                dupe_days=[]
                numeric_days2=[]
                dupe_score=0
                rev_dupe_score=0
                line2=( str(row[0]),  str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]), str(row[7]), str(row[8]), str(row[9]), str(row[10]) )
                days2=str(row[3])
                for day2 in days2:
                    if day2.isdigit():
                        numeric_days2.append(day2)
                        if day2 in days:
                            dupe_days.append(day2)
                
                dupe_days=set(dupe_days)
                if len(dupe_days)==0:
                    continue
                numeric_days2=set(numeric_days2)
                numeric_days=set(numeric_days)
                if len(numeric_days2) <= len(numeric_days):
                    dupe_score= 7 - len(numeric_days2-dupe_days)
                    if line2 not in flights2:
                        flights2.append(line2)
                        flight_dupe=( int( line2[0]  ),  dupe_score)
                        self.db.addDuplicateFlight(flight_dupe)
                    if int( str(row[0]) ) not in searched:
                        searched.append( int( str(row[0]) ) )
                elif len(numeric_days2) > len(numeric_days):
                    rev_dupe_score= 7 - len(numeric_days-dupe_days)
                    if line not in flights2:
                        flights2.append(line)
                        flight_dupe=( int( line[0] ),  rev_dupe_score)
                        self.db.addDuplicateFlight(flight_dupe)
                    if int( str(flight[0]) ) not in searched:
                        searched.append( int( str(flight[0]) ) )
                
            progress_overall=progress_overall+progress_overall_step
            self.emit(QtCore.SIGNAL('import_progress'), progress_overall)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
        if len(flights2) >0:
            self.db.commitTransaction()
        self.emit(QtCore.SIGNAL('ready_results'), flights2)
        self.emit(QtCore.SIGNAL('import_progress'), 100)
