from MainUIClass.config import filaments
import mainGUI
from MainUIClass.MainUIClasses.controlScreen import controlScreen
from MainUIClass.MainUIClasses.socketConnections import printerStatusText
from logger import *
import dialog

class changeFilamentRoutine(mainGUI.Ui_MainWindow):
    def __init__(self):
        try:
            log_info("Starting change filament init.")
            self.octopiclient = None
            super().__init__()
            log_info("Completed change filament init.")
        except Exception as e:
            error_message = f"Error in changeFilamentRoutine __init__: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def setup(self, octopiclient):
        try:
            log_info("Starting setup.")
            # self.octopiclient = octopiclient

            log_debug("Octopiclient inside class changeFilamentRoutine: " + str(self.octopiclient))
            self.changeFilamentButton.pressed.connect(self.changeFilament)
            self.changeFilamentBackButton.pressed.connect(self.control)
            self.changeFilamentBackButton2.pressed.connect(self.changeFilamentCancel)
            self.changeFilamentUnloadButton.pressed.connect(lambda: self.unloadFilament())
            self.changeFilamentLoadButton.pressed.connect(lambda: self.loadFilament())
            self.loadDoneButton.pressed.connect(self.control)
            self.unloadDoneButton.pressed.connect(self.changeFilament)
            self.retractFilamentButton.pressed.connect(lambda: self.octopiclient.extrude(-20))
            self.ExtrudeButton.pressed.connect(lambda: self.octopiclient.extrude(20))
            log_info("Completed setup.")
        except Exception as e:
            error_message = f"Error in changeFilamentRoutine setup: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def unloadFilament(self):
        try:
            log_info("Executing unloadFilament.")
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
        except Exception as e:
            error_message = f"Error in unloadFilament: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def loadFilament(self):
        try:
            log_info("Executing loadFilament.")
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
        except Exception as e:
            error_message = f"Error in loadFilament: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def changeFilament(self):
        try:
            log_info("Executing changeFilament.")
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
        except Exception as e:
            error_message = f"Error in changeFilament: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def changeFilamentCancel(self):
        try:
            log_info("Executing changeFilamentCancel.")
            self.changeFilamentHeatingFlag = False
            self.coolDownAction()
            self.control()
        except Exception as e:
            error_message = f"Error in changeFilamentCancel: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
