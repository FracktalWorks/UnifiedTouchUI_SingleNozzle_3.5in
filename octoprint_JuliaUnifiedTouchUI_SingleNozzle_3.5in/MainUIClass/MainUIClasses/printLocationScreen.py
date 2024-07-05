import mainGUI
from MainUIClass.MainUIClasses.getFilesAndInfo import getFilesAndInfo
from logger import *
import dialog

class printLocationScreen(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting print location screen init.")
        super().__init__()
        
    
    def setup(self, octopiclient):
        try:
            self.octopiclient = octopiclient

            # Connect buttons to functions
            self.printLocationScreenBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
            self.fromLocalButton.pressed.connect(self.fileListLocal)
            self.fromUsbButton.pressed.connect(self.fileListUSB)
        except Exception as e:
            log_error(f"Error setting up print location screen: {str(e)}")
            if dialog.WarningOk(self, f"Error setting up print location screen: {str(e)}", overlay=True):
                pass