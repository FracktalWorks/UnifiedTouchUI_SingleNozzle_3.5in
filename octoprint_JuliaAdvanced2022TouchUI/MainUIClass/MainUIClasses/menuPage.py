import mainGUI
from MainUIClass.MainUIClasses.controlScreen import controlScreen
from logger import *
import dialog

class menuPage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting menu page init.")
        super().__init__()
    
    def setup(self, octopiclient):
        """
        Sets up signal connections for menu page UI elements.
        """
        log_info("Setting up menu page.")
        try:
            self.menuBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
            self.menuControlButton.pressed.connect(self.control)
            self.menuPrintButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.printLocationPage))
            self.menuCalibrateButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.calibratePage))
            self.menuSettingsButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
            
            log_info("Menu page setup completed.")
        except Exception as e:
            error_message = f"Error setting up menu page: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
