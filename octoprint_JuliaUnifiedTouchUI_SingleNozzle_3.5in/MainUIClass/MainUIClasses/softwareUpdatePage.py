import mainGUI
from logger import *
from MainUIClass.MainUIClasses.controlScreen import controlScreen
import dialog

class softwareUpdatePage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting software update init.")
        self.octopiclient = None
        super().__init__()
    
    def setup(self, octopiclient):
        try:
            self.octopiclient = octopiclient
            log_debug("Octopiclient inside class softwareUpdatePage: " + str(self.octopiclient))
            
            self.softwareUpdateBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
            self.performUpdateButton.pressed.connect(lambda: self.octopiclient.performSoftwareUpdate())
        
        except Exception as e:
            error_message = f"Error in setup function of softwareUpdatePage: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
