from PyQt5 import QtCore, QtGui, QtWidgets
import win_keyboard
from functools import partial


class Keyboard(QtWidgets.QDialog):
    '''
    Class that sets up the win_keyboard UI and functionality
    '''

    keyboard_signal = QtCore.pyqtSignal('PyQt_PyObject')

    def __init__(self, parent=None, onlyNumeric=False, noSpace=False, text=""):
        # QtGui.QDialog.__init__(self)
        super(Keyboard, self).__init__(parent)

        self.ui = win_keyboard.Ui_WinKeyboard()
        self.ui.setupUi(self)

        self.setAlphaUpperState(False)

        self.setActions()

        self.ui.tbDisplay.setText(text)
        self.setTextFocus()

        self.ui.btBackNumeric.setEnabled(not onlyNumeric)
        self.ui.btSpecialNumeric.setEnabled(not onlyNumeric)

        self.ui.btSpaceAlpha.setEnabled(not noSpace)
        self.ui.btSpaceAlphaU.setEnabled(not noSpace)
        self.ui.btSpaceNumeric.setEnabled(not noSpace)
        self.ui.btSpaceSpecial.setEnabled(not noSpace)

        if not onlyNumeric:
            self.ShowAlpha()
        else:
            self.ShowNumeric()

    def setAlphaUpperState(self, pinned):
        self.mAlphaPinned = pinned
        self.ui.btCaseAlphaU.setChecked(pinned)
        self.ui.btCaseAlphaU.setFlat(pinned)

    def appendTextAndFocus(self, text):
        # self.ui.tbDisplay.setText(self.ui.tbDisplay.toPlainText() + arg)
        try:
            self.addText(text)
            if self.ui.pageHolder.currentWidget() == self.ui.pgAlphaU:
                if not self.mAlphaPinned:
                    self.ShowAlpha()
            self.ui.tbDisplay.setFocus()
        except Exception as e:
            print("error Pressing Button: " + str(e))
            self.ui = win_keyboard.Ui_WinKeyboard()

    def setTextFocus(self):
        self.ui.tbDisplay.moveCursor(QtGui.QTextCursor.End, QtGui.QTextCursor.MoveAnchor)
        self.ui.tbDisplay.setFocus()

    def addText(self, txt):
        cursor = self.ui.tbDisplay.textCursor()
        cursor.insertText(txt)
        self.ui.tbDisplay.setFocus()

    def connectClick(self, s):
        temp = "bt" + s
        button = getattr(self.ui, temp)
        button.clicked.connect(partial(self.appendTextAndFocus, button.text()))

    def HandleAlphaState(self):
        if not self.mAlphaPinned:
            self.setAlphaUpperState(True)
            self.setTextFocus()
        else:
            self.ShowAlpha()

    def ShowAlpha(self):
        self.setAlphaUpperState(False)
        self.ui.pageHolder.setCurrentWidget(self.ui.pgAlpha)
        self.setTextFocus()

    def ShowAlphaU(self):
        self.ui.pageHolder.setCurrentWidget(self.ui.pgAlphaU)
        self.setTextFocus()

    def ShowHome(self):
        self.ui.pageHolder.setCurrentWidget(self.ui.pgAlpha)
        self.setTextFocus()

    def ShowNumeric(self):
        self.ui.pageHolder.setCurrentWidget(self.ui.pgNumeric)
        self.setTextFocus()

    def ShowSpecial(self):
        self.ui.pageHolder.setCurrentWidget(self.ui.pgSpecial)
        self.setTextFocus()

    def Space(self):
        self.addText(" ")
        self.ui.tbDisplay.setFocus()

    def Backspace(self):
        cursor = self.ui.tbDisplay.textCursor()
        pos = cursor.position() - 1
        st = self.ui.tbDisplay.toPlainText()
        # self.ui.tbDisplay.setText(st[:-1])
        if pos >= 0:
            st = st[:pos] + st[(pos + 1):]
            self.ui.tbDisplay.setText(st)
            cursor.setPosition(pos)
            self.ui.tbDisplay.setTextCursor(cursor)
        self.ui.tbDisplay.setFocus()

    # caret
    def CaretLeft(self):
        self.ui.tbDisplay.moveCursor(QtGui.QTextCursor.Left, QtGui.QTextCursor.MoveAnchor)
        self.ui.tbDisplay.setFocus()

    def CaretRight(self):
        self.ui.tbDisplay.moveCursor(QtGui.QTextCursor.Right, QtGui.QTextCursor.MoveAnchor)
        self.ui.tbDisplay.setFocus()

    def CaretStart(self):
        self.ui.tbDisplay.moveCursor(QtGui.QTextCursor.Start, QtGui.QTextCursor.MoveAnchor)
        self.ui.tbDisplay.setFocus()

    def CaretEnd(self):
        self.setTextFocus()

    def setActions(self):
        # Screens
        # Char cases
        self.ui.btCaseAlphaU.clicked.connect(self.HandleAlphaState)
        self.ui.btCaseAlpha.clicked.connect(self.ShowAlphaU)
        # Show Numeric
        self.ui.btNumericAlpha.clicked.connect(self.ShowNumeric)
        self.ui.btNumericAlphaU.clicked.connect(self.ShowNumeric)
        self.ui.btNumericSpecial.clicked.connect(self.ShowNumeric)
        # ShowSpecial
        self.ui.btSpecialAlpha.clicked.connect(self.ShowSpecial)
        self.ui.btSpecialAlphaU.clicked.connect(self.ShowSpecial)
        self.ui.btSpecialNumeric.clicked.connect(self.ShowSpecial)

        # Cursor
        self.ui.btCursorLeft.clicked.connect(self.CaretLeft)
        self.ui.btCursorRight.clicked.connect(self.CaretRight)

        # ASCII
        for i in range(1, 95):
            self.connectClick(str(i))
        # repeated elements
        rep = ["27_2", "56_2", "69_2", "74_2", "79_2", "27_3", "56_3"]
        for i in rep:
            self.connectClick(i)

        # Space
        self.ui.btSpaceAlpha.clicked.connect(self.Space)
        self.ui.btSpaceAlphaU.clicked.connect(self.Space)
        self.ui.btSpaceNumeric.clicked.connect(self.Space)
        self.ui.btSpaceSpecial.clicked.connect(self.Space)

        # Backspace
        self.ui.btBackspaceAlpha.clicked.connect(self.Backspace)
        self.ui.btBackspaceAlphaU.clicked.connect(self.Backspace)
        self.ui.btBackspaceNumeric.clicked.connect(self.Backspace)
        self.ui.btBackspaceSpecial.clicked.connect(self.Backspace)

        # Submit
        self.ui.btSubmitAlpha.clicked.connect(self.submit)
        self.ui.btSubmitAlphaU.clicked.connect(self.submit)
        self.ui.btSubmitNumeric.clicked.connect(self.submit)
        self.ui.btSubmitSpecial.clicked.connect(self.submit)

        # Back
        self.ui.btBackNumeric.clicked.connect(self.ShowHome)
        self.ui.btBackSpecial.clicked.connect(self.ShowHome)

    # Submit
    def submit(self):
        self.close()
        self.keyboard_signal.emit(self.ui.tbDisplay.toPlainText())
        self.ui.tbDisplay.setText("")
