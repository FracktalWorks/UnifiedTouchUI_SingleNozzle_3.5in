import dialog

class lockSettings:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):
        self.MainUIObj.pgLock_pin.textChanged.connect(self.Lock_onPinInputChanged)

        self.MainUIObj.pgLock_bt1.clicked.connect(lambda: self.Lock_kbAdd("1"))
        self.MainUIObj.pgLock_bt2.clicked.connect(lambda: self.Lock_kbAdd("2"))
        self.MainUIObj.pgLock_bt3.clicked.connect(lambda: self.Lock_kbAdd("3"))
        self.MainUIObj.pgLock_bt4.clicked.connect(lambda: self.Lock_kbAdd("4"))
        self.MainUIObj.pgLock_bt5.clicked.connect(lambda: self.Lock_kbAdd("5"))
        self.MainUIObj.pgLock_bt6.clicked.connect(lambda: self.Lock_kbAdd("6"))
        self.MainUIObj.pgLock_bt7.clicked.connect(lambda: self.Lock_kbAdd("7"))
        self.MainUIObj.pgLock_bt8.clicked.connect(lambda: self.Lock_kbAdd("8"))
        self.MainUIObj.pgLock_bt9.clicked.connect(lambda: self.Lock_kbAdd("9"))
        self.MainUIObj.pgLock_bt0.clicked.connect(lambda: self.Lock_kbAdd("0"))
        self.MainUIObj.pgLock_btBackspace.clicked.connect(lambda: self.MainUIObj.pgLock_pin.backspace())
        self.MainUIObj.pgLock_btSubmit.clicked.connect(self.Lock_submitPIN)

    def Lock_showLock(self):
        self.MainUIObj.pgLock_HID.setText(str(self.MainUIObj.__packager.hc()))
        self.MainUIObj.pgLock_pin.setText("")
        if not self.MainUIObj.__timelapse_enabled:
            # dialog.WarningOk(self, "Machine locked!", overlay=True)
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.pgLock)
        else:
            # if self.__timelapse_started:
            #     dialog.WarningOk(self, "Demo mode!", overlay=True)
            self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage)
        
    def Lock_kbAdd(self, txt):
        if len(str(self.MainUIObj.pgLock_pin.text())) < 9:
            self.MainUIObj.pgLock_pin.setText(str(self.MainUIObj.pgLock_pin.text()) + txt)
        self.MainUIObj.pgLock_pin.setFocus()
        
    def Lock_onPinInputChanged(self):
        self.MainUIObj.pgLock_btBackspace.setEnabled(len(str(self.MainUIObj.pgLock_pin.text())) > 0)
        self.MainUIObj.pgLock_btSubmit.setEnabled(len(str(self.MainUIObj.pgLock_pin.text())) > 3)
        
    def Lock_submitPIN(self):
        k = -1
        t = self.MainUIObj.pgLock_pin.text()
        try:
            k = int(t)
            if self.MainUIObj.__packager.match(k):
                self.MainUIObj.__packager.save(k)
                # self.__timelapse_enabled = True
                if dialog.SuccessOk(self.MainUIObj, "Machine unlocked!", overlay=True):
                    self.tellAndReboot()
                self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage)
            else:
                dialog.WarningOk(self.MainUIObj, "Incorrect unlock code")
        except Exception as e:
            dialog.WarningOk(self.MainUIObj, "Error while parsing unlock code")
            print(e)
