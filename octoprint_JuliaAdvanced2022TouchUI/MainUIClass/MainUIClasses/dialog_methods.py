import dialog
import os

def tellAndReboot(self, msg="Rebooting...", overlay=True):
    if dialog.WarningOk(self, msg, overlay=overlay):
        os.system('sudo reboot now')
        return True
    return False

def askAndReboot(self, msg="Are you sure you want to reboot?", overlay=True):
    if dialog.WarningYesNo(self, msg, overlay=overlay):
        os.system('sudo reboot now')
        return True
    return False
