from MainUIClass.config import *
from MainUIClass.socket_qt import *
from MainUIClass.network_utils import *

import qrcode
from PyQt5 import QtGui, QtCore, QtWidgets

from MainUIClass.buzzer_feedback import buzzer


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

