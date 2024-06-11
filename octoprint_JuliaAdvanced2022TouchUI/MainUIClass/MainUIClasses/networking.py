from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import wifiSettingsPage
from MainUIClass.MainUIClasses.networking_package.ethernetSettingsPage import ethernetSettingsPage

class networking(wifiSettingsPage, ethernetSettingsPage):
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj
        wifiSettingsPage.__init__(self, MainUIObj=MainUIObj)
        ethernetSettingsPage.__init__(self, MainUIObj=MainUIObj)

    def connect(self):
        wifiSettingsPage.connect(self)
        ethernetSettingsPage.connect(self)

        #network settings page
        self.MainUIObj.networkInfoButton.pressed.connect(self.networkInfo)
        self.MainUIObj.configureWifiButton.pressed.connect(self.wifiSettings)
        self.MainUIObj.configureEthButton.pressed.connect(self.ethSettings)
        self.MainUIObj.networkSettingsBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.settingsPage))

        #network info page
        self.MainUIObj.networkInfoBackButton.pressed.connect(
            lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.networkSettingsPage))