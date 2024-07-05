from MainUIClass.config import *
from MainUIClass.socket_qt import *
from MainUIClass.network_utils import *
import time
import qrcode
from PyQt5 import QtGui, QtCore, QtWidgets
import dialog
from logger import log_info, log_error  # Assuming these are your user-defined log functions

if not Development:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  # Use the board numbering scheme
    GPIO.setwarnings(False)  # Disable GPIO warnings

class BuzzerFeedback(object):
    def __init__(self, buzzerPin):
        try:
            if not Development:
                GPIO.cleanup()
                self.buzzerPin = buzzerPin
                GPIO.setup(self.buzzerPin, GPIO.OUT)
                GPIO.output(self.buzzerPin, GPIO.LOW)
        except Exception as e:
            log_error(f"Error initializing BuzzerFeedback: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

    @run_async
    def buzz(self):
        try:
            if not Development:
                GPIO.output(self.buzzerPin, GPIO.HIGH)
                time.sleep(0.005)
                GPIO.output(self.buzzerPin, GPIO.LOW)
        except Exception as e:
            log_error(f"Error in buzz: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

buzzer = BuzzerFeedback(12)

'''
To get the buzzer to beep on button press
'''

OriginalPushButton = QtWidgets.QPushButton
OriginalToolButton = QtWidgets.QToolButton

class QPushButtonFeedback(QtWidgets.QPushButton):
    def mousePressEvent(self, QMouseEvent):
        try:
            buzzer.buzz()
            OriginalPushButton.mousePressEvent(self, QMouseEvent)
        except Exception as e:
            log_error(f"Error in QPushButtonFeedback mousePressEvent: {str(e)}")
            if dialog.WarningOk(self, str(e), overlay=True):
                pass

class QToolButtonFeedback(QtWidgets.QToolButton):
    def mousePressEvent(self, QMouseEvent):
        try:
            buzzer.buzz()
            OriginalToolButton.mousePressEvent(self, QMouseEvent)
        except Exception as e:
            log_error(f"Error in QToolButtonFeedback mousePressEvent: {str(e)}")
            if dialog.WarningOk(self, str(e), overlay=True):
                pass

QtWidgets.QToolButton = QToolButtonFeedback
QtWidgets.QPushButton = QPushButtonFeedback

class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        try:
            self.border = border
            self.width = width
            self.box_size = box_size
            size = (width + border * 2) * box_size
            self._image = QtGui.QImage(size, size, QtGui.QImage.Format_RGB16)
            self._image.fill(QtCore.Qt.white)
        except Exception as e:
            log_error(f"Error initializing Image: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

    def pixmap(self):
        try:
            return QtGui.QPixmap.fromImage(self._image)
        except Exception as e:
            log_error(f"Error in Image pixmap: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

    def drawrect(self, row, col):
        try:
            painter = QtGui.QPainter(self._image)
            painter.fillRect((col + self.border) * self.box_size,
                             (row + self.border) * self.box_size,
                             self.box_size, self.box_size, QtCore.Qt.black)
        except Exception as e:
            log_error(f"Error in Image drawrect: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

    def save(self, stream, kind=None):
        try:
            pass
        except Exception as e:
            log_error(f"Error in Image save: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked_signal = QtCore.pyqtSignal()

    def __init__(self, parent):
        try:
            QtWidgets.QLineEdit.__init__(self, parent)
        except Exception as e:
            log_error(f"Error initializing ClickableLineEdit: {str(e)}")
            if dialog.WarningOk(None, str(e), overlay=True):
                pass

    def mousePressEvent(self, QMouseEvent):
        try:
            buzzer.buzz()
            self.clicked_signal.emit()
        except Exception as e:
            log_error(f"Error in ClickableLineEdit mousePressEvent: {str(e)}")
            if dialog.WarningOk(self, str(e), overlay=True):
                pass
