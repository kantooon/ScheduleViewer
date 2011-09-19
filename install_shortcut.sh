#!/bin/sh
# announce the app to modern desktop environments
# (by creating ~/.local/share/applications/ScheduleViewer.desktop)
# Hint: this script has to be located in the ScheduleViewer base directory to work
# script from the assaultcube project
# get Exec target path (APP_DIR has to be the full path of the ScheduleViewer base directory)

APP_DIR=$(dirname $(readlink -f "${0}"))
APP_EXEC=ScheduleViewer.sh
SHORTCUTPATH=~/.local/share/applications
SHORTCUTFILE=ScheduleViewer.desktop

if [ -x "${APP_DIR}/${APP_EXEC}" ]; then
  if [ -f ${SHORTCUTPATH}/${SHORTCUTFILE} ]; then
    rm ${SHORTCUTPATH}/${SHORTCUTFILE}
    echo "Shortcut removed."
  else
    mkdir -pv ${SHORTCUTPATH}
    cat > ${SHORTCUTPATH}/${SHORTCUTFILE} <<EOF
[Desktop Entry]
Version=1.1
Type=Application
Encoding=UTF-8
Exec=${APP_DIR}/${APP_EXEC}
Path=${APP_DIR}
Icon=${APP_DIR}/icons/main.png
StartupNotify=true
Categories=Game;
Name=ScheduleViewer
Comment=Flightgear AI schedule manager
EOF
    echo "Shortcut created."
  fi
else
  echo "Could not find the ScheduleViewer base directory, move this script to the ScheduleViewer base"
  echo "directory and start it again."
  exit -1
fi

