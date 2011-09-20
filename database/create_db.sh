#!/bin/sh

/usr/bin/sqlite3 flights.db 'CREATE TABLE flights (id INTEGER PRIMARY KEY, callsign TEXT, flt_rules TEXT, dep_day TEXT, dep_airport TEXT, arr_airport TEXT, dep_time TEXT, arr_time TEXT, ac_type TEXT, flt_level INT);'
