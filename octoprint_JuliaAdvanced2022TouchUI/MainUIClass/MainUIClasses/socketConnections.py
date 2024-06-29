from MainUIClass.socket_qt import QtWebsocket
from MainUIClass.MainUIClasses.dialog_methods import tellAndReboot, askAndReboot
import mainGUI
import dialog
from PyQt5 import QtGui, QtCore
from MainUIClass.config import _fromUtf8, ip, apiKey
import styles
import requests
from logger import *
from MainUIClass.MainUIClasses.controlScreen import controlScreen

printerStatusText = None

class socketConnections(QtWebsocket, mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting socket connections init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        self.octopiclient = octopiclient
        # Calibrate page
        self.z_probing_failed_signal.connect(self.showProbingFailed)
        self.z_probe_offset_signal.connect(self.updateEEPROMProbeOffset)
        self.z_home_offset_signal.connect(self.getZHomeOffset)

        # Firmware Update
        self.firmware_updater_signal.connect(self.firmwareUpdateHandler)

        # Filament Sensor
        self.filament_sensor_triggered_signal.connect(self.filamentSensorHandler)

        # Printer Status
        self.temperatures_signal.connect(self.updateTemperature)
        self.status_signal.connect(self.updateStatus)
        self.print_status_signal.connect(self.updatePrintStatus)

        # Software Update Page
        self.update_started_signal.connect(self.softwareUpdateProgress)
        self.update_log_signal.connect(self.softwareUpdateProgressLog)
        self.update_log_result_signal.connect(self.softwareUpdateResult)
        self.update_failed_signal.connect(self.updateFailed)
        


    def updateEEPROMProbeOffset(self, offset):
        '''
        Sets the spinbox value to have the value of the Z offset from the printer.
        the value is -ve so as to be more intuitive.
        :param offset:
        :return:
        '''
        self.nozzleOffsetDoubleSpinBox.setValue(float(offset))

    def showProbingFailed(self):
        tellAndReboot(self, "Bed position is not calibrated. Please run calibration wizard after restart.")

    def getZHomeOffset(self, offset):
        '''
        Sets the spinbox value to have the value of the Z offset from the printer.
        the value is -ve so as to be more intuitive.
        :param offset:
        :return:
        '''
        self.nozzleOffsetDoubleSpinBox.setValue(-float(offset))
        self.nozzleHomeOffset = offset


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
                    dialog.WarningOk(self, "Firmware Updater Error: " + str(data["message"]), overlay=True)
            elif subtype == "success":
                if dialog.SuccessYesNo(self, "Firmware update found.\nPress yes to update now!", overlay=True):
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
                    dialog.WarningOk(self, "Firmware Updater Error: " + str(data["message"]), overlay=True)
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

    def firmwareUpdateStart(self):
        headers = {'X-Api-Key': apiKey}
        requests.get(f'http://{ip}/plugin/JuliaFirmwareUpdater/update/start', headers=headers)

    def firmwareUpdateStartProgress(self):
        self.stackedWidget.setCurrentWidget(self.firmwareUpdateProgressPage)
        self.firmwareUpdateLog.setText("<span style='color: cyan'>Julia Firmware Updater<span>")
        self.firmwareUpdateLog.append("<span style='color: cyan'>---------------------------------------------------------------</span>")
        self.firmwareUpdateBackButton.setEnabled(False)

    def firmwareUpdateProgress(self, text, backEnabled=False):
        self.stackedWidget.setCurrentWidget(self.firmwareUpdateProgressPage)
        self.firmwareUpdateLog.append(str(text))
        self.firmwareUpdateBackButton.setEnabled(backEnabled)

    def filamentSensorHandler(self, data):
        sensor_enabled = False

        if 'sensor_enabled' in data:
            sensor_enabled = data["sensor_enabled"] == 1

        icon = 'filamentSensorOn' if sensor_enabled else 'filamentSensorOff'
        self.toggleFilamentSensorButton.setIcon(QtGui.QIcon(_fromUtf8("templates/img/" + icon)))

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

        if triggered_extruder0 and self.stackedWidget.currentWidget() not in [
            self.changeFilamentPage, self.changeFilamentProgressPage,
            self.changeFilamentExtrudePage, self.changeFilamentRetractPage]:
            if dialog.WarningOk(self, "Filament outage in Extruder 0"):
                pass

        if triggered_door:
            if self.printerStatusText == "Printing":
                no_pause_pages = [self.controlPage, self.changeFilamentPage, 
                                  self.changeFilamentProgressPage, self.changeFilamentExtrudePage, 
                                  self.changeFilamentRetractPage]
                if not pause_print or self.stackedWidget.currentWidget() in no_pause_pages:
                    if dialog.WarningOk(self, "Door opened"):
                        return
                self.octopiclient.pausePrint()
                if dialog.WarningOk(self, "Door opened. Print paused.", overlay=True):
                    return
            else:
                if dialog.WarningOk(self, "Door opened"):
                    return


    def updateTemperature(self, temperature):
        '''
        Slot that gets a signal originating from the thread that keeps polling for printer status
        runs at 1HZ, so do things that need to be constantly updated only. This also controls the cooling fan depending on the temperatures
        :param temperature: dict containing key:value pairs with keys being the tools, bed and their values being their corresponding temperatures
        '''
        if temperature['tool0Target'] is None:
            temperature['tool0Target'] = 0
        if temperature['bedTarget'] is None:
            temperature['bedTarget'] = 0
        if temperature['bedActual'] is None:
            temperature['bedActual'] = 0

        if temperature['tool0Target'] == 0:
            self.tool0TempBar.setMaximum(300)
            self.tool0TempBar.setStyleSheet(styles.bar_heater_cold)
        elif temperature['tool0Actual'] <= temperature['tool0Target']:
            self.tool0TempBar.setMaximum(int(temperature['tool0Target']))
            self.tool0TempBar.setStyleSheet(styles.bar_heater_heating)
        else:
            self.tool0TempBar.setMaximum(int(temperature['tool0Actual']))
        self.tool0TempBar.setValue(int(temperature['tool0Actual']))
        self.tool0ActualTemperature.setText(str(int(temperature['tool0Actual'])))
        self.tool0TargetTemperature.setText(str(int(temperature['tool0Target'])))

        if temperature['bedTarget'] == 0:
            self.bedTempBar.setMaximum(150)
            self.bedTempBar.setStyleSheet(styles.bar_heater_cold)
        elif temperature['bedActual'] <= temperature['bedTarget']:
            self.bedTempBar.setMaximum(int(temperature['bedTarget']))
            self.bedTempBar.setStyleSheet(styles.bar_heater_heating)
        else:
            self.bedTempBar.setMaximum(int(temperature['bedActual']))
        self.bedTempBar.setValue(int(temperature['bedActual']))
        self.bedActualTemperatute.setText(str(int(temperature['bedActual'])))
        self.bedTargetTemperature.setText(str(int(temperature['bedTarget'])))

        # updates the progress bar on the change filament screen
        if self.changeFilamentHeatingFlag:
            if temperature['tool0Target'] == 0:
                self.changeFilamentProgress.setMaximum(300)
            elif temperature['tool0Target'] - temperature['tool0Actual'] > 1:
                self.changeFilamentProgress.setMaximum(int(temperature['tool0Target']))
            else:
                self.changeFilamentProgress.setMaximum(int(temperature['tool0Actual']))
                self.changeFilamentHeatingFlag = False
                if self.loadFlag:
                    self.stackedWidget.setCurrentWidget(self.changeFilamentExtrudePage)
                else:
                    self.stackedWidget.setCurrentWidget(self.changeFilamentRetractPage)
                    self.octopiclient.extrude(10)  # extrudes some amount of filament to prevent plugging

            self.changeFilamentProgress.setValue(int(temperature['tool0Actual']))

    def updatePrintStatus(self, file):
        '''
        Displays information of a particular file on the home page, is a slot for the signal emitted from the thread that keeps polling for printer status
        runs at 1HZ, so do things that need to be constantly updated only
        :param file: dict of all the attributes of a particular file
        '''
        if file is None:
            self.currentFile = None
            self.currentImage = None
            self.timeLeft.setText("-")
            self.fileName.setText("-")
            self.printProgressBar.setValue(0)
            self.printTime.setText("-")
            self.playPauseButton.setDisabled(True)  # if file available, make play button visible
        else:
            self.playPauseButton.setDisabled(False)  # if file available, make play button visible
            self.fileName.setText(file['job']['file']['name'])
            self.currentFile = file['job']['file']['name']
            if file['progress']['printTime'] is None:
                self.printTime.setText("-")
            else:
                m, s = divmod(file['progress']['printTime'], 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                self.printTime.setText("%d:%d:%02d:%02d" % (d, h, m, s))

            if file['progress']['printTimeLeft'] is None:
                self.timeLeft.setText("-")
            else:
                m, s = divmod(file['progress']['printTimeLeft'], 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                self.timeLeft.setText("%d:%d:%02d:%02d" % (d, h, m, s))

            if file['progress']['completion'] is None:
                self.printProgressBar.setValue(0)
            else:
                self.printProgressBar.setValue(file['progress']['completion'])

            '''
            If image is available from server, set it, otherwise display default image.
            If the image was already loaded, don't load it again.
            '''
            if self.currentImage != self.currentFile:
                self.currentImage = self.currentFile
                img = self.octopiclient.getImage(file['job']['file']['name'].replace(".gcode", ".png"))
                if img:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(img)
                    self.printPreviewMain.setPixmap(pixmap)
                else:
                    self.printPreviewMain.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))

    def updateStatus(self, status):
        '''
        Updates the status bar, is a slot for the signal emitted from the thread that constantly polls for printer status
        this function updates the status bar, as well as enables/disables relevant buttons
        :param status: String of the status text
        '''
        global printerStatusText
        printerStatusText = status
        self.printerStatus.setText(status)

        if status == "Printing":  # Green
            self.printerStatusColour.setStyleSheet(styles.printer_status_green)
        elif status == "Offline":  # Red
            self.printerStatusColour.setStyleSheet(styles.printer_status_red)
        elif status == "Paused":  # Amber
            self.printerStatusColour.setStyleSheet(styles.printer_status_amber)
        elif status == "Operational":  # Amber
            self.printerStatusColour.setStyleSheet(styles.printer_status_blue)

        '''
        Depending on Status, enable and Disable Buttons
        '''
        if status == "Printing":
            self.playPauseButton.setChecked(True)
            self.stopButton.setDisabled(False)
            self.motionTab.setDisabled(True)
            self.changeFilamentButton.setDisabled(True)
            self.menuCalibrateButton.setDisabled(True)
            self.menuPrintButton.setDisabled(True)
            # if not Development:
            #     if not self.__timelapse_enabled:
            #         self.octopiclient.cancelPrint()
            #         self.coolDownAction()
        elif status == "Paused":
            self.playPauseButton.setChecked(False)
            self.stopButton.setDisabled(False)
            self.motionTab.setDisabled(False)
            self.changeFilamentButton.setDisabled(False)
            self.menuCalibrateButton.setDisabled(True)
            self.menuPrintButton.setDisabled(True)
        else:
            self.stopButton.setDisabled(True)
            self.playPauseButton.setChecked(False)
            self.motionTab.setDisabled(False)
            self.changeFilamentButton.setDisabled(False)
            self.menuCalibrateButton.setDisabled(False)
            self.menuPrintButton.setDisabled(False)



    def softwareUpdateResult(self, data):
        messageText = ""
        for item in data:
            messageText += item + ": " + data[item][0] + ".\n"
        messageText += "Restart required"
        askAndReboot(self, messageText)

    def softwareUpdateProgress(self, data):
        self.stackedWidget.setCurrentWidget(self.softwareUpdateProgressPage)
        self.logTextEdit.setTextColor(QtCore.Qt.red)
        self.logTextEdit.append("---------------------------------------------------------------\n"
                                     "Updating " + data["name"] + " to " + data["version"] + "\n"
                                     "---------------------------------------------------------------")

    def softwareUpdateProgressLog(self, data):
        self.logTextEdit.setTextColor(QtCore.Qt.white)
        for line in data:
            self.logTextEdit.append(line["line"])

    def updateFailed(self, data):
        self.stackedWidget.setCurrentWidget(self.settingsPage)
        messageText = (data["name"] + " failed to update\n")
        if dialog.WarningOkCancel(self, messageText, overlay=True):
            pass
