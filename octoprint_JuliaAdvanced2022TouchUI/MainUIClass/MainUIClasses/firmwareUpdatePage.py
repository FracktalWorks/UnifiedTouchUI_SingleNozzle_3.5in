import dialog
from MainUIClass.config import ip, apiKey
import requests
import mainGUI

class firmwareUpdatePage(mainGUI.Ui_MainWindow):
    isFirmwareUpdateInProgress = False

    def __init__(self, MainUIObj):
        self.firmwareUpdateBackButton.pressed.connect(self.firmwareUpdateBack)
        super().__init__()

    def firmwareUpdateCheck(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/JuliaFirmwareUpdater/update/check', headers=headers)

    def firmwareUpdateBack(self):
        self.isFirmwareUpdateInProgress = False
        self.firmwareUpdateBackButton.setEnabled(False)
        self.stackedWidget.setCurrentWidget(self.homePage)
