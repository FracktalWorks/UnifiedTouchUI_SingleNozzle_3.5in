from MainUIClass.config import *
from MainUIClass.socket_qt import *
from MainUIClass.network_utils import *
import time
import qrcode
from PyQt5 import QtGui, QtCore, QtWidgets

if not Development:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)  # Use the board numbering scheme
    GPIO.setwarnings(False)  # Disable GPIO warnings H


class BuzzerFeedback(object):
    def __init__(self, buzzerPin):
        if not Development:
            GPIO.cleanup()
            self.buzzerPin = buzzerPin
            GPIO.setup(self.buzzerPin, GPIO.OUT)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        pass

    @run_async
    def buzz(self):
        if not Development:
            GPIO.output(self.buzzerPin, (GPIO.HIGH))
            time.sleep(0.005)
            GPIO.output(self.buzzerPin, GPIO.LOW)
        pass

buzzer = BuzzerFeedback(12)

'''
To get the buzzer to beep on button press
'''

OriginalPushButton = QtGui.QPushButton
OriginalToolButton = QtGui.QToolButton


class QPushButtonFeedback(QtWidgets.QPushButton):
    def mousePressEvent(self, QMouseEvent):
        buzzer.buzz()
        OriginalPushButton.mousePressEvent(self, QMouseEvent)


class QToolButtonFeedback(QtWidgets.QToolButton):
    def mousePressEvent(self, QMouseEvent):
        buzzer.buzz()
        OriginalToolButton.mousePressEvent(self, QMouseEvent)


QtWidgets.QToolButton = QToolButtonFeedback
QtWidgets.QPushButton = QPushButtonFeedback

class Image(qrcode.image.base.BaseImage):
    def __init__(self, border, width, box_size):
        self.border = border
        self.width = width
        self.box_size = box_size
        size = (width + border * 2) * box_size
        self._image = QtGui.QImage(
            size, size, QtGui.QImage.Format_RGB16)
        self._image.fill(QtCore.Qt.white)

    def pixmap(self):
        return QtGui.QPixmap.fromImage(self._image)

    def drawrect(self, row, col):
        painter = QtGui.QPainter(self._image)
        painter.fillRect(
            (col + self.border) * self.box_size,
            (row + self.border) * self.box_size,
            self.box_size, self.box_size,
            QtCore.Qt.black)

    def save(self, stream, kind=None):
        pass

class ClickableLineEdit(QtWidgets.QLineEdit):
    clicked_signal = QtCore.pyqtSignal()
    def __init__(self, parent):
        QtWidgets.QLineEdit.__init__(self, parent)
    def mousePressEvent(self, QMouseEvent):
        buzzer.buzz()
        self.clicked_signal.emit()

