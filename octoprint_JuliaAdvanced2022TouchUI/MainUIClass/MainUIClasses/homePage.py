import dialog
import os
import mainGUI
from MainUIClass.MainUIClasses.socketConnections import printerStatusText
from MainUIClass.MainUIClasses.controlScreen import controlScreen
from logger import *
from MainUIClass.MainUIClasses.controlScreen import controlScreen

class homePage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting home page init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        # self.octopiclient = octopiclient

        log_debug("Octopiclient inside class homePage: " + str(self.octopiclient))
        self.stopButton.pressed.connect(self.stopActionMessageBox)
        self.menuButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.controlButton.pressed.connect(self.control)
        self.playPauseButton.clicked.connect(self.playPauseAction)
        

    def stopActionMessageBox(self):
        '''
        Displays a message box asking if the user is sure if he wants to turn off the print
        '''
        if dialog.WarningYesNo(self, "Are you sure you want to stop the print?"):
            self.octopiclient.cancelPrint()

    def playPauseAction(self):
        '''
        Toggles Play/Pause of a print depending on the status of the print
        '''
        if printerStatusText == "Operational":
            if self.playPauseButton.isChecked:
                self.octopiclient.startPrint()
        elif printerStatusText == "Printing":
            self.octopiclient.pausePrint()
        elif printerStatusText == "Paused":
            self.octopiclient.pausePrint()
