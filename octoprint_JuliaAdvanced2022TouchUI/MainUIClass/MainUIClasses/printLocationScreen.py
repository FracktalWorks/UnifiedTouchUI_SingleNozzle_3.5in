import mainGUI
from MainUIClass.MainUIClasses import getFilesAndInfo
from logger import *

class printLocationScreen(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting print location screen init.")
        super().__init__()

    def setup(self):
        self.printLocationScreenBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.fromLocalButton.pressed.connect(getFilesAndInfo.fileListLocal)
        self.fromUsbButton.pressed.connect(getFilesAndInfo.fileListUSB)
        
