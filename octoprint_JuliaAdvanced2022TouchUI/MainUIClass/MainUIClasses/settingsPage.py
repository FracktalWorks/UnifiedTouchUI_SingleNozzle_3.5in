from MainUIClass.network_utils import getIP
import qrcode
from MainUIClass.config import octopiclient
from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import ThreadRestartNetworking
from MainUIClass.gui_elements import Image
import dialog
import os

class settingsPage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.networkSettingsButton.pressed.connect(
            lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkSettingsPage))
        self.MainUIObj.displaySettingsButton.pressed.connect(
            lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.displaySettingsPage))
        self.MainUIObj.settingsBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.MenuPage))
        self.MainUIObj.pairPhoneButton.pressed.connect(self.pairPhoneApp)
        self.MainUIObj.OTAButton.pressed.connect(self.MainUIObj.softwareUpdatePageInstance.softwareUpdate)
        self.MainUIObj.versionButton.pressed.connect(self.MainUIObj.softwareUpdatePageInstance.displayVersionInfo)

        self.MainUIObj.restartButton.pressed.connect(self.MainUIObj.homePageInstance.askAndReboot)
        self.MainUIObj.restoreFactoryDefaultsButton.pressed.connect(self.restoreFactoryDefaults)
        self.MainUIObj.restorePrintSettingsButton.pressed.connect(self.restorePrintDefaults)

        self.MainUIObj.QRCodeBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.settingsPage))

    def pairPhoneApp(self):
        if getIP(ThreadRestartNetworking.ETH) is not None:
            qrip = getIP(ThreadRestartNetworking.ETH)
        elif getIP(ThreadRestartNetworking.WLAN) is not None:
            qrip = getIP(ThreadRestartNetworking.WLAN)
        else:
            if dialog.WarningOk(self.MainUIObj, "Network Disconnected"):
                return
        self.MainUIObj.QRCodeLabel.setPixmap(
            qrcode.make("http://"+ qrip, image_factory=Image).pixmap())
        self.stackedWidget.setCurrentWidget(self.QRCodePage)

    def restoreFactoryDefaults(self):
        if dialog.WarningYesNo(self.MainUIObj, "Are you sure you want to restore machine state to factory defaults?\nWarning: Doing so will also reset printer profiles, WiFi & Ethernet config.",
                                overlay=True):
            os.system('sudo cp -f config/dhcpcd.conf /etc/dhcpcd.conf')
            os.system('sudo cp -f config/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf')
            os.system('sudo rm -rf /home/pi/.octoprint/users.yaml')
            os.system('sudo cp -f config/users.yaml /home/pi/.octoprint/users.yaml')
            os.system('sudo rm -rf /home/pi/.octoprint/printerProfiles/*')
            os.system('sudo rm -rf /home/pi/.octoprint/scripts/gcode')
            os.system('sudo rm -rf /home/pi/.octoprint/print_restore.json')
            os.system('sudo cp -f config/config.yaml /home/pi/.octoprint/config.yaml')
            # os.system('sudo rm -rf /home/pi/.fw_logo.dat')
            self.MainUIObj.homePageInstance.tellAndReboot("Settings restored. Rebooting...")

    def restorePrintDefaults(self):
        if dialog.WarningYesNo(self.MainUIObj, "Are you sure you want to restore default print settings?\nWarning: Doing so will erase offsets and bed leveling info",
                                overlay=True):
            octopiclient.gcode(command='M502')
            octopiclient.gcode(command='M500')
