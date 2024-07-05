import dialog
import mainGUI
from logger import *

class lockSettings(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting lock settings init.")
        super().__init__()
    
    def setup(self, octopiclient):
        """
        Sets up signal connections for lock settings UI elements.
        """
        log_info("Setting up lock settings.")
        try:
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
            
            log_info("Lock settings setup completed.")
        except Exception as e:
            error_message = f"Error setting up lock settings: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def Lock_showLock(self):
        """
        Displays the lock screen and clears PIN input.
        """
        try:
            self.pgLock_HID.setText(str(self.__packager.hc()))
            self.pgLock_pin.setText("")
            if not self.__timelapse_enabled:
                self.stackedWidget.setCurrentWidget(self.pgLock)
            else:
                self.stackedWidget.setCurrentWidget(self.homePage)
        except Exception as e:
            error_message = f"Error showing lock screen: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
        
    def Lock_kbAdd(self, txt):
        """
        Adds text to the PIN input field.
        """
        try:
            if len(str(self.pgLock_pin.text())) < 9:
                self.pgLock_pin.setText(str(self.pgLock_pin.text()) + txt)
            self.pgLock_pin.setFocus()
        except Exception as e:
            error_message = f"Error adding text to PIN input: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
        
    def Lock_onPinInputChanged(self):
        """
        Enables or disables backspace and submit buttons based on PIN input length.
        """
        try:
            self.pgLock_btBackspace.setEnabled(len(str(self.pgLock_pin.text())) > 0)
            self.pgLock_btSubmit.setEnabled(len(str(self.pgLock_pin.text())) > 3)
        except Exception as e:
            error_message = f"Error handling PIN input change: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
        
    def Lock_submitPIN(self):
        """
        Submits the entered PIN for verification and unlocks the machine if correct.
        """
        try:
            k = -1
            t = self.pgLock_pin.text()
            try:
                k = int(t)
                if self.__packager.match(k):
                    self.__packager.save(k)
                    if dialog.SuccessOk(self, "Machine unlocked!", overlay=True):
                        self.tellAndReboot()
                    self.stackedWidget.setCurrentWidget(self.homePage)
                else:
                    dialog.WarningOk(self, "Incorrect unlock code")
            except ValueError:
                dialog.WarningOk(self, "Invalid unlock code: Must be numeric")
        except Exception as e:
            error_message = f"Error submitting PIN: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
