from MainUIClass.config import getCalibrationPosition
from PyQt5 import QtGui
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import tellAndReboot
from MainUIClass.MainUIClasses.printerName import printerName
from logger import *
import dialog

class calibrationPage(mainGUI.Ui_MainWindow):
    def __init__(self):
        try:
            log_info("Starting calibration init.")
            self.octopiclient = None
            super().__init__()
            log_info("Completed calibration init.")
        except Exception as e:
            error_message = f"Error in calibrationPage __init__: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def setup(self, octopiclient):
        try:
            log_info("Starting setup.")
            # self.octopiclient = octopiclient

            log_debug("Octopiclient inside class calibrationPage: " + str(self.octopiclient))

            self.printerName = printerName.getPrinterName()
            
            self.calibrationPosition = getCalibrationPosition(self)
            self.calibrateBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.MenuPage))
            self.nozzleOffsetButton.pressed.connect(self.nozzleOffset)
            # the -ve sign is such that its converted to home offset and not just distance between nozzle and bed
            # self.nozzleOffsetSetButton.pressed.connect(
            #     lambda: self.setZHomeOffset(self.nozzleOffsetDoubleSpinBox.value(), True))
            self.nozzleOffsetBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.calibratePage))
            # Bypass calibration wizzard page for not using Klipper
            # self.calibrationWizardButton.clicked.connect(
            #     lambda: self.stackedWidget.setCurrentWidget(self.calibrationWizardPage))
            self.calibrationWizardButton.clicked.connect(self.quickStep1)

            self.calibrationWizardBackButton.clicked.connect(
                lambda: self.stackedWidget.setCurrentWidget(self.calibratePage))
            # required for Klipper
            # self.quickCalibrationButton.clicked.connect(self.quickStep6)
            # self.fullCalibrationButton.clicked.connect(self.quickStep1)

            self.quickStep1NextButton.clicked.connect(self.quickStep2)
            self.quickStep2NextButton.clicked.connect(self.quickStep3)
            self.quickStep3NextButton.clicked.connect(self.quickStep4)
            self.quickStep4NextButton.clicked.connect(self.quickStep5)
            self.quickStep5NextButton.clicked.connect(self.doneStep)
            # Required for Klipper
            # self.quickStep5NextButton.clicked.connect(self.quickStep6)
            # self.quickStep6NextButton.clicked.connect(self.doneStep)

            # self.moveZPCalibrateButton.pressed.connect(lambda: self.octopiclient.jog(z=-0.05))
            # self.moveZPCalibrateButton.pressed.connect(lambda: self.octopiclient.jog(z=0.05))
            self.quickStep1CancelButton.pressed.connect(self.cancelStep)
            self.quickStep2CancelButton.pressed.connect(self.cancelStep)
            self.quickStep3CancelButton.pressed.connect(self.cancelStep)
            self.quickStep4CancelButton.pressed.connect(self.cancelStep)
            self.quickStep5CancelButton.pressed.connect(self.cancelStep)
            # self.quickStep6CancelButton.pressed.connect(self.cancelStep)
            self.nozzleOffsetSetButton.pressed.connect(
                lambda: self.setZProbeOffset(self.nozzleOffsetDoubleSpinBox.value()))
            log_info("Completed setup.")
        except Exception as e:
            error_message = f"Error in calibrationPage setup: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def setZProbeOffset(self, offset):
        try:
            log_info(f"Setting Z Probe offset to {offset}.")
            self.octopiclient.gcode(command='M851 Z{}'.format(offset))
            self.octopiclient.gcode(command='M500')
        except Exception as e:
            error_message = f"Error in setZProbeOffset: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def setZHomeOffset(self, offset, setOffset=False):
        try:
            log_info(f"Setting Z Home offset to {offset}, setOffset={setOffset}.")
            if self.setHomeOffsetBool:
                self.octopiclient.gcode(command='M206 Z{}'.format(-float(offset)))
                self.setHomeOffsetBool = False
                self.octopiclient.gcode(command='M500')
            if setOffset:
                self.octopiclient.gcode(command='M206 Z{}'.format(-offset))
                self.octopiclient.gcode(command='M500')
        except Exception as e:
            error_message = f"Error in setZHomeOffset: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def nozzleOffset(self):
        try:
            log_info("Updating nozzle offset.")
            self.octopiclient.gcode(command='M503')
            self.stackedWidget.setCurrentWidget(self.nozzleOffsetPage)
        except Exception as e:
            error_message = f"Error in nozzleOffset: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def quickStep1(self):
        try:
            log_info("Executing quickStep1.")
            self.octopiclient.gcode(command='M503')
            self.octopiclient.gcode(command='M420 S0')
            self.octopiclient.gcode(command='M206 Z0')
            self.octopiclient.home(['x', 'y', 'z'])
            self.octopiclient.jog(x=100, y=100, z=15, absolute=True, speed=1500)
            self.stackedWidget.setCurrentWidget(self.quickStep1Page)
        except Exception as e:
            error_message = f"Error in quickStep1: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def quickStep2(self):
        try:
            log_info("Executing quickStep2.")
            self.stackedWidget.setCurrentWidget(self.quickStep2Page)
            if self.printerName != "Julia Pro Single Nozzle":
                self.movie1 = QtGui.QMovie("templates/img/calibration/calib1.gif")
                self.calib1.setMovie(self.movie1)
                self.movie1.start()
        except Exception as e:
            error_message = f"Error in quickStep2: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def quickStep3(self):
        try:
            log_info("Executing quickStep3.")
            self.stackedWidget.setCurrentWidget(self.quickStep3Page)
            self.octopiclient.jog(x=self.calibrationPosition['X1'], y=self.calibrationPosition['Y1'], absolute=True, speed=9000)
            self.octopiclient.jog(z=0, absolute=True, speed=1500)
            if self.printerName != "Julia Pro Single Nozzle":
                self.movie1.stop()
                self.movie2 = QtGui.QMovie("templates/img/calibration/calib2.gif")
                self.calib2.setMovie(self.movie2)
                self.movie2.start()
        except Exception as e:
            error_message = f"Error in quickStep3: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def quickStep4(self):
        try:
            log_info("Executing quickStep4.")
            self.stackedWidget.setCurrentWidget(self.quickStep4Page)
            self.octopiclient.jog(z=10, absolute=True, speed=1500)
            self.octopiclient.jog(x=self.calibrationPosition['X2'], y=self.calibrationPosition['Y2'], absolute=True, speed=9000)
            self.octopiclient.jog(z=0, absolute=True, speed=1500)
            if self.printerName != "Julia Pro Single Nozzle":
                self.movie2.stop()
                self.movie3 = QtGui.QMovie("templates/img/calibration/calib3.gif")
                self.calib3.setMovie(self.movie3)
                self.movie3.start()
        except Exception as e:
            error_message = f"Error in quickStep4: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def quickStep5(self):
        try:
            log_info("Executing quickStep5.")
            self.stackedWidget.setCurrentWidget(self.quickStep5Page)
            self.octopiclient.jog(z=10, absolute=True, speed=1500)
            self.octopiclient.jog(x=self.calibrationPosition['X3'], y=self.calibrationPosition['Y3'], absolute=True, speed=9000)
            self.octopiclient.jog(z=0, absolute=True, speed=1500)
            if self.printerName != "Julia Pro Single Nozzle":
                self.movie3.stop()
                self.movie4 = QtGui.QMovie("templates/img/calibration/calib4.gif")
                self.calib4.setMovie(self.movie4)
                self.movie4.start()
        except Exception as e:
            error_message = f"Error in quickStep5: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    # def quickStep6(self):
    #     '''
    #     Performs Auto bed Leveiling, required for Klipper
    #     '''
    #     self.stackedWidget.setCurrentWidget(self.quickStep6Page)
    #     self.octopiclient.gcode(command='M190 S70')
    #     self.octopiclient.gcode(command='G29')

    def doneStep(self):
        try:
            log_info("Executing doneStep.")
            self.stackedWidget.setCurrentWidget(self.calibratePage)
            self.movie4.stop()
            self.octopiclient.gcode(command='M501')
            self.octopiclient.home(['x', 'y', 'z'])
        except Exception as e:
            error_message = f"Error in doneStep: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass

    def cancelStep(self):
        try:
            log_info("Executing cancelStep.")
            self.octopiclient.gcode(command='M501')
            self.stackedWidget.setCurrentWidget(self.calibratePage)
            try:
                self.movie1.stop()
                self.movie2.stop()
                self.movie3.stop()
                self.movie4.stop()
            except:
                pass
        except Exception as e:
            error_message = f"Error in cancelStep: {str(e)}"
            log_error(error_message)
            if dialog.WarningOk(self, error_message, overlay=True):
                pass
