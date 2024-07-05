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

    def setup(self, octopiclient):
        log_info("Setting up firmware update.")
        try:
            self.firmwareUpdateBackButton.pressed.connect(self.firmwareUpdateBack)
            log_info("Firmware update setup complete.")
        except Exception as e:
            error_message = f"Error setting up firmware update: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def firmwareUpdateCheck(self):
        log_info("Checking for firmware update.")
        try:
            headers = {'X-Api-Key': apiKey}
            requests.get(f'http://{ip}/plugin/JuliaFirmwareUpdater/update/check', headers=headers)
            log_info("Firmware update check successful.")
        except Exception as e:
            error_message = f"Error checking firmware update: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def firmwareUpdateBack(self):
        log_info("Backing out of firmware update.")
        try:
            self.isFirmwareUpdateInProgress = False
            self.firmwareUpdateBackButton.setEnabled(False)
            self.stackedWidget.setCurrentWidget(self.homePage)
            log_info("Firmware update back action successful.")
        except Exception as e:
            error_message = f"Error performing firmware update back action: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
