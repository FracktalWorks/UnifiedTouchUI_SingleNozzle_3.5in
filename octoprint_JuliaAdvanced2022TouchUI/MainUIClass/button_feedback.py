from PyQt5 import QtWidgets, QtGui
from MainUIClass.buzzer_feedback import buzzer

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


