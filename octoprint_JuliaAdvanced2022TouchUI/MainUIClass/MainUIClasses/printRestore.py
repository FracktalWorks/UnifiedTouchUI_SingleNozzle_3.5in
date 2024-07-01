from octoprintAPI import octoprintAPI
import dialog
import mainGUI
from logger import *
from MainUIClass.MainUIClasses.controlScreen import controlScreen

class printRestore(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting print restore init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        # self.octopiclient = octopiclient

        log_debug("Octopiclient inside class printRestore: " + str(self.octopiclient))

    def printRestoreMessageBox(self, file):
        '''
        Displays a message box alerting the user of a filament error
        '''
        if dialog.WarningYesNo(self, file + " Did not finish, would you like to restore?"):
            response = self.octopiclient.restore(restore=True)
            if response["status"] == "Successfully Restored":
                dialog.WarningOk(response["status"])
            else:
                dialog.WarningOk(response["status"])
        else:
            octoprintAPI.restore(restore=False)
