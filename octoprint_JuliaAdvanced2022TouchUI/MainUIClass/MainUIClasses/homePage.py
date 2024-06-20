import dialog
import os


class homePage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.stopButton.pressed.connect(self.stopActionMessageBox)
        self.MainUIObj.menuButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.MenuPage))
        self.MainUIObj.controlButton.pressed.connect(self.MainUIObj.controlScreenInstance.control)
        self.MainUIObj.playPauseButton.clicked.connect(self.playPauseAction)

    def tellAndReboot(self, msg="Rebooting...", overlay=True):
        if dialog.WarningOk(self.MainUIObj, msg, overlay=overlay):
            os.system('sudo reboot now')
            return True
        return False

    def askAndReboot(self, msg="Are you sure you want to reboot?", overlay=True):
        if dialog.WarningYesNo(self.MainUIObj, msg, overlay=overlay):
            os.system('sudo reboot now')
            return True
        return False

    def stopActionMessageBox(self):
        '''
        Displays a message box asking if the user is sure if he wants to turn off the print
        '''
        if dialog.WarningYesNo(self.MainUIObj, "Are you sure you want to stop the print?"):
            self.MainUIObj.octopiclient.cancelPrint()

    def playPauseAction(self):
        '''
        Toggles Play/Pause of a print depending on the status of the print
        '''
        if self.MainUIObj.printerStatusText == "Operational":
            if self.MainUIObj.playPauseButton.isChecked:
                self.MainUIObj.octopiclient.startPrint()
        elif self.MainUIObj.printerStatusText == "Printing":
            self.MainUIObj.octopiclient.pausePrint()
        elif self.MainUIObj.printerStatusText == "Paused":
            self.MainUIObj.octopiclient.resumePrint()
