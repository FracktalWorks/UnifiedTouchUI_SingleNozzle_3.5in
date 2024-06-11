import keyboard
from PyQt5 import QtCore


def startKeyboard(self, returnFn, onlyNumeric=False, noSpace=False, text=""):
    '''
    starts the keyboard screen for entering Password
    '''
    keyBoardMainUIObj = keyboard.Keyboard(onlyNumeric=onlyNumeric, noSpace=noSpace, text=text)
    keyBoardMainUIObj.keyboard_signal.connect(returnFn)
    keyBoardMainUIObj.setWindowFlags(QtCore.Qt.FramelessWindowHint)
    keyBoardMainUIObj.show()
