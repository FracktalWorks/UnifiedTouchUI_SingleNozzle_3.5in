from PyQt5 import QtWidgets, QtGui, QtCore

from MainUIClass.MainUIClasses.printerName import printerName
from MainUIClass.MainUIClasses.changeFilamentRoutine import changeFilamentRoutine
from MainUIClass.MainUIClasses.controlScreen import controlScreen
from MainUIClass.MainUIClasses.displaySettings import displaySettings
from MainUIClass.MainUIClasses.filamentSensor import filamentSensor
from MainUIClass.MainUIClasses.firmwareUpdatePage import firmwareUpdatePage
from MainUIClass.MainUIClasses.getFilesAndInfo import getFilesAndInfo
from MainUIClass.MainUIClasses.homePage import homePage
from MainUIClass.MainUIClasses.menuPage import menuPage
from MainUIClass.MainUIClasses.printLocationScreen import printLocationScreen
from MainUIClass.MainUIClasses.printRestore import printRestore
from MainUIClass.MainUIClasses.settingsPage import settingsPage
from MainUIClass.MainUIClasses.softwareUpdatePage import softwareUpdatePage
from MainUIClass.MainUIClasses.start_keyboard import startKeyboard
from MainUIClass.MainUIClasses.calibrationPage import calibrationPage
from MainUIClass.MainUIClasses.networking import networking
from MainUIClass.MainUIClasses.threads import ThreadSanityCheck
from MainUIClass.MainUIClasses.lineEdits import lineEdits

import mainGUI

from MainUIClass.config import _fromUtf8, setCalibrationPosition, Development
import logging
import styles
from MainUIClass.socket_qt import QtWebsocket
from MainUIClass.MainUIClasses.threads import octopiclient
from MainUIClass.gui_elements import ClickableLineEdit

from logger import *

# from MainUIClass.import_helper import load_classes      #used to import all classes at runtime

import dialog

class MainUIClass(QtWidgets.QMainWindow, mainGUI.Ui_MainWindow, lineEdits, printerName, changeFilamentRoutine, controlScreen, displaySettings, filamentSensor, firmwareUpdatePage, getFilesAndInfo, homePage, menuPage, printLocationScreen, printRestore, settingsPage, settingsPage, softwareUpdatePage, calibrationPage, networking):
    
    def __init__(self):

        log_info("Starting mainUI init.")

        '''
        This method gets called when an object of type MainUIClass is defined
        '''

        QtWidgets.QMainWindow.__init__(MainUIClass, self)
        super().__init__()
 
        if not Development:
            formatter = logging.Formatter("%(asctime)s %(message)s")
            self._logger = logging.getLogger("TouchUI")
            file_handler = logging.FileHandler("/home/pi/ui.log")
            file_handler.setFormatter(formatter)
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            file_handler.setLevel(logging.DEBUG)
            self._logger.addHandler(file_handler)
            self._logger.addHandler(stream_handler)
        try:
            # if not Development:
                # self.__packager = asset_bundle.AssetBundle()
                # self.__packager.save_time()
                # self.__timelapse_enabled = self.__packager.read_match() if self.__packager.time_delta() else True
                # self.__timelapse_started = not self.__packager.time_delta()

                # self._logger.info("Hardware ID = {}, Unlocked = {}".format(self.__packager.hc(), self.__timelapse_enabled))
                # print("Hardware ID = {}, Unlocked = {}".format(self.__packager.hc(), self.__timelapse_enabled))
                # self._logger.info("File time = {}, Demo = {}".format(self.__packager.read_time(), self.__timelapse_started))
                # print("File time = {}, Demo = {}".format(self.__packager.read_time(), self.__timelapse_started))
            self.setupUi(self)
            self.stackedWidget.setCurrentWidget(self.loadingPage)
            self.setStep(10)
            self.keyboardWindow = None
            self.changeFilamentHeatingFlag = False
            self.setHomeOffsetBool = False
            self.currentImage = None
            self.currentFile = None
            # if not Development:
            #     self.sanityCheck = ThreadSanityCheck(self._logger, virtual=not self.__timelapse_enabled)
            # else:
            self.sanityCheck = ThreadSanityCheck(virtual=False)
            self.sanityCheck.start()
            self.sanityCheck.loaded_signal.connect(self.proceed)
            self.sanityCheck.startup_error_signal.connect(self.handleStartupError)


            for spinbox in self.findChildren(QtWidgets.QSpinBox):
                lineEdit = spinbox.lineEdit()
                lineEdit.setReadOnly(True)
                lineEdit.setDisabled(True)
                p = lineEdit.palette()
                p.setColor(QtGui.QPalette.Highlight, QtGui.QColor(40, 40, 40))
                lineEdit.setPalette(p)


        except Exception as e:
            if not Development:
                self._logger.error(e)

    def setupUi(self, MainWindow):
        log_info("setup UI")
        
        super(MainUIClass, self).setupUi(MainWindow)

        self.menuCartButton.setDisabled(True)

        self.setPrinterNameComboBox()
        setCalibrationPosition(self)

        if self.printerName == "Julia Advanced":
            self.movie = QtGui.QMovie("templates/img/loading.gif")
        elif self.printerName == "Julia Extended":
            self.movie = QtGui.QMovie("templates/img/loading-90.gif")
        elif self.printerName == "Julia Pro Single Nozzle":
            self.movie = QtGui.QMovie("templates/img/loading.gif")
        self.loadingGif.setMovie(self.movie)
        self.movie.start()

    def safeProceed(self):
        
        log_info("safe proceed")
        
        '''
        When Octoprint server cannot connect for whatever reason, still show the home screen to conduct diagnostics
        '''
        self.movie.stop()
        if not Development:
            self.stackedWidget.setCurrentWidget(self.homePage)
            # self.Lock_showLock()
            self.networkingInstance.setIPStatus()
        else:
            self.stackedWidget.setCurrentWidget(self.homePage)

        # # Text Input events
        self.wifiPasswordLineEdit.clicked_signal.connect(lambda: self.startKeyboard(self.wifiPasswordLineEdit.setText))
        self.ethStaticIpLineEdit.clicked_signal.connect(lambda: self.ethShowKeyboard(self.ethStaticIpLineEdit))
        self.ethStaticGatewayLineEdit.clicked_signal.connect(lambda: self.ethShowKeyboard(self.ethStaticGatewayLineEdit))

        # Button Events:

        # Home Screen:
        self.stopButton.setDisabled()
        # self.menuButton.pressed.connect(self.keyboardButton)
        self.menuButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.controlButton.setDisabled()
        self.playPauseButton.setDisabled()

        # MenuScreen
        self.menuBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.menuControlButton.setDisabled()
        self.menuPrintButton.setDisabled()
        self.menuCalibrateButton.setDisabled()
        self.menuSettingsButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))


        # Settings Page
        self.networkSettingsButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))
        self.displaySettingsButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.displaySettingsPage))
        self.settingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.pairPhoneButton.pressed.connect(self.pairPhoneApp)
        self.OTAButton.setDisabled()
        self.versionButton.setDisabled()

        self.restartButton.pressed.connect(self.askAndReboot)
        self.restoreFactoryDefaultsButton.pressed.connect(self.restoreFactoryDefaults)
        self.restorePrintSettingsButton.pressed.connect(self.restorePrintDefaults)

        # Network settings page
        self.networkInfoButton.pressed.connect(self.networkInfo)
        self.configureWifiButton.pressed.connect(self.wifiSettings)
        self.configureEthButton.pressed.connect(self.ethSettings)
        self.networkSettingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

        # Network Info Page
        self.networkInfoBackButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))

        # WifiSetings page
        self.wifiSettingsSSIDKeyboardButton.pressed.connect(
            lambda: self.startKeyboard(self.wifiSettingsComboBox.addItem))
        self.wifiSettingsCancelButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))
        self.wifiSettingsDoneButton.pressed.connect(self.acceptWifiSettings)

        # Ethernet setings page
        self.ethStaticCheckBox.stateChanged.connect(self.ethStaticChanged)
        # self.ethStaticCheckBox.stateChanged.connect(lambda: self.ethStaticSettings.setVisible(self.ethStaticCheckBox.isChecked()))
        self.ethStaticIpKeyboardButton.pressed.connect(lambda: self.ethShowKeyboard(self.ethStaticIpLineEdit))
        self.ethStaticGatewayKeyboardButton.pressed.connect(lambda: self.ethShowKeyboard(self.ethStaticGatewayLineEdit))
        self.ethSettingsDoneButton.pressed.connect(self.ethSaveStaticNetworkInfo)
        self.ethSettingsCancelButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))

        # Display settings
        self.rotateDisplay.pressed.connect(self.showRotateDisplaySettingsPage)
        self.calibrateTouch.pressed.connect(self.touchCalibration)
        self.displaySettingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

        # Rotate Display Settings
        self.rotateDisplaySettingsDoneButton.pressed.connect(self.saveRotateDisplaySettings)
        self.rotateDisplaySettingsCancelButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.displaySettingsPage))

        # QR Code
        self.QRCodeBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

        # SoftwareUpdatePage
        self.softwareUpdateBackButton.setDisabled()
        self.performUpdateButton.setDisabled()

        # Firmware update page
        self.firmwareUpdateBackButton.setDisabled()

        # Filament sensor toggle
        self.toggleFilamentSensorButton.setDisabled()

    def proceed(self):
        
        log_info("proceed")
        
        '''
        Startes websocket, as well as initialises button actions and callbacks. THis is done in such a manner so that the callbacks that dnepend on websockets
        load only after the socket is available which in turn is dependent on the server being available which is checked in the sanity check thread
        '''
        self.QtSocket = QtWebsocket()
        self.QtSocket.start()
        self.setActions()
        self.movie.stop()
        if not Development:
            self.stackedWidget.setCurrentWidget(self.homePage)
            # self.Lock_showLock()
            self.setIPStatus()
        else:
            self.stackedWidget.setCurrentWidget(self.homePage)

        self.isFilamentSensorInstalled()
        self.onServerConnected()

    def setActions(self):
        
        log_info("set actions")
        

        '''
        defines all the Slots and Button events.
        '''
        self.QtSocket.connected_signal.connect(self.onServerConnected)

        #  # Lock settings
        #     if not Development:
        #         self.lockSettingsInstance = lockSettings(self)
        
    def handleStartupError(self):
        
        log_info("handle startup error")
        
        self.safeProceed()
        print('Unable to connect to Octoprint Server')
        if dialog.WarningOk(self, "Unable to connect to internal Server, try restoring factory settings", overlay=True):
            pass

    def onServerConnected(self):
        
        log_info("Starting mainUI init.")
        
        self.isFilamentSensorInstalled()
        # if not self.__timelapse_enabled:
        #     return
        # if self.__timelapse_started:
        #     return
        try:
            response = octopiclient.isFailureDetected()
            if response["canRestore"] is True:
                self.printRestoreMessageBox(response["file"])
            else:
                self.firmwareUpdateCheck()
        except:
            print ("error on Server Connected")
            pass

