from octoprintAPI import octoprintAPI
import dialog
import mainGUI
from MainUIClass.MainUIClasses.threads import octopiclient

class printRestore(mainGUI.Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def printRestoreMessageBox(self, file):
        '''
        Displays a message box alerting the user of a filament error
        '''
        if dialog.WarningYesNo(self, file + " Did not finish, would you like to restore?"):
            response = octopiclient.restore(restore=True)
            if response["status"] == "Successfully Restored":
                dialog.WarningOk(response["status"])
            else:
                dialog.WarningOk(response["status"])
        else:
            octoprintAPI.restore(restore=False)
