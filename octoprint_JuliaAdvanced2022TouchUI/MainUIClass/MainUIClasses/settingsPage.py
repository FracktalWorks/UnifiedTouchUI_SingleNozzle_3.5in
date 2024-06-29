from MainUIClass.network_utils import getIP
import qrcode
from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import ThreadRestartNetworking
from MainUIClass.gui_elements import Image
import dialog
import os
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import askAndReboot, tellAndReboot
from MainUIClass.config import ip, apiKey
import requests
from logger import *
from MainUIClass.MainUIClasses.controlScreen import controlScreen

class settingsPage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting settings init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        self.octopiclient = octopiclient
        self.networkSettingsButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))
        self.displaySettingsButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.displaySettingsPage))
        self.settingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.pairPhoneButton.pressed.connect(self.pairPhoneApp)
        self.OTAButton.pressed.connect(self.softwareUpdate)
        self.versionButton.pressed.connect(self.displayVersionInfo)

        self.restartButton.pressed.connect(self.askAndReboot_settings)
        self.restoreFactoryDefaultsButton.pressed.connect(self.restoreFactoryDefaults)
        self.restorePrintSettingsButton.pressed.connect(self.restorePrintDefaults)

        self.QRCodeBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
        

    def askAndReboot_settings(self):
        askAndReboot(self)

    def displayVersionInfo(self):
        self.updateListWidget.clear()
        updateAvailable = False
        self.performUpdateButton.setDisabled(True)

        # Firmware version on the MKS https://github.com/FracktalWorks/OctoPrint-JuliaFirmwareUpdater
        self.updateListWidget.addItem(self.getFirmwareVersion())

        data = self.octopiclient.getSoftwareUpdateInfo()
        if data:
            for item in data["information"]:
                plugin = data["information"][item]
                info = u'\u2713' if not plugin["updateAvailable"] else u'\u2717'
                info += plugin["displayName"] + "  " + plugin["displayVersion"] + "\n"
                info += "   Available: "
                if "information" in plugin and "remote" in plugin["information"] and plugin["information"]["remote"]["value"] is not None:
                    info += plugin["information"]["remote"]["value"]
                else:
                    info += "Unknown"
                self.updateListWidget.addItem(info)

                if plugin["updateAvailable"]:
                    updateAvailable = True

                # if not updatable:
                #     self.updateListWidget.addItem(u'\u2713' + data["information"][item]["displayName"] +
                #                                   "  " + data["information"][item]["displayVersion"] + "\n"
                #                                   + "   Available: " +
                #                                   )
                # else:
                #     updateAvailable = True
                #     self.updateListWidget.addItem(u"\u2717" + data["information"][item]["displayName"] +
                #                                   "  " + data["information"][item]["displayVersion"] + "\n"
                #                                   + "   Available: " +
                #                                   data["information"][item]["information"]["remote"]["value"])

        if updateAvailable:
            self.performUpdateButton.setDisabled(False)
        self.stackedWidget.setCurrentWidget(self.OTAUpdatePage)

    def softwareUpdate(self):
        data = self.octopiclient.getSoftwareUpdateInfo()
        updateAvailable = False
        if data:
            for item in data["information"]:
                if data["information"][item]["updateAvailable"]:
                    updateAvailable = True
        if updateAvailable:
            print('Update Available')
            if dialog.SuccessYesNo(self, "Update Available! Update Now?", overlay=True):
                self.octopiclient.performSoftwareUpdate()
        else:
            if dialog.SuccessOk(self, "System is Up To Date!", overlay=True):
                print('Update Unavailable')


    def pairPhoneApp(self):
        if getIP(ThreadRestartNetworking.ETH) is not None:
            qrip = getIP(ThreadRestartNetworking.ETH)
        elif getIP(ThreadRestartNetworking.WLAN) is not None:
            qrip = getIP(ThreadRestartNetworking.WLAN)
        else:
            if dialog.WarningOk(self, "Network Disconnected"):
                return
        self.QRCodeLabel.setPixmap(
            qrcode.make("http://"+ qrip, image_factory=Image).pixmap())
        self.stackedWidget.setCurrentWidget(self.QRCodePage)

    def restoreFactoryDefaults(self):
        if dialog.WarningYesNo(self, "Are you sure you want to restore machine state to factory defaults?\nWarning: Doing so will also reset printer profiles, WiFi & Ethernet config.",
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
            tellAndReboot(self, "Settings restored. Rebooting...")

    def restorePrintDefaults(self):
        if dialog.WarningYesNo(self, "Are you sure you want to restore default print settings?\nWarning: Doing so will erase offsets and bed leveling info",
                                overlay=True):
            self.octopiclient.gcode(command='M502')
            self.octopiclient.gcode(command='M500')

    def getFirmwareVersion(self):
        try:
            headers = {'X-Api-Key': apiKey}
            req = requests.get('http://{}/plugin/JuliaFirmwareUpdater/hardware/version'.format(ip), headers=headers)
            data = req.json()
            if req.status_code == requests.codes.ok:
                info = u'\u2713' if not data["update_available"] else u"\u2717"    # icon
                info += " Firmware: "
                info += "Unknown" if not data["variant_name"] else data["variant_name"]
                info += "\n"
                if data["variant_name"]:
                    info += "   Installed: "
                    info += "Unknown" if not data["version_board"] else data["version_board"]
                info += "\n"
                info += "" if not data["version_repo"] else "   Available: " + data["version_repo"]
                return info
        except:
            print("Error accessing /plugin/JuliaFirmwareUpdater/hardware/version")
            pass
        return u'\u2713' + "Firmware: Unknown\n"

