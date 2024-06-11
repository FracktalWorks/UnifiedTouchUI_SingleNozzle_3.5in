import dialog
import requests
from MainUIClass.config import apiKey, _fromUtf8, ip
from PyQt5 import QtGui
from MainUIClass.config import octopiclient

class filamentSensor:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.toggleFilamentSensorButton.clicked.connect(self.toggleFilamentSensor)
        self.MainUIObj.QtSocket.filament_sensor_triggered_signal.connect(self.filamentSensorHandler)

    def isFilamentSensorInstalled(self):
        success = False
        try:
            headers = {'X-Api-Key': apiKey}
            req = requests.get(f'http://{ip}/plugin/Julia2018FilamentSensor/status', headers=headers)
            success = req.status_code == requests.codes.ok
        except:
            pass
        self.MainUIObj.toggleFilamentSensorButton.setEnabled(success)
        return success

    def toggleFilamentSensor(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/Julia2018FilamentSensor/toggle', headers=headers)

    def filamentSensorHandler(self, data):
        sensor_enabled = False

        if 'sensor_enabled' in data:
            sensor_enabled = data["sensor_enabled"] == 1

        icon = 'filamentSensorOn' if sensor_enabled else 'filamentSensorOff'
        self.MainUIObj.toggleFilamentSensorButton.setIcon(QtGui.QIcon(_fromUtf8("templates/img/" + icon)))

        if not sensor_enabled:
            return

        triggered_extruder0 = False
        triggered_door = False
        pause_print = False

        if 'filament' in data:
            triggered_extruder0 = data["filament"] == 0
        elif 'extruder0' in data:
            triggered_extruder0 = data["extruder0"] == 0

        if 'door' in data:
            triggered_door = data["door"] == 0
        if 'pause_print' in data:
            pause_print = data["pause_print"]

        if triggered_extruder0 and self.MainUIObj.stackedWidget.currentWidget() not in [
            self.MainUIObj.changeFilamentPage, self.MainUIObj.changeFilamentProgressPage,
            self.MainUIObj.changeFilamentExtrudePage, self.MainUIObj.changeFilamentRetractPage]:
            if dialog.WarningOk(self.MainUIObj, "Filament outage in Extruder 0"):
                pass

        if triggered_door:
            if self.MainUIObj.printerStatusText == "Printing":
                no_pause_pages = [self.MainUIObj.controlPage, self.MainUIObj.changeFilamentPage, 
                                  self.MainUIObj.changeFilamentProgressPage, self.MainUIObj.changeFilamentExtrudePage, 
                                  self.MainUIObj.changeFilamentRetractPage]
                if not pause_print or self.MainUIObj.stackedWidget.currentWidget() in no_pause_pages:
                    if dialog.WarningOk(self.MainUIObj, "Door opened"):
                        return
                octopiclient.pausePrint()
                if dialog.WarningOk(self.MainUIObj, "Door opened. Print paused.", overlay=True):
                    return
            else:
                if dialog.WarningOk(self.MainUIObj, "Door opened"):
                    return
