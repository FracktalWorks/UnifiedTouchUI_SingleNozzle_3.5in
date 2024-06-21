import subprocess
from PyQt5 import QtWidgets
import dialog
from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import ThreadRestartNetworking
from MainUIClass.network_utils import *
import re
import mainGUI
from MainUIClass.MainUIClasses.lineEdits import lineEdits
from logger import *

class ethernetSettingsPage(lineEdits, mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting eth settings init.")
        super().__init__()

    def setup(self):
        self.ethStaticCheckBox.stateChanged.connect(self.ethStaticChanged)
        self.ethStaticCheckBox.stateChanged.connect(lambda: self.ethStaticSettings.setVisible(self.ethStaticCheckBox.isChecked()))
        self.ethStaticIpKeyboardButton.pressed.connect(lambda: self.ethShowKeyboard(self.ethStaticIpLineEdit))
        self.ethStaticGatewayKeyboardButton.pressed.connect(lambda: self.ethShowKeyboard(self.ethStaticGatewayLineEdit))
        self.ethSettingsDoneButton.pressed.connect(self.ethSaveStaticNetworkInfo)
        self.ethSettingsCancelButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))

    def ethSettings(self):
        self.stackedWidget.setCurrentWidget(self.ethSettingsPage)
        self.ethNetworkInfo()

    def ethStaticChanged(self, state):
        self.ethStaticSettings.setVisible(self.ethStaticCheckBox.isChecked())
        self.ethStaticSettings.setEnabled(self.ethStaticCheckBox.isChecked())

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

        self.ethStaticCheckBox.setChecked(cbStaticEnabled)
        self.ethStaticSettings.setVisible(cbStaticEnabled)
        self.ethStaticIpLineEdit.setText(txtEthAddress)
        self.ethStaticGatewayLineEdit.setText(txtEthGateway)

    def isIpErr(self, ip):
        return (re.search(r"^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", ip) is None)

    def showIpErr(self, var):
        return dialog.WarningOk(self, "Invalid input: {0}".format(var))

    def ethSaveStaticNetworkInfo(self):
        cbStaticEnabled = self.ethStaticCheckBox.isChecked()
        txtEthAddress = str(self.ethStaticIpLineEdit.text())
        txtEthGateway = str(self.ethStaticGatewayLineEdit.text())

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
            if dialog.WarningOk(self, "Failed to change Ethernet Interface configuration."):
                pass

        self.restartEthThreadObject = ThreadRestartNetworking(ThreadRestartNetworking.ETH)
        self.restartEthThreadObject.signal.connect(self.ethReconnectResult)
        self.restartEthThreadObject.start()
        self.ethMessageBox = dialog.dialog(self,
                                               "Restarting networking, please wait...",
                                               icon="exclamation-mark.png",
                                               buttons=QtWidgets.QMessageBox.Cancel)
        if self.ethMessageBox.exec_() in {QtWidgets.QMessageBox.Ok, QtWidgets.QMessageBox.Cancel}:
            self.stackedWidget.setCurrentWidget(self.networkSettingsPage)

    def ethReconnectResult(self, x):
        self.ethMessageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        if x is not None:
            self.ethMessageBox.setLocalIcon('success.png')
            self.ethMessageBox.setText('Connected, IP: ' + x)
        else:
            self.ethMessageBox.setText("Not able to connect to Ethernet")

    def ethShowKeyboard(self, textbox):
        self.startKeyboard(textbox.setText, onlyNumeric=True, noSpace=True, text=str(textbox.text()))
