import mainGUI
from MainUIClass.MainUIClasses import getFilesAndInfo

class printLocationScreen(mainGUI.Ui_MainWindow):
    def __init__(self, MainUIObj):
        self.printLocationScreenBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
        self.fromLocalButton.pressed.connect(getFilesAndInfo.fileListLocal)
        self.fromUsbButton.pressed.connect(getFilesAndInfo.fileListUSB)
        super().__init__()
