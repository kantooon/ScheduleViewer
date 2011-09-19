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


import sys, os, io, time

class LogStream(object):
    def __init__(self, type): 
        if type=='debug':
            self.logfile = open(os.path.join(os.getcwd(), 'logs', 'debug_'+time.strftime("%Y-%m-%d")+'.log'), 'ab')
        elif type=='error':
            self.logfile = open(os.path.join(os.getcwd(), 'logs', 'error_'+time.strftime("%Y-%m-%d")+'.log'), 'ab')
    def write(self,data): 
        self.logfile.write(data)
    def read(self,data): pass
    def flush(self): 
        self.logfile.flush()
    def close(self): 
        self.logfile.close()

