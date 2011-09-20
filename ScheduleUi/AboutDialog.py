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
import Ui_AboutDialog
import os

class AboutDialog(QtGui.QDialog):

    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.ui = Ui_AboutDialog.Ui_Dialog()
        self.ui.setupUi(self)
        try:
            license_file=open(os.path.join(os.getcwd(),'COPYING'), 'rb')
            license_text= license_file.read()
        except Exception as ex:
            license_text=''
        try:
            thanks_file=open(os.path.join(os.getcwd(),'THANKS'), 'rb')
            thanks_text= thanks_file.read()
        except Exception as ex2:
            thanks_text=''
        self.ui.aboutTextEdit.setHtml("<b>ScheduleViewer</b> is a lightweight viewer and manager of \
        Flightgear AI flight schedules.<br/><br/> It uses a sqlite database backend and allows one to \
        query the schedule database according to the filter criteria, import schedules in conf format, \
        filter, edit, delete and export them back to conf format.<br/><br/> \
        For the latest version download \
        <a href=\"https://gitorious.org/fg-ai-flightplan/fgscheduleviewer/archive-tarball/master/\">\
        https://gitorious.org/fg-ai-flightplan/fgscheduleviewer/archive-tarball/master</a>")
        self.ui.licenseTextEdit.setHtml("<b>ScheduleViewer</b> is Copyright (c) 2011 Adrian Musceac \
        <a href=\"mailto:kantooon@users.sf.net\">kantooon@users.sf.net</a><br/><br/> \
        ScheduleViewer is distributed \"as is\", in the hope that it will be useful \
        <br/>\
        You may use, distribute and copy ScheduleViewer under the terms of the GNU \
        General Public License as published by the Free Software Foundation, \
        either version 2 of the License, which is shown below, or (at your \
        option) any later version.<br/><hr/><br/>\
        " +license_text)
        self.ui.thanksTextEdit.setHtml(thanks_text)
        self.show()
