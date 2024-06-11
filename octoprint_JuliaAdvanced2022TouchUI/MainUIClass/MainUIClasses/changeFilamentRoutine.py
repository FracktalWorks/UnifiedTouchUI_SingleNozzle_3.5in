from MainUIClass.config import octopiclient
from MainUIClass.config import filaments

class changeFilamentRoutine:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.changeFilamentButton.pressed.connect(self.changeFilament)
        self.MainUIObj.changeFilamentBackButton.pressed.connect(self.MainUIObj.controlScreenInstance.control)
        self.MainUIObj.changeFilamentBackButton2.pressed.connect(self.changeFilamentCancel)
        self.MainUIObj.changeFilamentUnloadButton.pressed.connect(lambda: self.unloadFilament())
        self.MainUIObj.changeFilamentLoadButton.pressed.connect(lambda: self.loadFilament())
        self.MainUIObj.loadDoneButton.pressed.connect(self.MainUIObj.controlScreenInstance.control)
        self.MainUIObj.unloadDoneButton.pressed.connect(self.changeFilament)
        self.MainUIObj.retractFilamentButton.pressed.connect(lambda: octopiclient.extrude(-20))
        self.MainUIObj.ExtrudeButton.pressed.connect(lambda: octopiclient.extrude(20))

    def unloadFilament(self):
        # Update
        if self.MainUIObj.changeFilamentComboBox.findText("Loaded Filament") == -1:
            octopiclient.setToolTemperature(
                filaments[str(self.MainUIObj.changeFilamentComboBox.currentText())])
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.changeFilamentProgressPage)
        self.MainUIObj.changeFilamentStatus.setText("Heating , Please Wait...")
        self.MainUIObj.changeFilamentNameOperation.setText("Unloading {}".format(str(self.MainUIObj.changeFilamentComboBox.currentText())))
        # This flag tells the updateTemperature function that runs every second to update the filament change progress bar as well, and to load or unload after heating done
        self.MainUIObj.changeFilamentHeatingFlag = True
        self.MainUIObj.loadFlag = False

    def loadFilament(self):
        # Update
        if self.MainUIObj.changeFilamentComboBox.findText("Loaded Filament") == -1:
            octopiclient.setToolTemperature(
                filaments[str(self.MainUIObj.changeFilamentComboBox.currentText())])
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.changeFilamentProgressPage)
        self.MainUIObj.changeFilamentStatus.setText("Heating , Please Wait...")
        self.MainUIObj.changeFilamentNameOperation.setText("Loading {}".format(str(self.MainUIObj.changeFilamentComboBox.currentText())))
        # This flag tells the updateTemperature function that runs every second to update the filament change progress bar as well, and to load or unload after heating done
        self.MainUIObj.changeFilamentHeatingFlag = True
        self.MainUIObj.loadFlag = True

    def changeFilament(self):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.changeFilamentPage)
        self.MainUIObj.changeFilamentComboBox.clear()
        self.MainUIObj.changeFilamentComboBox.addItems(filaments.keys())
        # Update
        print(self.MainUIObj.tool0TargetTemperature)
        if self.MainUIObj.tool0TargetTemperature and self.MainUIObj.printerStatusText in ["Printing", "Paused"]:
            self.MainUIObj.changeFilamentComboBox.addItem("Loaded Filament")
            index = self.MainUIObj.changeFilamentComboBox.findText("Loaded Filament")
            if index >= 0:
                self.MainUIObj.changeFilamentComboBox.setCurrentIndex(index)

    def changeFilamentCancel(self):
        self.MainUIObj.changeFilamentHeatingFlag = False
        self.MainUIObj.coolDownAction()
        self.MainUIObj.controlScreenInstance.control()
