import io
import subprocess
from PyQt5 import QtWidgets, QtCore
import dialog
from MainUIClass.network_utils import *
import time
from MainUIClass.decorators import run_async

class wifiSettingsPage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.wifiSettingsSSIDKeyboardButton.pressed.connect(
            lambda: self.MainUIObj.startKeyboard(self.MainUIObj.wifiSettingsComboBox.addItem))
        self.MainUIObj.wifiSettingsCancelButton.pressed.connect(
            lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkSettingsPage))
        self.MainUIObj.wifiSettingsDoneButton.pressed.connect(self.acceptWifiSettings)

    def acceptWifiSettings(self):
        wlan0_config_file = io.open("/etc/wpa_supplicant/wpa_supplicant.conf", "r+", encoding='utf8')
        wlan0_config_file.truncate()
        ascii_ssid = self.MainUIObj.wifiSettingsComboBox.currentText()
        # unicode_ssid = ascii_ssid.decode('string_escape').decode('utf-8')
        wlan0_config_file.write(u"country=IN\n")
        wlan0_config_file.write(u"ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
        wlan0_config_file.write(u"update_config=1\n")
        wlan0_config_file.write(u"network={\n")
        wlan0_config_file.write(u'ssid="' + str(ascii_ssid) + '"\n')
        if self.MainUIObj.hiddenCheckBox.isChecked():
            wlan0_config_file.write(u'scan_ssid=1\n')
        # wlan0_config_file.write(u"scan_ssid=1\n")
        if str(self.MainUIObj.wifiPasswordLineEdit.text()) != "":
            wlan0_config_file.write(u'psk="' + str(self.MainUIObj.wifiPasswordLineEdit.text()) + '"\n')
        # wlan0_config_file.write(u"key_mgmt=WPA-PSK\n")
        wlan0_config_file.write(u'}')
        wlan0_config_file.close()
        self.MainUIObj.restartWifiThreadMainUIObject = ThreadRestartNetworking(ThreadRestartNetworking.WLAN)
        self.MainUIObj.restartWifiThreadMainUIObject.signal.connect(self.wifiReconnectResult)
        self.MainUIObj.restartWifiThreadMainUIObject.start()
        self.MainUIObj.wifiMessageBox = dialog.dialog(self.MainUIObj,
                                                "Restarting networking, please wait...",
                                                icon="exclamation-mark.png",
                                                buttons=QtWidgets.QMessageBox.Cancel) 
        if self.MainUIObj.wifiMessageBox.exec_() in {QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel}:
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkSettingsPage)

    def wifiReconnectResult(self, x):
        self.MainUIObj.wifiMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if x is not None:
            print("Ouput from signal " + x)
            self.MainUIObj.wifiMessageBox.setLocalIcon('success.png')
            self.MainUIObj.wifiMessageBox.setText('Connected, IP: ' + x)
            self.MainUIObj.wifiMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.MainUIObj.ipStatus.setText(x) #sets the IP addr. in the status bar

        else:
            self.MainUIObj.wifiMessageBox.setText("Not able to connect to WiFi")

    def networkInfo(self):
        ipWifi = getIP(ThreadRestartNetworking.WLAN)
        ipEth = getIP(ThreadRestartNetworking.ETH)

        self.MainUIObj.hostname.setText(getHostname())
        self.MainUIObj.wifiAp.setText(getWifiAp())
        self.MainUIObj.wifiIp.setText("Not connected" if not ipWifi else ipWifi)
        self.MainUIObj.ipStatus.setText("Not connected" if not ipWifi else ipWifi)
        self.MainUIObj.lanIp.setText("Not connected" if not ipEth else ipEth)
        self.MainUIObj.wifiMac.setText(getMac(ThreadRestartNetworking.WLAN).decode('utf8'))
        self.MainUIObj.lanMac.setText(getMac(ThreadRestartNetworking.ETH).decode('utf8'))
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkInfoPage)

    def wifiSettings(self):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.wifiSettingsPage)
        self.MainUIObj.wifiSettingsComboBox.clear()
        self.MainUIObj.wifiSettingsComboBox.addItems(self.scan_wifi())

    def scan_wifi(self):
        '''
        uses linux shell and WIFI interface to scan available networks
        :return: dictionary of the SSID and the signal strength
        '''
        # scanData = {}
        # print "Scanning available wireless signals available to wlan0"
        scan_result = \
            subprocess.Popen("iwlist wlan0 scan | grep 'ESSID'", stdout=subprocess.PIPE, shell=True).communicate()[0]
        # Processing STDOUT into a dictionary that later will be converted to a json file later
        scan_result = scan_result.decode('utf8').split('ESSID:')  # each ssid and pass from an item in a list ([ssid pass,ssid pass])
        scan_result = [s.strip() for s in scan_result]
        scan_result = [s.strip('"') for s in scan_result]
        scan_result = filter(None, scan_result)
        return scan_result

    @run_async
    def setIPStatus(self):
        '''
        Function to update IP address of printer on the status bar. Refreshes at a particular interval.
        '''
        while(True):
            try:
                if getIP("eth0"):
                    self.MainUIObj.ipStatus.setText(getIP("eth0"))
                elif getIP("wlan0"):
                    self.MainUIObj.ipStatus.setText(getIP("wlan0"))
                else:
                    self.MainUIObj.ipStatus.setText("Not connected")

            except:
                self.MainUIObj.ipStatus.setText("Not connected")
            time.sleep(60)

class ThreadRestartNetworking(QtCore.QThread):
    WLAN = "wlan0"
    ETH = "eth0"
    signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, interface):
        super(ThreadRestartNetworking, self).__init__()
        self.interface = interface
    def run(self):
        self.restart_interface()
        attempt = 0
        while attempt < 3:
            # print(getIP(self.interface))
            if getIP(self.interface):
                self.signal.emit(getIP(self.interface))
                break
            else:
                attempt += 1
                time.sleep(5)
        if attempt >= 3:
            self.signal.emit(None)

    def restart_interface(self):
        '''
        restars wlan0 wireless interface to use new changes in wpa_supplicant.conf file
        :return:
        '''
        if self.interface == "wlan0":
            subprocess.call(["wpa_cli","-i",  self.interface, "reconfigure"], shell=False)
        if self.interface == "eth0":
            subprocess.call(["ifconfig",  self.interface, "down"], shell=False)
            time.sleep(1)
            subprocess.call(["ifconfig", self.interface, "up"], shell=False)
        # subprocess.call(["ifdown", "--force", self.interface], shell=False)
        # subprocess.call(["ifup", "--force", self.interface], shell=False)
        time.sleep(5)
