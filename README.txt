About:
======
ScheduleViewer is a program that can:
1. Import Flightgear AI schedules in .conf format into a common database
2. Filter and show flightplans according to user criteria
3. Delete flightplans
4. Edit flightplans
5. Export flightplans

At the moment only points 1 and 2 are functional


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
    sh ScheduleViewer.sh
 Or install the shortcut in your desktop environment by running the script.
    
Windows:
 Extract the folder to a convenient location on your drive.
 Make sure you meet the requirements listed above.
 Run "C:\Python27\python.exe viewer.py" from the application directory.
 
 
Basic usage:
============
Only Linux usage is supported at the moment.
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
If you order the table by a column other than id and then apply filters,
the table will be corrupted. To solve this, simply order by id again, then order by
the column you want.


License information:
====================
ScheduleViewer is Copyright (c) 2011 Adrian Musceac <kantooon@users.sf.net>
You may use, distribute and copy ScheduleViewer under the terms of the GNU
General Public License as published by the Free Software Foundation, 
either version 2 of the License, which is attached to this archive, or
(at your option) any later version.
