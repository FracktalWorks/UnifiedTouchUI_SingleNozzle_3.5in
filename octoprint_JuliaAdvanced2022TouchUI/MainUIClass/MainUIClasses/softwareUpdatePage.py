import mainGUI
from MainUIClass.MainUIClasses.threads import octopiclient

class softwareUpdatePage(mainGUI.Ui_MainWindow):
    def __init__(self):
        self.softwareUpdateBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.settingsPage))
        self.performUpdateButton.pressed.connect(lambda: octopiclient.performSoftwareUpdate())
        super().__init__()

