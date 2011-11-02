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

import os, sqlite3

class FlightsDatabase():
    def __init__(self):
        try:
            self.conn=sqlite3.connect(os.path.join(os.getcwd(), 'database', 'flights.db'))
            self.cursor=self.conn.cursor()
            self.mem_conn=sqlite3.connect(':memory:')
            self.mem_cursor=self.mem_conn.cursor()
        except Exception as eroare:
            print "DB: could not connect to database:",  eroare
            return
    
    
    def loadFlightsInMemory(self):
        self.mem_cursor.execute('CREATE TABLE temp_flights (id INTEGER PRIMARY KEY, callsign TEXT, flt_rules TEXT, dep_day TEXT,\
        dep_airport TEXT, arr_airport TEXT, dep_time TEXT, arr_time TEXT, ac_type TEXT, flt_level INT);')
        self.mem_conn.commit()
        flights=self.getAllFlights()
        for flight in flights:
            for day in str(flight[3]):
                if day.isdigit():
                    insert=(flight[1], flight[2], day, flight[4], flight[5], flight[6], flight[7], flight[8], flight[9])
                    self.mem_cursor.execute('INSERT OR ROLLBACK INTO temp_flights (callsign, flt_rules, dep_day, dep_airport, arr_airport, dep_time, arr_time, ac_type, flt_level) VALUES (?,?,?,?,?,?,?,?,?)', insert)
        self.mem_conn.commit()
    
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
        self.mem_cursor.close()
        self.mem_conn.close()
    
    
    def checkTables(self):
        # table flights: id, callsign, flt_rules, dep_day, dep_airport, arr_airport, dep_time, arr_time, ac_type, flt_level
        # table fleet: id, airline, ac_type, nr_ac, hubs, callsign, designation
        # table aircraft: id, ac_type, designation, offset, radius, fl_type, perf_class, heavy, model
        # table flight_duplicates: id, flight_id, duplicate_score
        # table aircraft_fleet: id, homeport, reg_nr, ac_type, designation, airline, livery ,offset,radius, fl_type,perf_class,heavy,model
        pass 
    
    #hubs: SELECT COUNT(id) AS nr, dep_airport FROM flights WHERE ac_type LIKE '%-CCA' GROUP BY dep_airport ORDER BY nr DESC LIMIT 20;
    
    def dumpDatabase(self):
        fw=open(os.path.join(os.getcwd(),'database', 'flights_dump.sql'),'wb')
        for line in self.conn.iterdump():
            fw.write(line +'\n')
        fw.close()
    
    
    def dropTables(self):
        self.cursor.executescript('DROP TABLE flights;DROP TABLE flight_duplicates;DROP TABLE fleet;DROP TABLE aircraft;DROP TABLE aircraft_fleet;')
    
    
    def execSQL(self, sql):
        self.cursor.executescript(sql)

    
    def commitTransaction(self):
        self.conn.commit()
 
    ## flight duplicates ##
    
    def addDuplicateFlight(self, flight_dupe):
        self.cursor.execute('SELECT COUNT(*) FROM flight_duplicates WHERE flight_id=?', (flight_dupe[0], ))
        nr=self.cursor.fetchone()
        if nr[0]==0:
            self.cursor.execute('INSERT OR ROLLBACK INTO flight_duplicates (flight_id, duplicate_score) VALUES (?,?)', flight_dupe)
    
    
    def getNrDuplicates(self):
        self.cursor.execute('SELECT COUNT(id) FROM flight_duplicates')
        nr=self.cursor.fetchone()
        return nr[0]
    
    
    def getAllDuplicates(self):
        self.cursor.execute('SELECT * FROM flight_duplicates ORDER BY id ASC')
        rows=self.cursor.fetchall()
        return rows
    
    
    def deleteAllDuplicates(self, treshhold=7):
        self.cursor.execute('SELECT * FROM flight_duplicates WHERE duplicate_score >= ? ORDER BY id ASC', (treshhold, ))
        rows=self.cursor.fetchall()
        for row in rows:
            self.cursor.execute('DELETE FROM flights WHERE id=?', (row[1], ))
            self.cursor.execute('DELETE FROM flight_duplicates WHERE id=?', (row[0], ))
        self.conn.commit()
 
    ## flights ##
 
    def getAllFlights(self):
        self.cursor.execute('SELECT * FROM flights ORDER BY id ASC')
        rows=self.cursor.fetchall()
        return rows
    
    
    def getNrFlights(self):
        self.cursor.execute('SELECT COUNT(*) FROM flights ORDER BY id ASC')
        nr=self.cursor.fetchone()
        return nr[0]


    def getFlightInfo(self, index):
        self.cursor.execute('SELECT * FROM flights WHERE id=?', (index, ))
        flight=self.cursor.fetchone()
        return flight
    

    def queryFlights(self, params):
        ## forget about sql injection, must make LIKE % work as expected :)
        query='SELECT flights.*,flight_duplicates.duplicate_score FROM flights LEFT JOIN flight_duplicates ON flights.id=flight_duplicates.flight_id WHERE'
        query_params=[]
        for cond,  value in params.iteritems():
            if cond=='ac_type':
                query=query+' '+cond+' LIKE \''+value+'-%\' AND '
            elif cond=='airline':
                query=query+' '+'ac_type'+' LIKE \'%-'+value+'\' AND '
            elif cond=='dep_day':
                query=query+' '+'dep_day'+' LIKE \'%'+value+'%\' AND '
            elif cond=='callsign':
                query=query+' '+'callsign'+' LIKE \'%'+value+'%\' AND '
            elif cond=='dep_time':
                query=query+' '+'dep_time'+' LIKE \'%'+value+'%\' AND '
            elif cond=='arr_time':
                query=query+' '+'arr_time'+' LIKE \'%'+value+'%\' AND '
            elif cond=='not_id':
                query=query+' flights.id !=? AND '
                query_params.append(value)
            elif cond=='id_larger_than':
                query=query+' flights.id > ? AND '
                query_params.append(value)
            else:
                query=query+' '+cond+'=? AND '
                query_params.append(value)
        query=query+' 1=1 ORDER BY flights.id ASC'
        #print query, query_params
        self.cursor.execute(query, query_params)
        rows=self.cursor.fetchall()
        return rows
    
    
    
    def addFlight(self, flight):
        self.cursor.execute('INSERT OR ROLLBACK INTO flights (callsign, flt_rules, dep_day, dep_airport, arr_airport, dep_time, arr_time, ac_type, flt_level) VALUES (?,?,?,?,?,?,?,?,?)', flight)
        #self.conn.commit() # call commit on the whole chunk to speed things up
    
    
    def editWholeFlight(self, flight):
        self.cursor.execute('UPDATE OR ROLLBACK flights SET callsign=?, flt_rules=?, dep_day=?, dep_airport=?, arr_airport=?, dep_time=?, arr_time=?, ac_type=?, flt_level=? WHERE id=?', flight)
        self.conn.commit()
    
    
    def editFlight(self, params):
        query="UPDATE OR ROLLBACK flights SET "+params[0][0]+"=? WHERE id=?"
        self.cursor.execute(query, (params[0][1], params[1][1]))
        self.conn.commit()
    
    
    def deleteFlight(self, flight):
        self.cursor.execute('DELETE FROM flights WHERE id=?', (flight, ))
    
    
    def emptyFlights(self):
        self.cursor.execute('DELETE FROM flights')
        self.cursor.execute('DELETE FROM flight_duplicates')
        self.conn.commit()


    ## fleets ##

    def addFleet(self, fleet_item):
        self.cursor.execute('INSERT OR ROLLBACK INTO fleet (airline, ac_type, nr_ac, hubs, callsign, designation) VALUES (?,?,?,?,?,?)', fleet_item)
    
    
    def getAllFleets(self):
        self.cursor.execute('SELECT * FROM fleet ORDER BY id ASC')
        rows=self.cursor.fetchall()
        return rows
    
    
    def getDistinctAirlinesFromFleets(self):
        self.cursor.execute('SELECT DISTINCT airline FROM fleet ORDER BY id ASC')
        rows=self.cursor.fetchall()
        airlines=[]
        for row in rows:
            airlines.append(row[0])
        return airlines
    
    
    def getAirlineFleets(self, airline):
        self.cursor.execute('SELECT * FROM fleet WHERE airline=? ORDER BY id ASC', (airline, ))
        rows=self.cursor.fetchall()
        return rows
    
    
    def getNrFleets(self):
        self.cursor.execute('SELECT COUNT(*) FROM fleet ORDER BY id ASC')
        nr=self.cursor.fetchone()
        return nr[0]


    def getFleetInfo(self, index):
        self.cursor.execute('SELECT * FROM fleet WHERE id=?', (index, ))
        flight=self.cursor.fetchone()
        return flight
    

    def queryFleet(self, params):
        ## forget about sql injection, must make LIKE % work as expected :)
        query='SELECT * FROM fleet WHERE'
        query_params=[]
        for cond,  value in params.iteritems():
            if cond=='ac_type':
                query=query+' '+cond+' LIKE \''+value+'%\' AND '
            elif cond=='airline':
                query=query+' '+'airline'+' LIKE \'%'+value+'\' AND '
            elif cond=='hubs':
                query=query+' '+'hubs'+' LIKE \'%'+value+'%\' AND '
            elif cond=='callsign':
                query=query+' '+'callsign'+' LIKE \'%'+value+'%\' AND '
            elif cond=='designation':
                query=query+' '+'designation'+' LIKE \'%'+value+'%\' AND '
            else:
                query=query+' '+cond+'=? AND '
                query_params.append(value)
        query=query+' 1=1 ORDER BY id ASC'
        #print query, query_params
        self.cursor.execute(query, query_params)
        rows=self.cursor.fetchall()
        return rows
    
    
    def editFleet(self, params):
        query="UPDATE OR ROLLBACK fleet SET "+params[0][0]+"=? WHERE id=?"
        self.cursor.execute(query, (params[0][1], params[1][1]))
        self.conn.commit()
    
    
    def deleteFleet(self, fleet):
        self.cursor.execute('DELETE FROM fleet WHERE id=?', (fleet, ))
    
    
    def emptyFleet(self):
        self.cursor.execute('DELETE FROM fleet')
        self.conn.commit()
    
    
    ## aircraft ##
    
    def addAircraft(self, aircraft):
        self.cursor.execute('INSERT OR ROLLBACK INTO aircraft (ac_type, designation, offset, radius, fl_type, perf_class, heavy, model) VALUES (?,?,?,?,?,?,?,?)', aircraft)
    
    
    def getAllAircraft(self):
        self.cursor.execute('SELECT * FROM aircraft ORDER BY id ASC')
        rows=self.cursor.fetchall()
        return rows
        
    
    def getNrAircraft(self):
        self.cursor.execute('SELECT COUNT(*) FROM aircraft ORDER BY id ASC')
        nr=self.cursor.fetchone()
        return nr[0]


    def getAircraftInfo(self, index):
        self.cursor.execute('SELECT * FROM aircraft WHERE ac_type=?', (index, ))
        aircraft=self.cursor.fetchone()
        return aircraft
    

    def queryAircraft(self, params):
        ## forget about sql injection, must make LIKE % work as expected :)
        query='SELECT * FROM aircraft WHERE'
        query_params=[]
        for cond,  value in params.iteritems():
            if cond=='ac_type':
                query=query+' '+cond+' LIKE \''+value+'%\' AND '
            elif cond=='designation':
                query=query+' '+'designation'+' LIKE \'%'+value+'\' AND '
            elif cond=='fl_type':
                query=query+' '+'fl_type'+' LIKE \'%'+value+'%\' AND '
            elif cond=='perf_class':
                query=query+' '+'perf_class'+' LIKE \'%'+value+'%\' AND '
            elif cond=='heavy':
                query=query+' '+'heavy'+' LIKE \'%'+value+'%\' AND '
            elif cond=='model':
                query=query+' '+'model'+' LIKE \'%'+value+'%\' AND '
            else:
                query=query+' '+cond+'=? AND '
                query_params.append(value)
        query=query+' 1=1 ORDER BY id ASC'
        #print query, query_params
        self.cursor.execute(query, query_params)
        rows=self.cursor.fetchall()
        return rows
    

    def editAircraft(self, params):
        query="UPDATE OR ROLLBACK aircraft SET "+params[0][0]+"=? WHERE id=?"
        self.cursor.execute(query, (params[0][1], params[1][1]))
        self.conn.commit()
    
    
    def deleteAircraft(self, aircraft):
        self.cursor.execute('DELETE FROM aircraft WHERE id=?', (aircraft, ))

    
    def emptyAircraft(self):
        self.cursor.execute('DELETE FROM aircraft')
        self.conn.commit()
    
    
    def missingAircraftTypes(self):
        self.cursor.execute('SELECT DISTINCT ac_type FROM flights ORDER BY ac_type ASC')
        rows=self.cursor.fetchall()
        acs1=[]
        acs2=[]
        for row in rows:
            ac=str(row[0])
            stubs=ac.split("-")
            ac=stubs[0]
            if ac not in acs1:
                acs1.append(ac)
        self.cursor.execute('SELECT ac_type FROM aircraft ORDER BY ac_type ASC')
        rows2=self.cursor.fetchall()
        for row in rows2:
            ac=str(row[0])
            if ac not in acs2:
                acs2.append(ac)
        set1=set(acs1)
        set2=set(acs2)
        diff=set1-set2
        for ac in diff:
            self.cursor.execute('INSERT OR ROLLBACK INTO aircraft (ac_type, designation, offset, radius, fl_type, perf_class, heavy, model) VALUES (?,"","","","","","","")', (ac, ))
        self.conn.commit()
    
    
    ## aircraft fleet ##
    
    def checkUniqueRegNr(self, reg_nr):
        self.cursor.execute('SELECT COUNT(*) FROM aircraft_fleet WHERE reg_nr=? ORDER BY id ASC', (reg_nr, ))
        nr=self.cursor.fetchone()
        return nr[0]
    
    def addAircraftFleet(self, aircraft):
        self.cursor.execute('INSERT OR ROLLBACK INTO aircraft_fleet (homeport, reg_nr, ac_type, designation, airline, livery, offset, radius, fl_type, perf_class, heavy, model) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)', aircraft)
    
    
    def getAllAircraftFleet(self):
        self.cursor.execute('SELECT * FROM aircraft_fleet ORDER BY id ASC')
        rows=self.cursor.fetchall()
        return rows
        
    
    def getNrAircraftFleet(self):
        self.cursor.execute('SELECT COUNT(*) FROM aircraft_fleet ORDER BY id ASC')
        nr=self.cursor.fetchone()
        return nr[0]


    def getAircraftFleetInfo(self, index):
        self.cursor.execute('SELECT * FROM aircraft_fleet WHERE ac_type=?', (index, ))
        aircraft=self.cursor.fetchone()
        return aircraft
    

    def queryAircraftFleet(self, params):
        ## forget about sql injection, must make LIKE % work as expected :)
        query='SELECT * FROM aircraft_fleet WHERE'
        query_params=[]
        for cond,  value in params.iteritems():
            if cond=='reg_nr':
                query=query+' '+cond+' LIKE \'%'+value+'%\' AND '
            elif cond=='designation':
                query=query+' '+'designation'+' LIKE \'%'+value+'%\' AND '
            elif cond=='fl_type':
                query=query+' '+'fl_type'+' LIKE \'%'+value+'%\' AND '
            elif cond=='perf_class':
                query=query+' '+'perf_class'+' LIKE \'%'+value+'%\' AND '
            elif cond=='heavy':
                query=query+' '+'heavy'+' LIKE \'%'+value+'%\' AND '
            elif cond=='model':
                query=query+' '+'model'+' LIKE \'%'+value+'%\' AND '
            else:
                query=query+' '+cond+'=? AND '
                query_params.append(value)
        query=query+' 1=1 ORDER BY id ASC'
        #print query, query_params
        self.cursor.execute(query, query_params)
        rows=self.cursor.fetchall()
        return rows
    

    def emptyAircraftFleet(self):
        self.cursor.execute('DELETE FROM aircraft_fleet')
        self.conn.commit()
    
    
    
    
    

