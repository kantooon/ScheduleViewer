#!/bin/sh

/usr/bin/sqlite3 flights.db 'CREATE TABLE flights (id INTEGER PRIMARY KEY, callsign TEXT, flt_rules TEXT, dep_day TEXT, dep_airport TEXT, arr_airport TEXT, dep_time TEXT, arr_time TEXT, ac_type TEXT, flt_level INT);CREATE TABLE aircraft ( id INTEGER PRIMARY KEY, ac_type TEXT, designation TEXT, offset TEXT, radius TEXT, fl_type TEXT, perf_class TEXT, heavy TEXT, model TEXT);CREATE TABLE fleet ( id INTEGER PRIMARY KEY, airline TEXT, ac_type TEXT, nr_ac TEXT, hubs TEXT, callsign TEXT, designation TEXT);'
