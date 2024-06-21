import dialog
import mainGUI

class lockSettings(mainGUI.Ui_MainWindow):
    def __init__(self, MainUIObj):
        self.pgLock_pin.textChanged.connect(self.Lock_onPinInputChanged)

        self.pgLock_bt1.clicked.connect(lambda: self.Lock_kbAdd("1"))
        self.pgLock_bt2.clicked.connect(lambda: self.Lock_kbAdd("2"))
        self.pgLock_bt3.clicked.connect(lambda: self.Lock_kbAdd("3"))
        self.pgLock_bt4.clicked.connect(lambda: self.Lock_kbAdd("4"))
        self.pgLock_bt5.clicked.connect(lambda: self.Lock_kbAdd("5"))
        self.pgLock_bt6.clicked.connect(lambda: self.Lock_kbAdd("6"))
        self.pgLock_bt7.clicked.connect(lambda: self.Lock_kbAdd("7"))
        self.pgLock_bt8.clicked.connect(lambda: self.Lock_kbAdd("8"))
        self.pgLock_bt9.clicked.connect(lambda: self.Lock_kbAdd("9"))
        self.pgLock_bt0.clicked.connect(lambda: self.Lock_kbAdd("0"))
        self.pgLock_btBackspace.clicked.connect(lambda: self.pgLock_pin.backspace())
        self.pgLock_btSubmit.clicked.connect(self.Lock_submitPIN)
        super().__init__()

    def Lock_showLock(self):
        self.pgLock_HID.setText(str(self.__packager.hc()))
        self.pgLock_pin.setText("")
        if not self.__timelapse_enabled:
            # dialog.WarningOk(self, "Machine locked!", overlay=True)
            self.stackedWidget.setCurrentWidget(self.pgLock)
        else:
            # if self.__timelapse_started:
            #     dialog.WarningOk(self, "Demo mode!", overlay=True)
            self.stackedWidget.setCurrentWidget(self.homePage)
        
    def Lock_kbAdd(self, txt):
        if len(str(self.pgLock_pin.text())) < 9:
            self.pgLock_pin.setText(str(self.pgLock_pin.text()) + txt)
        self.pgLock_pin.setFocus()
        
    def Lock_onPinInputChanged(self):
        self.pgLock_btBackspace.setEnabled(len(str(self.pgLock_pin.text())) > 0)
        self.pgLock_btSubmit.setEnabled(len(str(self.pgLock_pin.text())) > 3)
        
    def Lock_submitPIN(self):
        k = -1
        t = self.pgLock_pin.text()
        try:
            k = int(t)
            if self.__packager.match(k):
                self.__packager.save(k)
                # self.__timelapse_enabled = True
                if dialog.SuccessOk(self, "Machine unlocked!", overlay=True):
                    self.tellAndReboot()
                self.stackedWidget.setCurrentWidget(self.homePage)
            else:
                dialog.WarningOk(self, "Incorrect unlock code")
        except Exception as e:
            dialog.WarningOk(self, "Error while parsing unlock code")
            print(e)
