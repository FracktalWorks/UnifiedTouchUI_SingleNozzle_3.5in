import io
import subprocess
from PyQt5 import QtWidgets, QtCore
import dialog
from MainUIClass.network_utils import *
import time
import mainGUI
from MainUIClass.decorators import run_async
from MainUIClass.MainUIClasses.start_keyboard import startKeyboard
from MainUIClass.MainUIClasses.lineEdits import lineEdits
from logger import *
from MainUIClass.MainUIClasses.start_keyboard import startKeyboard

class wifiSettingsPage(lineEdits, mainGUI.Ui_MainWindow):
    def __init__(self):
        """
        Initializes the WiFi settings page.

        """
        log_info("Starting wifi settings init.")
        super().__init__()

    def setup(self):
        """
        Sets up connections for GUI elements and buttons related to WiFi settings.

        """
        self.wifiPasswordLineEdit.clicked_signal.connect(lambda: startKeyboard(self, self.wifiPasswordLineEdit.setText))
        self.wifiSettingsSSIDKeyboardButton.pressed.connect(
            lambda: startKeyboard(self, self.wifiSettingsComboBox.addItem))
        self.wifiSettingsCancelButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))
        self.wifiSettingsDoneButton.pressed.connect(self.acceptWifiSettings)

    def acceptWifiSettings(self):
        """
        Accepts and saves WiFi settings entered by the user.

        """
        wlan0_config_file = io.open("/etc/wpa_supplicant/wpa_supplicant.conf", "r+", encoding='utf8')
        wlan0_config_file.truncate()
        ascii_ssid = self.wifiSettingsComboBox.currentText()
        wlan0_config_file.write(u"country=IN\n")
        wlan0_config_file.write(u"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        wlan0_config_file.write(u"update_config=1\n")
        wlan0_config_file.write(u"network={\n")
        wlan0_config_file.write(u'ssid="' + str(ascii_ssid) + '"\n')
        if self.hiddenCheckBox.isChecked():
            wlan0_config_file.write(u'scan_ssid=1\n')
        if str(self.wifiPasswordLineEdit.text()) != "":
            wlan0_config_file.write(u'psk="' + str(self.wifiPasswordLineEdit.text()) + '"\n')
        wlan0_config_file.write(u'}')
        wlan0_config_file.close()

        self.restartWifiThreadMainUIObject = ThreadRestartNetworking(ThreadRestartNetworking.WLAN)
        self.restartWifiThreadMainUIObject.signal.connect(self.wifiReconnectResult)
        self.restartWifiThreadMainUIObject.start()

        self.wifiMessageBox = dialog.dialog(self,
                                           "Restarting networking, please wait...",
                                           icon="exclamation-mark.png",
                                           buttons=QtWidgets.QMessageBox.Cancel)
        if self.wifiMessageBox.exec_() in {QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel}:
            self.stackedWidget.setCurrentWidget(self.networkSettingsPage)

    def wifiReconnectResult(self, x):
        """
        Handles the result of WiFi network reconnection.

        """
        self.wifiMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if x is not None:
            print("Ouput from signal " + x)
            self.wifiMessageBox.setLocalIcon('success.png')
            self.wifiMessageBox.setText('Connected, IP: ' + x)
            self.wifiMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.ipStatus.setText(x)  # sets the IP address in the status bar
        else:
            self.wifiMessageBox.setText("Not able to connect to WiFi")

    def networkInfo(self):
        """
        Retrieves and displays current network information.

        """
        ipWifi = getIP(ThreadRestartNetworking.WLAN)
        ipEth = getIP(ThreadRestartNetworking.ETH)

        self.hostname.setText(getHostname())
        self.wifiAp.setText(getWifiAp())
        self.wifiIp.setText("Not connected" if not ipWifi else ipWifi)
        self.ipStatus.setText("Not connected" if not ipWifi else ipWifi)
        self.lanIp.setText("Not connected" if not ipEth else ipEth)
        self.wifiMac.setText(getMac(ThreadRestartNetworking.WLAN).decode('utf8'))
        self.lanMac.setText(getMac(ThreadRestartNetworking.ETH).decode('utf8'))
        self.stackedWidget.setCurrentWidget(self.networkInfoPage)

    def wifiSettings(self):
        """
        Displays the WiFi settings page and scans available networks.

        """
        self.stackedWidget.setCurrentWidget(self.wifiSettingsPage)
        self.wifiSettingsComboBox.clear()
        self.wifiSettingsComboBox.addItems(self.scan_wifi())

    def scan_wifi(self):
        """
        Scans available WiFi networks.

        Returns:
            list: List of available SSIDs.

        """
        scan_result = subprocess.Popen("iwlist wlan0 scan | grep 'ESSID'", stdout=subprocess.PIPE, shell=True).communicate()[0]
        scan_result = scan_result.decode('utf8').split('ESSID:')
        scan_result = [s.strip() for s in scan_result]
        scan_result = [s.strip('"') for s in scan_result]
        scan_result = filter(None, scan_result)
        return scan_result

    @run_async
    def setIPStatus(self):
        """
        Updates IP address of the printer on the status bar.

        """
        while True:
            try:
                if getIP("eth0"):
                    self.ipStatus.setText(getIP("eth0"))
                elif getIP("wlan0"):
                    self.ipStatus.setText(getIP("wlan0"))
                else:
                    self.ipStatus.setText("Not connected")
            except:
                self.ipStatus.setText("Not connected")
            time.sleep(60)


class ThreadRestartNetworking(QtCore.QThread):
    WLAN = "wlan0"
    ETH = "eth0"
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, interface):
        """
        Initializes the thread for restarting networking.

        Args:
            interface (str): Interface name ('wlan0' or 'eth0').

        """
        super(ThreadRestartNetworking, self).__init__()
        self.interface = interface

    def run(self):
        """
        Runs the thread to restart the specified network interface.

        """
        self.restart_interface()
        attempt = 0
        while attempt < 3:
            if getIP(self.interface):
                self.signal.emit(getIP(self.interface))
                break
            else:
                attempt += 1
                time.sleep(5)
        if attempt >= 3:
            self.signal.emit(None)

    def restart_interface(self):
        """
        Restarts the specified network interface.

        """
        if self.interface == "wlan0":
            subprocess.call(["wpa_cli", "-i",  self.interface, "reconfigure"], shell=False)
        if self.interface == "eth0":
            subprocess.call(["ifconfig",  self.interface, "down"], shell=False)
            time.sleep(1)
            subprocess.call(["ifconfig", self.interface, "up"], shell=False)
        time.sleep(5)