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
        pass 
    
 
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
                query=query+' '+'ac_type'+' LIKE \'%-'+value+'%\' AND '
            elif cond=='dep_day':
                query=query+' '+'dep_day'+' LIKE \'%'+value+'%\' AND '
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
    
    
    def commitTransaction(self):
        self.conn.commit()
    
    def editFlight(self, flight):
        self.cursor.execute('UPDATE OR ROLLBACK flights SET callsign=?, flt_rules=?, dep_day=?, dep_airport=?, arr_airport=?, dep_time=?, arr_time=?, ac_type=?, flt_level=? WHERE id=?', flight)
        self.conn.commit()
    
    
    def deleteFlight(self, flight):
        self.cursor.execute('DELETE FROM flights WHERE id=?', (flight, ))
        self.conn.commit()
    
    
    def emptyFlights(self):
        self.cursor.execute('DELETE FROM flights')
        self.conn.commit()

