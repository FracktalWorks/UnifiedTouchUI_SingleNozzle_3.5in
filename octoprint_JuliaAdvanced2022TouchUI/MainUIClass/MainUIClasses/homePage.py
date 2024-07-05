import dialog
import mainGUI
from MainUIClass.MainUIClasses.socketConnections import printerStatusText
from MainUIClass.MainUIClasses.controlScreen import controlScreen
from logger import *

class homePage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting home page init.")
        self.octopiclient = None
        super().__init__()
    
    def setup(self, octopiclient):
        """
        Sets up signal connections for various UI elements.
        """
        log_info("Setting up homePage.")
        try:
            # self.octopiclient = octopiclient
            log_debug("Octopiclient inside class homePage: " + str(self.octopiclient))
            
            # Connect signals
            self.stopButton.pressed.connect(self.stopActionMessageBox)
            self.menuButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
            self.controlButton.pressed.connect(self.control)
            self.playPauseButton.clicked.connect(self.playPauseAction)
            
            log_info("Setup for homePage complete.")
        except Exception as e:
            error_message = f"Error setting up homePage: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def stopActionMessageBox(self):
        '''
        Displays a message box asking if the user is sure if he wants to turn off the print
        '''
        try:
            log_info("Displaying stop action message box.")
            if dialog.WarningYesNo(self, "Are you sure you want to stop the print?"):
                self.octopiclient.cancelPrint()
                log_info("Print cancelled successfully.")
        except Exception as e:
            error_message = f"Error during stop action: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def playPauseAction(self):
        '''
        Toggles Play/Pause of a print depending on the status of the print
        '''
        try:
            log_info("Performing play/pause action.")
            if printerStatusText == "Operational":
                if self.playPauseButton.isChecked:
                    self.octopiclient.startPrint()
                    log_info("Print started.")
            elif printerStatusText in ["Printing", "Paused"]:
                self.octopiclient.pausePrint()
                log_info("Print paused.")
        except Exception as e:
            error_message = f"Error during play/pause action: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
