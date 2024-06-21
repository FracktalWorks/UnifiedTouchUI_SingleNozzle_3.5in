from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import wifiSettingsPage
from MainUIClass.MainUIClasses.networking_package.ethernetSettingsPage import ethernetSettingsPage

class networking(wifiSettingsPage, ethernetSettingsPage):
    def __init__(self, MainUIObj):
        self = MainUIObj
        wifiSettingsPage.__init__(self)
        ethernetSettingsPage.__init__(self)
        super().__init__()

    def connect(self):
        wifiSettingsPage.connect(self)
        ethernetSettingsPage.connect(self)

        #network settings page
        self.networkInfoButton.pressed.connect(self.networkInfo)
        self.configureWifiButton.pressed.connect(self.wifiSettings)
        self.configureEthButton.pressed.connect(self.ethSettings)
        self.networkSettingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

        #network info page
        self.networkInfoBackButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))