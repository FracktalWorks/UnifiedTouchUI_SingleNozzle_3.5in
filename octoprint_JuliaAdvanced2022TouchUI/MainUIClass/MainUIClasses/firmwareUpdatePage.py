import dialog
from MainUIClass.config import ip, apiKey
import requests


class firmwareUpdatePage:
    isFirmwareUpdateInProgress = False

    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.firmwareUpdateBackButton.pressed.connect(self.firmwareUpdateBack)
        self.MainUIObj.QtSocket.firmware_updater_signal.connect(self.firmwareUpdateHandler)

    def firmwareUpdateCheck(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/JuliaFirmwareUpdater/update/check', headers=headers)

    def firmwareUpdateStart(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/JuliaFirmwareUpdater/update/start', headers=headers)

    def firmwareUpdateStartProgress(self):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.firmwareUpdateProgressPage)
        self.MainUIObj.firmwareUpdateLog.setText("<span style='color: cyan'>Julia Firmware Updater<span>")
        self.MainUIObj.firmwareUpdateLog.append("<span style='color: cyan'>---------------------------------------------------------------</span>")
        self.MainUIObj.firmwareUpdateBackButton.setEnabled(False)

    def firmwareUpdateProgress(self, text, backEnabled=False):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.firmwareUpdateProgressPage)
        self.MainUIObj.firmwareUpdateLog.append(str(text))
        self.MainUIObj.firmwareUpdateBackButton.setEnabled(backEnabled)

    def firmwareUpdateBack(self):
        self.isFirmwareUpdateInProgress = False
        self.MainUIObj.firmwareUpdateBackButton.setEnabled(False)
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage)

    def firmwareUpdateHandler(self, data):
        if "type" not in data or data["type"] != "status":
            return

        if "status" not in data:
            return

        status = data["status"]
        subtype = data["subtype"] if "subtype" in data else None

        if status == "update_check":  # update check
            if subtype == "error":  # notify error in ok dialog
                self.isFirmwareUpdateInProgress = False
                if "message" in data:
                    dialog.WarningOk(self.MainUIObj, "Firmware Updater Error: " + str(data["message"]), overlay=True)
            elif subtype == "success":
                if dialog.SuccessYesNo(self.MainUIObj, "Firmware update found.\nPress yes to update now!", overlay=True):
                    self.isFirmwareUpdateInProgress = True
                    self.firmwareUpdateStart()
        elif status == "update_start":  # update started
            if subtype == "success":  # update progress
                self.isFirmwareUpdateInProgress = True
                self.firmwareUpdateStartProgress()
                if "message" in data:
                    message = "<span style='color: yellow'>{}</span>".format(data["message"])
                    self.firmwareUpdateProgress(message)
            else:  # show error
                self.isFirmwareUpdateInProgress = False
                if "message" in data:
                    dialog.WarningOk(self.MainUIObj, "Firmware Updater Error: " + str(data["message"]), overlay=True)
        elif status == "flasherror" or status == "progress":  # show software update dialog and update textview
            if "message" in data:
                message = "<span style='color: {}'>{}</span>".format("teal" if status == "progress" else "red", data["message"])
                self.firmwareUpdateProgress(message, backEnabled=(status == "flasherror"))
        elif status == "success":  # show ok dialog to show done
            self.isFirmwareUpdateInProgress = False
            message = data["message"] if "message" in data else "Flash successful!"
            message = "<span style='color: green'>{}</span>".format(message)
            message = message + "<br/><br/><span style='color: white'>Press back to continue...</span>"
            self.firmwareUpdateProgress(message, backEnabled=True)
