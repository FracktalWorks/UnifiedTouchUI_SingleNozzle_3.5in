from MainUIClass.MainUIClasses.networking_package.wifiSettingsPage import wifiSettingsPage
from MainUIClass.MainUIClasses.networking_package.ethernetSettingsPage import ethernetSettingsPage
from logger import *

class networking(wifiSettingsPage, ethernetSettingsPage):
    def __init__(self):
        log_info("Starting networking init.")
        super().__init__()

    def setup(self):
        wifiSettingsPage.setup(self)
        ethernetSettingsPage.setup(self)

        #network settings page
        self.networkInfoButton.pressed.connect(self.networkInfo)
        self.configureWifiButton.pressed.connect(self.wifiSettings)
        self.configureEthButton.pressed.connect(self.ethSettings)
        self.networkSettingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

        #network info page
        self.networkInfoBackButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.networkSettingsPage))