class printLocationScreen:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.printLocationScreenBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.MenuPage))
        self.MainUIObj.fromLocalButton.pressed.connect(self.MainUIObj.getFilesAndInfoInstance.fileListLocal)
        self.MainUIObj.fromUsbButton.pressed.connect(self.MainUIObj.getFilesAndInfoInstance.fileListUSB)
