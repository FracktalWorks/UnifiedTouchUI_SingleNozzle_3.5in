import subprocess
from PyQt5 import QtWidgets
import dialog
from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import ThreadRestartNetworking
from MainUIClass.network_utils import *
import re

class ethernetSettingsPage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.ethStaticCheckBox.stateChanged.connect(self.ethStaticChanged)
        self.MainUIObj.ethStaticCheckBox.stateChanged.connect(lambda: self.MainUIObj.ethStaticSettings.setVisible(self.MainUIObj.ethStaticCheckBox.isChecked()))
        self.MainUIObj.ethStaticIpKeyboardButton.pressed.connect(lambda: self.MainUIObj.ethShowKeyboard(self.MainUIObj.ethStaticIpLineEdit))
        self.MainUIObj.ethStaticGatewayKeyboardButton.pressed.connect(lambda: self.MainUIObj.ethShowKeyboard(self.MainUIObj.ethStaticGatewayLineEdit))
        self.MainUIObj.ethSettingsDoneButton.pressed.connect(self.ethSaveStaticNetworkInfo)
        self.MainUIObj.ethSettingsCancelButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkSettingsPage))

    def ethSettings(self):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.ethSettingsPage)
        self.ethNetworkInfo()

    def ethStaticChanged(self, state):
        self.MainUIObj.ethStaticSettings.setVisible(self.MainUIObj.ethStaticCheckBox.isChecked())
        self.MainUIObj.ethStaticSettings.setEnabled(self.MainUIObj.ethStaticCheckBox.isChecked())

    def ethNetworkInfo(self):
        txt = subprocess.Popen("cat /etc/dhcpcd.conf", stdout=subprocess.PIPE, shell=True).communicate()[0]

        reEthGlobal = b"interface\s+eth0\s?(static\s+[a-z0-9./_=\s]+\n)*"
        reEthAddress = b"static\s+ip_address=([\d.]+)(/[\d]{1,2})?"
        reEthGateway = b"static\s+routers=([\d.]+)(/[\d]{1,2})?"

        mtEthGlobal = re.search(reEthGlobal, txt)

        cbStaticEnabled = False
        txtEthAddress = ""
        txtEthGateway = ""

        if mtEthGlobal:
            sz = len(mtEthGlobal.groups())
            cbStaticEnabled = (sz == 1)

            if sz == 1:
                mtEthAddress = re.search(reEthAddress, mtEthGlobal.group(0))
                if mtEthAddress and len(mtEthAddress.groups()) == 2:
                    txtEthAddress = mtEthAddress.group(1)
                mtEthGateway = re.search(reEthGateway, mtEthGlobal.group(0))
                if mtEthGateway and len(mtEthGateway.groups()) == 2:
                    txtEthGateway = mtEthGateway.group(1)

        self.MainUIObj.ethStaticCheckBox.setChecked(cbStaticEnabled)
        self.MainUIObj.ethStaticSettings.setVisible(cbStaticEnabled)
        self.MainUIObj.ethStaticIpLineEdit.setText(txtEthAddress)
        self.MainUIObj.ethStaticGatewayLineEdit.setText(txtEthGateway)

    def isIpErr(self, ip):
        return (re.search(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", ip) is None)

    def showIpErr(self, var):
        return dialog.WarningOk(self.MainUIObj, "Invalid input: {0}".format(var))

    def ethSaveStaticNetworkInfo(self):
        cbStaticEnabled = self.MainUIObj.ethStaticCheckBox.isChecked()
        txtEthAddress = str(self.MainUIObj.ethStaticIpLineEdit.text())
        txtEthGateway = str(self.MainUIObj.ethStaticGatewayLineEdit.text())

        if cbStaticEnabled:
            if self.isIpErr(txtEthAddress):
                return self.showIpErr("IP Address")
            if self.isIpErr(txtEthGateway):
                return self.showIpErr("Gateway")

        txt = subprocess.Popen("cat /etc/dhcpcd.conf", stdout=subprocess.PIPE, shell=True).communicate()[0]
        op = ""

        reEthGlobal = r"interface\s+eth0"
        mtEthGlobal = re.search(reEthGlobal, txt)

        if cbStaticEnabled:
            if not mtEthGlobal:
                txt = txt + "\n" + "interface eth0" + "\n"
            op = "interface eth0\nstatic ip_address={0}/24\nstatic routers={1}\nstatic domain_name_servers=8.8.8.8 8.8.4.4\n\n".format(txtEthAddress, txtEthGateway)

        res = re.sub(r"interface\s+eth0\s?(static\s+[a-z0-9./_=\s]+\n)*", op, txt)
        try:
            file = open("/etc/dhcpcd.conf", "w")
            file.write(res)
            file.close()
        except:
            if dialog.WarningOk(self.MainUIObj, "Failed to change Ethernet Interface configuration."):
                pass

        self.MainUIObj.restartEthThreadObject = ThreadRestartNetworking(ThreadRestartNetworking.ETH)
        self.MainUIObj.restartEthThreadObject.signal.connect(self.ethReconnectResult)
        self.MainUIObj.restartEthThreadObject.start()
        self.MainUIObj.ethMessageBox = dialog.dialog(self.MainUIObj,
                                               "Restarting networking, please wait...",
                                               icon="exclamation-mark.png",
                                               buttons=QtWidgets.QMessageBox.Cancel)
        if self.MainUIObj.ethMessageBox.exec_() in {QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel}:
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkSettingsPage)

    def ethReconnectResult(self, x):
        self.MainUIObj.ethMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if x is not None:
            self.MainUIObj.ethMessageBox.setLocalIcon('success.png')
            self.MainUIObj.ethMessageBox.setText('Connected, IP: ' + x)
        else:
            self.MainUIObj.ethMessageBox.setText("Not able to connect to Ethernet")

    def ethShowKeyboard(self, textbox):
        self.MainUIObj.startKeyboard(textbox.setText, onlyNumeric=True, noSpace=True, text=str(textbox.text()))
