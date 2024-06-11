import os
import re
import subprocess
from dialog import WarningOk

class displaySettings:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        # Display settings
        self.MainUIObj.rotateDisplay.pressed.connect(self.showRotateDisplaySettingsPage)
        self.MainUIObj.calibrateTouch.pressed.connect(self.touchCalibration)
        self.MainUIObj.displaySettingsBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.settingsPage))

        # Rotate Display Settings
        self.MainUIObj.rotateDisplaySettingsDoneButton.pressed.connect(self.saveRotateDisplaySettings)
        self.MainUIObj.rotateDisplaySettingsCancelButton.pressed.connect(
            lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.displaySettingsPage))

    def touchCalibration(self):
        os.system('sudo /home/pi/setenv.sh')

    def showRotateDisplaySettingsPage(self):
        txt = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

        reRot = r"dtoverlay\s*=\s*waveshare35a(\s*:\s*rotate\s*=\s*([0-9]{1,3})){0,1}"
        mtRot = re.search(reRot, txt)
        # print(mtRot.group(0))

        if mtRot and len(mtRot.groups()) == 2 and str(mtRot.group(2)) == "270":
            self.MainUIObj.rotateDisplaySettingsComboBox.setCurrentIndex(1)
        else:
            self.MainUIObj.rotateDisplaySettingsComboBox.setCurrentIndex(0)

        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.rotateDisplaySettingsPage)

    # def saveRotateDisplaySettings(self):
    #     txt1 = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

    #     reRot = r"dtoverlay\s*=\s*waveshare35a(\s*:\s*rotate\s*=\s*([0-9]{1,3})){0,1}"
    #     if self.MainUIObj.rotateDisplaySettingsComboBox.currentIndex() == 1:
    #         op1 = "dtoverlay=waveshare35a,rotate=270,fps=12,speed=16000000"
    #     else:
    #         op1 = "dtoverlay=waveshare35a,fps=12,speed=16000000"
    #     res1 = re.sub(reRot, op1, txt1)

    #     try:
    #         with open("/boot/config.txt", "w") as file1:
    #             file1.write(res1)
    #     except:
    #         if WarningOk(self.MainUIObj, "Failed to change rotation settings", overlay=True):
    #             return

    #     txt2 = (subprocess.Popen("cat /usr/share/X11/xorg.conf.d/99-calibration.conf", stdout=subprocess.PIPE,
    #                             shell=True).communicate()[0]).decode("utf-8")

    #     reTouch = r"Option\s+\"Calibration\"\s+\"([\d\s-]+)\""
    #     if self.MainUIObj.rotateDisplaySettingsComboBox.currentIndex() == 1:
    #         op2 = "Option \"Calibration\"  \"3919 208 236 3913\""
    #     else:
    #         op2 = "Option \"Calibration\"  \"300 3932 3801 294\""
    #     res2 = re.sub(reTouch, op2, txt2, flags=re.I)

    #     try:
    #         with open("/usr/share/X11/xorg.conf.d/99-calibration.conf", "w") as file2:
    #             file2.write(res2)
    #     except:
    #         if WarningOk(self.MainUIObj, "Failed to change touch settings", overlay=True):
    #             return

    #     self.MainUIObj.homePageInstance.askAndReboot()
    #     self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.displaySettingsPage)

    def saveRotateDisplaySettings(self):
        txt1 = (subprocess.Popen("cat /boot/config.txt", stdout=subprocess.PIPE, shell=True).communicate()[0]).decode("utf-8")

        try:
            if self.MainUIObj.rotateDisplaySettingsComboBox.currentIndex() == 1:
                os.system('sudo cp -f config/config.txt /boot/config.txt')
            else:
                os.system('sudo cp -f config/config_rot.txt /boot/config.txt')
        except:
            if WarningOk(self.MainUIObj, "Failed to change rotation settings", overlay=True):
                return
        try:
            if self.MainUIObj.rotateDisplaySettingsComboBox.currentIndex() == 1:
                os.system('sudo cp -f config/99-calibration.conf /usr/share/X11/xorg.conf.d/99-calibration.conf')
            else:
                os.system('sudo cp -f config/99-calibration_rot.conf /usr/share/X11/xorg.conf.d/99-calibration.conf')
        except:
            if WarningOk(self.MainUIObj, "Failed to change touch settings", overlay=True):
                return

        self.MainUIObj.homePageInstance.askAndReboot()
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.displaySettingsPage)
