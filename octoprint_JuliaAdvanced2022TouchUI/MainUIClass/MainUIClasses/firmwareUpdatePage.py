import dialog
from MainUIClass.config import ip, apiKey
import requests
import mainGUI
from logger import *

class firmwareUpdatePage(mainGUI.Ui_MainWindow):
    isFirmwareUpdateInProgress = False

    def __init__(self):
        log_info("Starting firmware update init.")
        super().__init__()

    def setup(self):
        self.firmwareUpdateBackButton.pressed.connect(self.firmwareUpdateBack)
        

    def firmwareUpdateCheck(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/JuliaFirmwareUpdater/update/check', headers=headers)

    def firmwareUpdateBack(self):
        self.isFirmwareUpdateInProgress = False
        self.firmwareUpdateBackButton.setEnabled(False)
        self.stackedWidget.setCurrentWidget(self.homePage)
