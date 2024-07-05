import sys
from MainUIClass.MainUIClass_def import MainUIClass
from PyQt5 import QtWidgets
from logger import *

# from MainUIClass.config import Development
# if not Development:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)  # Use the board numbering scheme
#     GPIO.setwarnings(False)  # Disable GPIO warnings 

if __name__ == '__main__':
    start_logger('Application started')
    try:
        app = QtWidgets.QApplication(sys.argv)
        log_debug('QApplication created')
        
        # Initialize the library (must be called once before other functions).
        # Creates an object of type MainUIClass
        log_info('Creating MainUI Object instance')
        MainWindow = MainUIClass()
        log_debug('MainUIClass instance created')
        
        MainWindow.show()
        log_info('Main window shown')
        
        # MainWindow.showFullScreen()
        # MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # Create NeoPixel object with appropriate configuration.
        # charm = FlickCharm()
        # charm.activateOn(MainWindow.FileListWidget)
        
        log_info('Application exited cleanly')
    except Exception as e:
        log_error(f'Application encountered an error: {e}')
sys.exit(app.exec_())

