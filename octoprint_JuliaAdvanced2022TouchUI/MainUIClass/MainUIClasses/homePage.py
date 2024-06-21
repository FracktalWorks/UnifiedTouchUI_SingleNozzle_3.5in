import dialog
import os
import mainGUI
from MainUIClass.MainUIClasses.threads import octopiclient
from MainUIClass.MainUIClasses.socketConnections import printerStatusText
from MainUIClass.MainUIClasses import controlScreen
from MainUIClass.MainUIClasses.threads import octopiclient

class homePage(mainGUI.Ui_MainWindow):
    def __init__(self):
        self.stopButton.pressed.connect(self.stopActionMessageBox)
        self.menuButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.controlButton.pressed.connect(controlScreen.control)
        self.playPauseButton.clicked.connect(self.playPauseAction)
        super().__init__()

    def stopActionMessageBox(self):
        '''
        Displays a message box asking if the user is sure if he wants to turn off the print
        '''
        if dialog.WarningYesNo(self, "Are you sure you want to stop the print?"):
            octopiclient.cancelPrint()

    def playPauseAction(self):
        '''
        Toggles Play/Pause of a print depending on the status of the print
        '''
        if printerStatusText == "Operational":
            if self.playPauseButton.isChecked:
                octopiclient.startPrint()
        elif printerStatusText == "Printing":
            octopiclient.pausePrint()
        elif printerStatusText == "Paused":
            octopiclient.pausePrint()
