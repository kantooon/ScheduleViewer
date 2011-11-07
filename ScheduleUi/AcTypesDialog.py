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


from PyQt4 import QtCore, QtGui
from QTableWidgetNumericItem import QTableWidgetNumericItem
import Ui_AcTypesDialog
import os

class AcTypesDialog(QtGui.QDialog):

    def __init__(self, ac):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_AcTypesDialog.Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.hubsTableWidget.setSortingEnabled(False)
        if ac==None:
            self.close()
        nr_hubs=len(ac)
        if nr_hubs==0:
            self.close()
        table=self.ui.hubsTableWidget
        table.setRowCount(0)
        table.setRowCount(nr_hubs)
        r=0
        for a in ac:
            nr=QTableWidgetNumericItem(str(a[0]), 0)
            nr.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            #nr.setFlags(QtCore.Qt.NoItemFlags)
            
            aircraft=QtGui.QTableWidgetItem(str(a[1][:3]), 0)
            aircraft.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
            
            table.setItem(r, 1, nr)
            table.setItem(r, 0, aircraft)
            QtCore.QCoreApplication.processEvents(QtCore.QEventLoop.AllEvents)
            r=r+1
        self.ui.hubsTableWidget.setSortingEnabled(True)
        self.ui.hubsTableWidget.sortItems(1, QtCore.Qt.DescendingOrder)
        
        self.show()
