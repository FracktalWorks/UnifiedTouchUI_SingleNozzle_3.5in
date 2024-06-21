from MainUIClass.config import filaments
import mainGUI
from MainUIClass.MainUIClasses import controlScreen
from MainUIClass.MainUIClasses.socketConnections import printerStatusText
from logger import *

class changeFilamentRoutine(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting change filemanet init.")
        self.octopiclient = None
        super().__init__()
        
    def setup(self):        
        from MainUIClass.MainUIClasses.threads import octopiclient
        self.octopiclient = octopiclient
        self.changeFilamentButton.pressed.connect(self.changeFilament)
        self.changeFilamentBackButton.pressed.connect(controlScreen.control)
        self.changeFilamentBackButton2.pressed.connect(self.changeFilamentCancel)
        self.changeFilamentUnloadButton.pressed.connect(lambda: self.unloadFilament())
        self.changeFilamentLoadButton.pressed.connect(lambda: self.loadFilament())
        self.loadDoneButton.pressed.connect(controlScreen.control)
        self.unloadDoneButton.pressed.connect(self.changeFilament)
        self.retractFilamentButton.pressed.connect(lambda: self.octopiclient.extrude(-20))
        self.ExtrudeButton.pressed.connect(lambda: self.octopiclient.extrude(20))

    def unloadFilament(self):
        # Update
        if self.changeFilamentComboBox.findText("Loaded Filament") == -1:
            self.octopiclient.setToolTemperature(
                filaments[str(self.changeFilamentComboBox.currentText())])
        self.stackedWidget.setCurrentWidget(self.changeFilamentProgressPage)
        self.changeFilamentStatus.setText("Heating , Please Wait...")
        self.changeFilamentNameOperation.setText("Unloading {}".format(str(self.changeFilamentComboBox.currentText())))
        # This flag tells the updateTemperature function that runs every second to update the filament change progress bar as well, and to load or unload after heating done
        self.changeFilamentHeatingFlag = True
        self.loadFlag = False

    def loadFilament(self):
        # Update
        if self.changeFilamentComboBox.findText("Loaded Filament") == -1:
            self.octopiclient.setToolTemperature(
                filaments[str(self.changeFilamentComboBox.currentText())])
        self.stackedWidget.setCurrentWidget(self.changeFilamentProgressPage)
        self.changeFilamentStatus.setText("Heating , Please Wait...")
        self.changeFilamentNameOperation.setText("Loading {}".format(str(self.changeFilamentComboBox.currentText())))
        # This flag tells the updateTemperature function that runs every second to update the filament change progress bar as well, and to load or unload after heating done
        self.changeFilamentHeatingFlag = True
        self.loadFlag = True

    def changeFilament(self):
        self.stackedWidget.setCurrentWidget(self.changeFilamentPage)
        self.changeFilamentComboBox.clear()
        self.changeFilamentComboBox.addItems(filaments.keys())
        # Update
        print(self.tool0TargetTemperature)
        if self.tool0TargetTemperature and printerStatusText in ["Printing", "Paused"]:
            self.changeFilamentComboBox.addItem("Loaded Filament")
            index = self.changeFilamentComboBox.findText("Loaded Filament")
            if index >= 0:
                self.changeFilamentComboBox.setCurrentIndex(index)

    def changeFilamentCancel(self):
        self.changeFilamentHeatingFlag = False
        controlScreen.coolDownAction(self)
        controlScreen.control(self)
