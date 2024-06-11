class menuPage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.menuBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage))
        self.MainUIObj.menuControlButton.pressed.connect(self.MainUIObj.controlScreenInstance.control)
        self.MainUIObj.menuPrintButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.printLocationPage))
        self.MainUIObj.menuCalibrateButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        self.MainUIObj.menuSettingsButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.settingsPage))
