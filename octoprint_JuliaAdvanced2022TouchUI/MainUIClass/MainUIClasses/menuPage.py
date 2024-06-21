import mainGUI
from MainUIClass.MainUIClasses import controlScreen
from logger import *

class menuPage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting menu page init.")
        super().__init__()

    def setup(self):
        self.menuBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.menuControlButton.pressed.connect(controlScreen.control)
        self.menuPrintButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.printLocationPage))
        self.menuCalibrateButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.calibratePage))
        self.menuSettingsButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
