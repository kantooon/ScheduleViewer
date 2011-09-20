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


import sys
from ScheduleUi import MainWindow
from Logic.logger import *
from PyQt4 import QtGui
from PyQt4 import QtCore


## log redirecting will happen
sys.stdout = LogStream('debug')
sys.stderr = LogStream('error')


app = QtGui.QApplication(sys.argv)
app.setApplicationName("ScheduleViewer")
app.setApplicationVersion("0.1")
window = MainWindow.MainWindow()
window.show()
sys.exit(app.exec_())
