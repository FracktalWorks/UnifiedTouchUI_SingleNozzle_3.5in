import os
import re
import subprocess
from dialog import WarningOk
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import askAndReboot
from logger import *

class displaySettings(mainGUI.Ui_MainWindow):
    def __init__(self):
        '''
        Constructor for the displaySettings class.
        '''
        try:
            log_info("Starting display settings init.")
            super().__init__()
            log_info("Completed display settings init.")
        except Exception as e:
            error_message = f"Error in displaySettings __init__: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass
    
    def setup(self, octopiclient):
        '''
        Sets up the display settings UI and connects buttons.
        
        Parameters:
        - octopiclient: The OctoPrint client instance.
        '''
        try:
            log_info("Starting setup.")
            # Display settings
            self.rotateDisplay.pressed.connect(self.showRotateDisplaySettingsPage)
            self.calibrateTouch.pressed.connect(self.touchCalibration)
            self.displaySettingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

            # Rotate Display Settings
            self.rotateDisplaySettingsDoneButton.pressed.connect(self.saveRotateDisplaySettings)
            self.rotateDisplaySettingsCancelButton.pressed.connect(
                lambda: self.stackedWidget.setCurrentWidget(self.displaySettingsPage))
            log_info("Completed setup.")
        except Exception as e:
            error_message = f"Error in displaySettings setup: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass

    def touchCalibration(self):
        '''
        Executes touch calibration by running a shell script.
        '''
        try:
            log_info("Executing touch calibration.")
            os.system('sudo /home/pi/setenv.sh')
        except Exception as e:
            error_message = f"Error in touchCalibration: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass

    def showRotateDisplaySettingsPage(self):
        '''
        Shows the rotate display settings page and adjusts UI based on current settings.
        '''
        try:
            log_info("Showing rotate display settings page.")
            txt = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

            reRot = r"dtoverlay\s*=\s*waveshare35a(\s*:\s*rotate\s*=\s*([0-9]{1,3})){0,1}"
            mtRot = re.search(reRot, txt)

            if mtRot and len(mtRot.groups()) == 2 and str(mtRot.group(2)) == "270":
                self.rotateDisplaySettingsComboBox.setCurrentIndex(1)
            else:
                self.rotateDisplaySettingsComboBox.setCurrentIndex(0)

            self.stackedWidget.setCurrentWidget(self.rotateDisplaySettingsPage)
        except Exception as e:
            error_message = f"Error in showRotateDisplaySettingsPage: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass

    def saveRotateDisplaySettings(self):
        '''
        Saves rotate display settings by modifying configuration files and optionally reboots the system.
        '''
        try:
            log_info("Saving rotate display settings.")
            txt1 = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

            if self.rotateDisplaySettingsComboBox.currentIndex() == 1:
                os.system('sudo cp -f config/config.txt /boot/config.txt')
            else:
                os.system('sudo cp -f config/config_rot.txt /boot/config.txt')

            if self.rotateDisplaySettingsComboBox.currentIndex() == 1:
                os.system('sudo cp -f config/99-calibration.conf /usr/share/X11/xorg.conf.d/99-calibration.conf')
            else:
                os.system('sudo cp -f config/99-calibration_rot.conf /usr/share/X11/xorg.conf.d/99-calibration.conf')

            askAndReboot(self)
            self.stackedWidget.setCurrentWidget(self.displaySettingsPage)
        except Exception as e:
            error_message = f"Error in saveRotateDisplaySettings: {str(e)}"
            log_error(error_message)
            if WarningOk(self, error_message, overlay=True):
                pass
