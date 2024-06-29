import mainGUI
from logger import *
from MainUIClass.MainUIClasses.controlScreen import controlScreen

class softwareUpdatePage(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting software update init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        self.octopiclient = octopiclient
        self.softwareUpdateBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
        self.performUpdateButton.pressed.connect(lambda: self.octopiclient.performSoftwareUpdate())
        

