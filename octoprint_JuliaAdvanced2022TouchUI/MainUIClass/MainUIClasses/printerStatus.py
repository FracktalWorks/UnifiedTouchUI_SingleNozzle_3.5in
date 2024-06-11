import styles
from PyQt5 import QtGui
from MainUIClass.config import octopiclient
from MainUIClass.config import _fromUtf8

class printerStatus:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.QtSocket.temperatures_signal.connect(self.updateTemperature)
        self.MainUIObj.QtSocket.status_signal.connect(self.updateStatus)
        self.MainUIObj.QtSocket.print_status_signal.connect(self.updatePrintStatus)

    ''' +++++++++++++++++++++++++++++++++Printer Status+++++++++++++++++++++++++++++++++++ '''
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
            self.MainUIObj.tool0TempBar.setMaximum(300)
            self.MainUIObj.tool0TempBar.setStyleSheet(styles.bar_heater_cold)
        elif temperature['tool0Actual'] <= temperature['tool0Target']:
            self.MainUIObj.tool0TempBar.setMaximum(int(temperature['tool0Target']))
            self.MainUIObj.tool0TempBar.setStyleSheet(styles.bar_heater_heating)
        else:
            self.MainUIObj.tool0TempBar.setMaximum(int(temperature['tool0Actual']))
        self.MainUIObj.tool0TempBar.setValue(int(temperature['tool0Actual']))
        self.MainUIObj.tool0ActualTemperature.setText(str(int(temperature['tool0Actual'])))
        self.MainUIObj.tool0TargetTemperature.setText(str(int(temperature['tool0Target'])))

        if temperature['bedTarget'] == 0:
            self.MainUIObj.bedTempBar.setMaximum(150)
            self.MainUIObj.bedTempBar.setStyleSheet(styles.bar_heater_cold)
        elif temperature['bedActual'] <= temperature['bedTarget']:
            self.MainUIObj.bedTempBar.setMaximum(int(temperature['bedTarget']))
            self.MainUIObj.bedTempBar.setStyleSheet(styles.bar_heater_heating)
        else:
            self.MainUIObj.bedTempBar.setMaximum(int(temperature['bedActual']))
        self.MainUIObj.bedTempBar.setValue(int(temperature['bedActual']))
        self.MainUIObj.bedActualTemperatute.setText(str(int(temperature['bedActual'])))
        self.MainUIObj.bedTargetTemperature.setText(str(int(temperature['bedTarget'])))

        # updates the progress bar on the change filament screen
        if self.MainUIObj.changeFilamentHeatingFlag:
            if temperature['tool0Target'] == 0:
                self.MainUIObj.changeFilamentProgress.setMaximum(300)
            elif temperature['tool0Target'] - temperature['tool0Actual'] > 1:
                self.MainUIObj.changeFilamentProgress.setMaximum(int(temperature['tool0Target']))
            else:
                self.MainUIObj.changeFilamentProgress.setMaximum(int(temperature['tool0Actual']))
                self.MainUIObj.changeFilamentHeatingFlag = False
                if self.MainUIObj.loadFlag:
                    self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.changeFilamentExtrudePage)
                else:
                    self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.changeFilamentRetractPage)
                    octopiclient.extrude(10)  # extrudes some amount of filament to prevent plugging

            self.MainUIObj.changeFilamentProgress.setValue(int(temperature['tool0Actual']))

    def updatePrintStatus(self, file):
        '''
        Displays information of a particular file on the home page, is a slot for the signal emitted from the thread that keeps polling for printer status
        runs at 1HZ, so do things that need to be constantly updated only
        :param file: dict of all the attributes of a particular file
        '''
        if file is None:
            self.MainUIObj.currentFile = None
            self.MainUIObj.currentImage = None
            self.MainUIObj.timeLeft.setText("-")
            self.MainUIObj.fileName.setText("-")
            self.MainUIObj.printProgressBar.setValue(0)
            self.MainUIObj.printTime.setText("-")
            self.MainUIObj.playPauseButton.setDisabled(True)  # if file available, make play button visible
        else:
            self.MainUIObj.playPauseButton.setDisabled(False)  # if file available, make play button visible
            self.MainUIObj.fileName.setText(file['job']['file']['name'])
            self.MainUIObj.currentFile = file['job']['file']['name']
            if file['progress']['printTime'] is None:
                self.MainUIObj.printTime.setText("-")
            else:
                m, s = divmod(file['progress']['printTime'], 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                self.MainUIObj.printTime.setText("%d:%d:%02d:%02d" % (d, h, m, s))

            if file['progress']['printTimeLeft'] is None:
                self.MainUIObj.timeLeft.setText("-")
            else:
                m, s = divmod(file['progress']['printTimeLeft'], 60)
                h, m = divmod(m, 60)
                d, h = divmod(h, 24)
                self.MainUIObj.timeLeft.setText("%d:%d:%02d:%02d" % (d, h, m, s))

            if file['progress']['completion'] is None:
                self.MainUIObj.printProgressBar.setValue(0)
            else:
                self.MainUIObj.printProgressBar.setValue(file['progress']['completion'])

            '''
            If image is available from server, set it, otherwise display default image.
            If the image was already loaded, don't load it again.
            '''
            if self.MainUIObj.currentImage != self.MainUIObj.currentFile:
                self.MainUIObj.currentImage = self.MainUIObj.currentFile
                img = octopiclient.getImage(file['job']['file']['name'].replace(".gcode", ".png"))
                if img:
                    pixmap = QtGui.QPixmap()
                    pixmap.loadFromData(img)
                    self.MainUIObj.printPreviewMain.setPixmap(pixmap)
                else:
                    self.MainUIObj.printPreviewMain.setPixmap(QtGui.QPixmap(_fromUtf8("templates/img/thumbnail.png")))

    def updateStatus(self, status):
        '''
        Updates the status bar, is a slot for the signal emitted from the thread that constantly polls for printer status
        this function updates the status bar, as well as enables/disables relevant buttons
        :param status: String of the status text
        '''
        self.MainUIObj.printerStatusText = status
        self.MainUIObj.printerStatus.setText(status)

        if status == "Printing":  # Green
            self.MainUIObj.printerStatusColour.setStyleSheet(styles.printer_status_green)
        elif status == "Offline":  # Red
            self.MainUIObj.printerStatusColour.setStyleSheet(styles.printer_status_red)
        elif status == "Paused":  # Amber
            self.MainUIObj.printerStatusColour.setStyleSheet(styles.printer_status_amber)
        elif status == "Operational":  # Amber
            self.MainUIObj.printerStatusColour.setStyleSheet(styles.printer_status_blue)

        '''
        Depending on Status, enable and Disable Buttons
        '''
        if status == "Printing":
            self.MainUIObj.playPauseButton.setChecked(True)
            self.MainUIObj.stopButton.setDisabled(False)
            self.MainUIObj.motionTab.setDisabled(True)
            self.MainUIObj.changeFilamentButton.setDisabled(True)
            self.MainUIObj.menuCalibrateButton.setDisabled(True)
            self.MainUIObj.menuPrintButton.setDisabled(True)
            # if not Development:
            #     if not self.__timelapse_enabled:
            #         octopiclient.cancelPrint()
            #         self.coolDownAction()
        elif status == "Paused":
            self.MainUIObj.playPauseButton.setChecked(False)
            self.MainUIObj.stopButton.setDisabled(False)
            self.MainUIObj.motionTab.setDisabled(False)
            self.MainUIObj.changeFilamentButton.setDisabled(False)
            self.MainUIObj.menuCalibrateButton.setDisabled(True)
            self.MainUIObj.menuPrintButton.setDisabled(True)
        else:
            self.MainUIObj.stopButton.setDisabled(True)
            self.MainUIObj.playPauseButton.setChecked(False)
            self.MainUIObj.motionTab.setDisabled(False)
            self.MainUIObj.changeFilamentButton.setDisabled(False)
            self.MainUIObj.menuCalibrateButton.setDisabled(False)
            self.MainUIObj.menuPrintButton.setDisabled(False)
