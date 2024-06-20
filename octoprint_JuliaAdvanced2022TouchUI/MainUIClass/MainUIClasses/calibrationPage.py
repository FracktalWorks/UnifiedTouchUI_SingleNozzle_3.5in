from MainUIClass.config import getCalibrationPosition
from PyQt5 import QtGui

class calibrationPage:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj

    def connect(self):

        self.calibrationPosition = getCalibrationPosition(self.MainUIObj)

        self.MainUIObj.QtSocket.z_home_offset_signal.connect(self.getZHomeOffset)

        self.MainUIObj.calibrateBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.MenuPage))
        self.MainUIObj.nozzleOffsetButton.pressed.connect(self.nozzleOffset)
        # the -ve sign is such that its converted to home offset and not just distance between nozzle and bed
        # self.MainUIObj.nozzleOffsetSetButton.pressed.connect(
        #     lambda: self.setZHomeOffset(self.MainUIObj.nozzleOffsetDoubleSpinBox.value(), True))
        self.MainUIObj.nozzleOffsetBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        # Bypass calibration wizzard page for not using Klipper
        # self.MainUIObj.calibrationWizardButton.clicked.connect(
        #     lambda: self.stackedWidget.setCurrentWidget(self.MainUIObj.calibrationWizardPage))
        self.MainUIObj.calibrationWizardButton.clicked.connect(self.quickStep1)

        self.MainUIObj.calibrationWizardBackButton.clicked.connect(
            lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage))
        # required for Klipper
        # self.MainUIObj.quickCalibrationButton.clicked.connect(self.MainUIObj.quickStep6)
        # self.MainUIObj.fullCalibrationButton.clicked.connect(self.quickStep1)

        self.MainUIObj.quickStep1NextButton.clicked.connect(self.quickStep2)
        self.MainUIObj.quickStep2NextButton.clicked.connect(self.quickStep3)
        self.MainUIObj.quickStep3NextButton.clicked.connect(self.quickStep4)
        self.MainUIObj.quickStep4NextButton.clicked.connect(self.quickStep5)
        self.MainUIObj.quickStep5NextButton.clicked.connect(self.doneStep)
        # Required for Klipper
        # self.MainUIObj.quickStep5NextButton.clicked.connect(self.quickStep6)
        # self.MainUIObj.quickStep6NextButton.clicked.connect(self.doneStep)

        # self.MainUIObj.moveZPCalibrateButton.pressed.connect(lambda: octopiclient.jog(z=-0.05))
        # self.MainUIObj.moveZPCalibrateButton.pressed.connect(lambda: octopiclient.jog(z=0.05))
        self.MainUIObj.quickStep1CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep2CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep3CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep4CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.quickStep5CancelButton.pressed.connect(self.cancelStep)
        # self.MainUIObj.quickStep6CancelButton.pressed.connect(self.cancelStep)
        self.MainUIObj.nozzleOffsetSetButton.pressed.connect(
                    lambda: self.setZProbeOffset(self.MainUIObj.nozzleOffsetDoubleSpinBox.value()))
        self.MainUIObj.QtSocket.z_probing_failed_signal.connect(self.showProbingFailed)
        self.MainUIObj.QtSocket.z_probe_offset_signal.connect(self.updateEEPROMProbeOffset)


    def updateEEPROMProbeOffset(self, offset):
        '''
        Sets the spinbox value to have the value of the Z offset from the printer.
        the value is -ve so as to be more intuitive.
        :param offset:
        :return:
        '''
        self.MainUIObj.nozzleOffsetDoubleSpinBox.setValue(float(offset))


    def setZProbeOffset(self, offset):
        '''
        Sets Z Probe offset from spinbox

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''

        self.MainUIObj.octopiclient.gcode(command='M851 Z{}'.format(offset))
        self.MainUIObj.octopiclient.gcode(command='M500')


    def showProbingFailed(self):
        self.MainUIObj.homePageInstance.tellAndReboot("Bed position is not calibrated. Please run calibration wizard after restart.")

    def getZHomeOffset(self, offset):
        '''
        Sets the spinbox value to have the value of the Z offset from the printer.
        the value is -ve so as to be more intuitive.
        :param offset:
        :return:
        '''
        self.MainUIObj.nozzleOffsetDoubleSpinBox.setValue(-float(offset))
        self.MainUIObj.nozzleHomeOffset = offset

    def setZHomeOffset(self, offset, setOffset=False):
        '''
        Sets the home offset after the calibration wizard is done, which is a callback to
        the response of M114 that is sent at the end of the Wizard in doneStep()
        :param offset: the value off the offset to set. is a str is coming from M114, and is float if coming from the nozzleOffsetPage
        :param setOffset: Boolean, is true if the function call is from the nozzleOffsetPage, else the current Z value sets the offset
        :return:

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''

        if self.MainUIObj.setHomeOffsetBool:
            self.MainUIObj.octopiclient.gcode(command='M206 Z{}'.format(-float(offset)))
            self.MainUIObj.setHomeOffsetBool = False
            self.MainUIObj.octopiclient.gcode(command='M500')
            # save in EEPROM
        if setOffset:    # When the offset needs to be set from spinbox value
            self.MainUIObj.octopiclient.gcode(command='M206 Z{}'.format(-offset))
            self.MainUIObj.octopiclient.gcode(command='M500')

    def nozzleOffset(self):
        '''
        Updates the value of M206 Z in the nozzle offset spinbox. Sends M503 so that the pritner returns the value as a websocket calback
        :return:
        '''
        self.MainUIObj.octopiclient.gcode(command='M503')
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.nozzleOffsetPage)

    def quickStep1(self):
        '''
        Shows welcome message.
        Sets Z Home Offset = 0
        Homes to MAX
        goes to position where leveling screws can be opened
        :return:
        '''

        self.MainUIObj.octopiclient.gcode(command='M503')
        self.MainUIObj.octopiclient.gcode(command='M420 S0')
        self.MainUIObj.octopiclient.gcode(command='M206 Z0')
        self.MainUIObj.octopiclient.home(['x', 'y', 'z'])
        self.MainUIObj.octopiclient.jog(x=100, y=100, z=15, absolute=True, speed=1500)
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep1Page)

    def quickStep2(self):
        '''
        Askes user to release all Leveling Screws
        :return:
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep2Page)
        if self.MainUIObj.printerName != "Julia Pro Single Nozzle":
            self.MainUIObj.movie1 = QtGui.QMovie("templates/img/calibration/calib1.gif")
            self.MainUIObj.calib1.setMovie(self.MainUIObj.movie1)
            self.MainUIObj.movie1.start()

    def quickStep3(self):
        '''
        leveks first position
        :return:
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep3Page)
        self.MainUIObj.octopiclient.jog(x=self.calibrationPosition['X1'], y=self.calibrationPosition['Y1'], absolute=True, speed=9000)
        self.MainUIObj.octopiclient.jog(z=0, absolute=True, speed=1500)
        if self.MainUIObj.printerName != "Julia Pro Single Nozzle":
            self.MainUIObj.movie1.stop()
            self.MainUIObj.movie2 = QtGui.QMovie("templates/img/calibration/calib2.gif")
            self.MainUIObj.calib2.setMovie(self.MainUIObj.movie2)
            self.MainUIObj.movie2.start()

    def quickStep4(self):
        '''
        levels second leveling position
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep4Page)
        self.MainUIObj.octopiclient.jog(z=10, absolute=True, speed=1500)
        self.MainUIObj.octopiclient.jog(x=self.calibrationPosition['X2'], y=self.calibrationPosition['Y2'], absolute=True, speed=9000)
        self.MainUIObj.octopiclient.jog(z=0, absolute=True, speed=1500)
        if self.MainUIObj.printerName != "Julia Pro Single Nozzle":
            self.MainUIObj.movie2.stop()
            self.MainUIObj.movie3 = QtGui.QMovie("templates/img/calibration/calib3.gif")
            self.MainUIObj.calib3.setMovie(self.MainUIObj.movie3)
            self.MainUIObj.movie3.start()

    def quickStep5(self):
        '''
        levels third leveling position
        :return:
        '''
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep5Page)
        self.MainUIObj.octopiclient.jog(z=10, absolute=True, speed=1500)
        self.MainUIObj.octopiclient.jog(x=self.calibrationPosition['X3'], y=self.calibrationPosition['Y3'], absolute=True, speed=9000)
        self.MainUIObj.octopiclient.jog(z=0, absolute=True, speed=1500)
        if self.MainUIObj.printerName != "Julia Pro Single Nozzle":
            self.MainUIObj.movie3.stop()
            self.MainUIObj.movie4 = QtGui.QMovie("templates/img/calibration/calib4.gif")
            self.MainUIObj.calib4.setMovie(self.MainUIObj.movie4)
            self.MainUIObj.movie4.start()

    # def quickStep6(self):
    #     '''
    #     Performs Auto bed Leveiling, required for Klipper
    #     '''
    #     self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.quickStep6Page)
    #     octopiclient.gcode(command='M190 S70')
    #     octopiclient.gcode(command='G29')

    def doneStep(self):
        '''
        decides weather to go to full calibration of return to calibration screen
        :return:
        '''

        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage)
        self.MainUIObj.movie4.stop()
        self.MainUIObj.octopiclient.gcode(command='M501')
        self.MainUIObj.octopiclient.home(['x', 'y', 'z'])

    def cancelStep(self):
        self.MainUIObj.octopiclient.gcode(command='M501')
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.calibratePage)
        try:
            self.MainUIObj.movie1.stop()
            self.MainUIObj.movie2.stop()
            self.MainUIObj.movie3.stop()
            self.MainUIObj.movie4.stop()
        except:
            pass
