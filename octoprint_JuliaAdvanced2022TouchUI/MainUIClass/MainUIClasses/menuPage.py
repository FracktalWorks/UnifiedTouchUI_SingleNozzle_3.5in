import mainGUI
from MainUIClass.MainUIClasses import controlScreen

class menuPage(mainGUI.Ui_MainWindow):
    def __init__(self, MainUIObj):
        self.menuBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.menuControlButton.pressed.connect(controlScreen.control)
        self.menuPrintButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.printLocationPage))
        self.menuCalibrateButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.calibratePage))
        self.menuSettingsButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
