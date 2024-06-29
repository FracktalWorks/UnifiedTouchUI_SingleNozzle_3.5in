import os
import re
import subprocess
from dialog import WarningOk
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import askAndReboot
from logger import *

class displaySettings(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting display settings init.")
        super().__init__()
        
    
    def setup(self, octopiclient):
        # Display settings
        self.rotateDisplay.pressed.connect(self.showRotateDisplaySettingsPage)
        self.calibrateTouch.pressed.connect(self.touchCalibration)
        self.displaySettingsBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))

        # Rotate Display Settings
        self.rotateDisplaySettingsDoneButton.pressed.connect(self.saveRotateDisplaySettings)
        self.rotateDisplaySettingsCancelButton.pressed.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.displaySettingsPage))
        

    def touchCalibration(self):
        os.system('sudo /home/pi/setenv.sh')

    def showRotateDisplaySettingsPage(self):
        txt = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

        reRot = r"dtoverlay\s*=\s*waveshare35a(\s*:\s*rotate\s*=\s*([0-9]{1,3})){0,1}"
        mtRot = re.search(reRot, txt)
        # print(mtRot.group(0))

        if mtRot and len(mtRot.groups()) == 2 and str(mtRot.group(2)) == "270":
            self.rotateDisplaySettingsComboBox.setCurrentIndex(1)
        else:
            self.rotateDisplaySettingsComboBox.setCurrentIndex(0)

        self.stackedWidget.setCurrentWidget(self.rotateDisplaySettingsPage)

    # def saveRotateDisplaySettings(self):
    #     txt1 = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

    #     reRot = r"dtoverlay\s*=\s*waveshare35a(\s*:\s*rotate\s*=\s*([0-9]{1,3})){0,1}"
    #     if self.rotateDisplaySettingsComboBox.currentIndex() == 1:
    #         op1 = "dtoverlay=waveshare35a,rotate=270,fps=12,speed=16000000"
    #     else:
    #         op1 = "dtoverlay=waveshare35a,fps=12,speed=16000000"
    #     res1 = re.sub(reRot, op1, txt1)

    #     try:
    #         with open("/boot/config.txt", "w") as file1:
    #             file1.write(res1)
    #     except:
    #         if WarningOk(self, "Failed to change rotation settings", overlay=True):
    #             return

    #     txt2 = (subprocess.Popen("cat /usr/share/X11/xorg.conf.d/99-calibration.conf", stdout=subprocess.PIPE,
    #                             shell=True).communicate()[0]).decode("utf-8")

    #     reTouch = r"Option\s+\"Calibration\"\s+\"([\d\s-]+)\""
    #     if self.rotateDisplaySettingsComboBox.currentIndex() == 1:
    #         op2 = "Option \"Calibration\"  \"3919 208 236 3913\""
    #     else:
    #         op2 = "Option \"Calibration\"  \"300 3932 3801 294\""
    #     res2 = re.sub(reTouch, op2, txt2, flags=re.I)

    #     try:
    #         with open("/usr/share/X11/xorg.conf.d/99-calibration.conf", "w") as file2:
    #             file2.write(res2)
    #     except:
    #         if WarningOk(self, "Failed to change touch settings", overlay=True):
    #             return

    #     self.homePageInstance.askAndReboot()
    #     self.stackedWidget.setCurrentWidget(self.displaySettingsPage)

    def saveRotateDisplaySettings(self):
        txt1 = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

        try:
            if self.rotateDisplaySettingsComboBox.currentIndex() == 1:
                os.system('sudo cp -f config/config.txt /boot/config.txt')
            else:
                os.system('sudo cp -f config/config_rot.txt /boot/config.txt')
        except:
            if WarningOk(self, "Failed to change rotation settings", overlay=True):
                return
        try:
            if self.rotateDisplaySettingsComboBox.currentIndex() == 1:
                os.system('sudo cp -f config/99-calibration.conf /usr/share/X11/xorg.conf.d/99-calibration.conf')
            else:
                os.system('sudo cp -f config/99-calibration_rot.conf /usr/share/X11/xorg.conf.d/99-calibration.conf')
        except:
            if WarningOk(self, "Failed to change touch settings", overlay=True):
                return

        askAndReboot(self)
        self.stackedWidget.setCurrentWidget(self.displaySettingsPage)
