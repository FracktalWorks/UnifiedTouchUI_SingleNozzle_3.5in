from MainUIClass.gui_elements import ClickableLineEdit
from PyQt5 import QtCore, QtGui
from MainUIClass.config import _fromUtf8
import styles
import mainGUI
from logger import *
import dialog

class lineEdits(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting line edits init.")
        super().__init__()
    
    def setup(self, octopiclient):
        """
        Sets up various line edits for UI elements.
        """
        log_info("Setting up line edits.")
        try:
            font = QtGui.QFont()
            font.setFamily(_fromUtf8("Gotham"))
            font.setPointSize(15)

            self.wifiPasswordLineEdit = ClickableLineEdit(self.wifiSettingsPage)
            self.wifiPasswordLineEdit.setGeometry(QtCore.QRect(0, 170, 480, 60))
            self.wifiPasswordLineEdit.setFont(font)
            self.wifiPasswordLineEdit.setStyleSheet(styles.textedit)
            self.wifiPasswordLineEdit.setObjectName(_fromUtf8("wifiPasswordLineEdit"))

            font.setPointSize(11)
            self.ethStaticIpLineEdit = ClickableLineEdit(self.ethStaticSettings)
            self.ethStaticIpLineEdit.setGeometry(QtCore.QRect(120, 10, 300, 30))
            self.ethStaticIpLineEdit.setFont(font)
            self.ethStaticIpLineEdit.setStyleSheet(styles.textedit)
            self.ethStaticIpLineEdit.setObjectName(_fromUtf8("ethStaticIpLineEdit"))

            self.ethStaticGatewayLineEdit = ClickableLineEdit(self.ethStaticSettings)
            self.ethStaticGatewayLineEdit.setGeometry(QtCore.QRect(120, 60, 300, 30))
            self.ethStaticGatewayLineEdit.setFont(font)
            self.ethStaticGatewayLineEdit.setStyleSheet(styles.textedit)
            self.ethStaticGatewayLineEdit.setObjectName(_fromUtf8("ethStaticGatewayLineEdit"))

            log_info("Line edits setup completed.")
        except Exception as e:
            error_message = f"Error setting up line edits: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
