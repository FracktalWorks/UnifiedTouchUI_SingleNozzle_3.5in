import requests
from MainUIClass.config import apiKey, ip
from PyQt5 import QtGui
import mainGUI

class filamentSensor(mainGUI.Ui_MainWindow):
    def __init__(self):
        self.toggleFilamentSensorButton.clicked.connect(self.toggleFilamentSensor)
        super().__init__()

    def isFilamentSensorInstalled(self):
        success = False
        try:
            headers = {'X-Api-Key': apiKey}
            req = requests.get(f'http://{ip}/plugin/Julia2018FilamentSensor/status', headers=headers)
            success = req.status_code == requests.codes.ok
        except:
            pass
        self.toggleFilamentSensorButton.setEnabled(success)
        return success

    def toggleFilamentSensor(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/Julia2018FilamentSensor/toggle', headers=headers)

