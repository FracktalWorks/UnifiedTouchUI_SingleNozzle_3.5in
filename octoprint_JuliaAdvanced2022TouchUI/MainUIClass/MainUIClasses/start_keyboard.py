import keyboard
from PyQt5 import QtCore
import dialog 
from logger import *

def startKeyboard(self, returnFn, onlyNumeric=False, noSpace=False, text=""):
    '''
    Starts the keyboard screen for entering Password
    '''
    try:
        keyBoardMainUIObj = keyboard.Keyboard(onlyNumeric=onlyNumeric, noSpace=noSpace, text=text)
        keyBoardMainUIObj.keyboard_signal.connect(returnFn)
        keyBoardMainUIObj.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        keyBoardMainUIObj.show()
    
    except Exception as e:
        error_message = f"Error starting keyboard: {str(e)}"
        log_error(error_message)
        if dialog.WarningOk(self, error_message, overlay=True):
            pass
