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
        except Exception as eroare:
            print "DB: could not connect to database:",  eroare
    
    
    def __del__(self):
        self.cursor.close()
        self.conn.close()
    
    
    def checkTables(self):
        # table flights: id, callsign, flt_rules, dep_day, dep_airport, arr_airport, dep_time, arr_time, ac_type, flt_level
        # table fleet: id, airline, ac_type, nr_ac, hubs, callsign, designation
        # table aircraft: id, ac_type, designation, offset, radius, fl_type, perf_class, heavy, model
        pass 
    
    
    def commitTransaction(self):
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
        query='SELECT * FROM flights WHERE'
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
            else:
                query=query+' '+cond+'=? AND '
                query_params.append(value)
        query=query+' 1=1 ORDER BY id ASC'
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
        #self.conn.commit() #manually commit to speed things up
    
    
    def emptyFlights(self):
        self.cursor.execute('DELETE FROM flights')
        self.conn.commit()


    ## fleets ##

    def addFleet(self, fleet_item):
        self.cursor.execute('INSERT OR ROLLBACK INTO fleet (airline, ac_type, nr_ac, hubs, callsign, designation) VALUES (?,?,?,?,?,?)', fleet_item)
        #self.conn.commit() # call commit on the whole chunk to speed things up
    
    
    def getAllFleets(self):
        self.cursor.execute('SELECT * FROM fleet ORDER BY id ASC')
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
        #self.conn.commit() #manually commit to speed things up
    
    
    def emptyFleet(self):
        self.cursor.execute('DELETE FROM fleet')
        self.conn.commit()
    
    
    ## aircraft ##
    
    def addAircraft(self, aircraft):
        self.cursor.execute('INSERT OR ROLLBACK INTO aircraft (ac_type, designation, offset, radius, fl_type, perf_class, heavy, model) VALUES (?,?,?,?,?,?,?,?)', aircraft)
        #self.conn.commit() # call commit on the whole chunk to speed things up
    
    
    def getAllAircraft(self):
        self.cursor.execute('SELECT * FROM aircraft ORDER BY id ASC')
        rows=self.cursor.fetchall()
        return rows
        
    
    def getNrAircraft(self):
        self.cursor.execute('SELECT COUNT(*) FROM aircraft ORDER BY id ASC')
        nr=self.cursor.fetchone()
        return nr[0]


    def getAircraftInfo(self, index):
        self.cursor.execute('SELECT * FROM aircraft WHERE id=?', (index, ))
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
        #self.conn.commit() #manually commit to speed things up
    
    
    def emptyAircraft(self):
        self.cursor.execute('DELETE FROM aircraft')
        self.conn.commit()

