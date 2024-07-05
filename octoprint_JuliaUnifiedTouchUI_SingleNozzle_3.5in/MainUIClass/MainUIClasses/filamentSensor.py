import requests
from MainUIClass.config import apiKey, ip
from PyQt5 import QtGui
import mainGUI
from logger import *
from dialog import WarningOk

class filamentSensor(mainGUI.Ui_MainWindow):
    def __init__(self):
        '''
        Constructor for the filamentSensor class.
        '''
        try:
            log_info("Starting filament sensor init.")
            super().__init__()
            log_info("Completed filament sensor init.")
        except Exception as e:
            error_message = f"Error in filamentSensor __init__: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass

    def setup(self, octopiclient):
        '''
        Sets up the filament sensor UI and connects button signals.
        
        Parameters:
        - octopiclient: The OctoPrint client instance.
        '''
        try:
            log_info("Starting setup.")
            self.toggleFilamentSensorButton.clicked.connect(self.toggleFilamentSensor)
            log_info("Completed setup.")
        except Exception as e:
            error_message = f"Error in filamentSensor setup: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass

    def isFilamentSensorInstalled(self):
        '''
        Checks if the filament sensor plugin is installed and sets button state accordingly.
        
        Returns:
        - bool: True if filament sensor is installed and connection successful, False otherwise.
        '''
        success = False
        try:
            headers = {'X-Api-Key': apiKey}
            req = requests.get(f'http://{ip}/plugin/Julia2018FilamentSensor/status', headers=headers)
            success = req.status_code == requests.codes.ok
        except Exception as e:
            error_message = f"Error in isFilamentSensorInstalled: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass
        self.toggleFilamentSensorButton.setEnabled(success)
        return success

    def toggleFilamentSensor(self):
        '''
        Toggles the filament sensor state using a HTTP GET request to the plugin endpoint.
        '''
        try:
            headers = {'X-Api-Key': apiKey}
            requests.get(f'http://{ip}/plugin/Julia2018FilamentSensor/toggle', headers=headers)
        except Exception as e:
            error_message = f"Error in toggleFilamentSensor: {str(e)}"
            log_error(error_message)
            if WarningOk(self, "Failed to toggle filament sensor", overlay=True):
                pass
