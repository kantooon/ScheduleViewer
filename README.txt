About:
======
ScheduleViewer is a program that can:
1. Import Flightgear AI schedules in .conf format into a common database
2. Filter and show flightplans according to user criteria
3. Create duplicate flights index
4. Delete obvious duplicate flights
5. Delete flightplans
6. Edit flightplans
7. Export flightplans
8. Add flightplans
9. Perform the above operations for airline fleets and aircraft
10. Check schedules and insert missing aircraft into the aicraft table
11. Check model-livery availability and display their status in the airline fleets tab
12. Export aircraft conf files.
13. Export complete XML flightplans
14. View airport statistics / airline hubs
15. Preview aircraft model with livery in FGViewer
16. Show the complete aircraft fleet of an airline


Requirements:
=============
Linux: 
 ScheduleViewer needs both Python >= 2.6 and PyQt >= 4.6 to run.
 Python 3.* is not supported.
 It may run on older versions of Python and PyQt with unpredictable
 results.
 To recreate the database and administer the tables, it is recommended to
 have the command line sqlite3 client.
 On Debian based distributions:
    apt-get install python python-qt4 sqlite3 libsqlite3-0 python-pysqlite2 
 This will install dependencies needed to run ScheduleViewer.

Windows XP: 
 The program requires the Python interpreter and the PyQt bindings to run. See:
 http://www.riverbankcomputing.co.uk/software/pyqt/download
 http://www.python.org/download/releases/2.7.2/
 Python 3.* is not supported.


Quick Installation:
===================
Linux: 
 Make sure you have installed all dependencies as described 
 above. Extract the archive to a convenient location.
 Open a terminal and type:
    sh run.sh
 Or install the shortcut in your desktop environment by running the script.
    
Windows:
 Extract the folder to a convenient location on your drive.
 Make sure you meet the requirements listed above.
 Run "C:\Python27\python.exe viewer.py" from the application directory.
 
 
Basic usage:
============
Only Linux usage is supported at the moment.
You must first edit the file "settings" to point fgdata_path to your FGFS data 
install path. This is required for livery checking and aircraft conf exporting.
The program comes with the most current flight schedule database so there is 
no need to re-import from conf files. However, if you wish to do so:
Select File...Import... to import flights from a directory and its subdirectories.
When the import has succeded a message box will apear to let you know.
This operation could take a long time.

To display flights according to your criteria, fill in the fields which you want
the results filtered on, and click Show(). 
See Help -> Help for additional instructions.


Known issues:
=============
The program can't import aircraft confs yet or lines starting with AC from mixed confs.
To display duplicate flight schedules, the application needs to build an index of
duplicate entries in the database. Due to the large number of flights, this operation
can take a very long time (an hour or more, depending on the machine performance).


License information:
====================
ScheduleViewer is Copyright (c) 2011 Adrian Musceac <kantooon@users.sf.net>
You may use, distribute and copy ScheduleViewer under the terms of the GNU
General Public License as published by the Free Software Foundation, 
either version 2 of the License, which is attached to this archive, or
(at your option) any later version.
