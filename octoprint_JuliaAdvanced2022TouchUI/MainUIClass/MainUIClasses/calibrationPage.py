from MainUIClass.config import getCalibrationPosition
from PyQt5 import QtGui
import mainGUI
from MainUIClass.MainUIClasses.dialog_methods import tellAndReboot
from MainUIClass.MainUIClasses.threads import octopiclient
from MainUIClass.MainUIClasses import printerName

class calibrationPage(mainGUI.Ui_MainWindow):
    def __init__(self):
        self.printerName = printerName.getPrinterName(self)
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

        # self.moveZPCalibrateButton.pressed.connect(lambda: octopiclient.jog(z=-0.05))
        # self.moveZPCalibrateButton.pressed.connect(lambda: octopiclient.jog(z=0.05))
        self.quickStep1CancelButton.pressed.connect(self.cancelStep)
        self.quickStep2CancelButton.pressed.connect(self.cancelStep)
        self.quickStep3CancelButton.pressed.connect(self.cancelStep)
        self.quickStep4CancelButton.pressed.connect(self.cancelStep)
        self.quickStep5CancelButton.pressed.connect(self.cancelStep)
        # self.quickStep6CancelButton.pressed.connect(self.cancelStep)
        self.nozzleOffsetSetButton.pressed.connect(
                    lambda: self.setZProbeOffset(self.nozzleOffsetDoubleSpinBox.value()))
        super().__init__()

    def setZProbeOffset(self, offset):
        '''
        Sets Z Probe offset from spinbox

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''

        octopiclient.gcode(command='M851 Z{}'.format(offset))
        octopiclient.gcode(command='M500')

    def setZHomeOffset(self, offset, setOffset=False):
        '''
        Sets the home offset after the calibration wizard is done, which is a callback to
        the response of M114 that is sent at the end of the Wizard in doneStep()
        :param offset: the value off the offset to set. is a str is coming from M114, and is float if coming from the nozzleOffsetPage
        :param setOffset: Boolean, is true if the function call is from the nozzleOffsetPage, else the current Z value sets the offset
        :return:

        #TODO can make this simpler, asset the offset value to string float to begin with instead of doing confitionals
        '''

        if self.setHomeOffsetBool:
            octopiclient.gcode(command='M206 Z{}'.format(-float(offset)))
            self.setHomeOffsetBool = False
            octopiclient.gcode(command='M500')
            # save in EEPROM
        if setOffset:    # When the offset needs to be set from spinbox value
            octopiclient.gcode(command='M206 Z{}'.format(-offset))
            octopiclient.gcode(command='M500')

    def nozzleOffset(self):
        '''
        Updates the value of M206 Z in the nozzle offset spinbox. Sends M503 so that the pritner returns the value as a websocket calback
        :return:
        '''
        octopiclient.gcode(command='M503')
        self.stackedWidget.setCurrentWidget(self.nozzleOffsetPage)

    def quickStep1(self):
        '''
        Shows welcome message.
        Sets Z Home Offset = 0
        Homes to MAX
        goes to position where leveling screws can be opened
        :return:
        '''

        octopiclient.gcode(command='M503')
        octopiclient.gcode(command='M420 S0')
        octopiclient.gcode(command='M206 Z0')
        octopiclient.home(['x', 'y', 'z'])
        octopiclient.jog(x=100, y=100, z=15, absolute=True, speed=1500)
        self.stackedWidget.setCurrentWidget(self.quickStep1Page)

    def quickStep2(self):
        '''
        Askes user to release all Leveling Screws
        :return:
        '''
        self.stackedWidget.setCurrentWidget(self.quickStep2Page)
        if self.printerName != "Julia Pro Single Nozzle":
            self.movie1 = QtGui.QMovie("templates/img/calibration/calib1.gif")
            self.calib1.setMovie(self.movie1)
            self.movie1.start()

    def quickStep3(self):
        '''
        leveks first position
        :return:
        '''
        self.stackedWidget.setCurrentWidget(self.quickStep3Page)
        octopiclient.jog(x=self.calibrationPosition['X1'], y=self.calibrationPosition['Y1'], absolute=True, speed=9000)
        octopiclient.jog(z=0, absolute=True, speed=1500)
        if self.printerName != "Julia Pro Single Nozzle":
            self.movie1.stop()
            self.movie2 = QtGui.QMovie("templates/img/calibration/calib2.gif")
            self.calib2.setMovie(self.movie2)
            self.movie2.start()

    def quickStep4(self):
        '''
        levels second leveling position
        '''
        self.stackedWidget.setCurrentWidget(self.quickStep4Page)
        octopiclient.jog(z=10, absolute=True, speed=1500)
        octopiclient.jog(x=self.calibrationPosition['X2'], y=self.calibrationPosition['Y2'], absolute=True, speed=9000)
        octopiclient.jog(z=0, absolute=True, speed=1500)
        if self.printerName != "Julia Pro Single Nozzle":
            self.movie2.stop()
            self.movie3 = QtGui.QMovie("templates/img/calibration/calib3.gif")
            self.calib3.setMovie(self.movie3)
            self.movie3.start()

    def quickStep5(self):
        '''
        levels third leveling position
        :return:
        '''
        self.stackedWidget.setCurrentWidget(self.quickStep5Page)
        octopiclient.jog(z=10, absolute=True, speed=1500)
        octopiclient.jog(x=self.calibrationPosition['X3'], y=self.calibrationPosition['Y3'], absolute=True, speed=9000)
        octopiclient.jog(z=0, absolute=True, speed=1500)
        if self.printerName != "Julia Pro Single Nozzle":
            self.movie3.stop()
            self.movie4 = QtGui.QMovie("templates/img/calibration/calib4.gif")
            self.calib4.setMovie(self.movie4)
            self.movie4.start()

    # def quickStep6(self):
    #     '''
    #     Performs Auto bed Leveiling, required for Klipper
    #     '''
    #     self.stackedWidget.setCurrentWidget(self.quickStep6Page)
    #     octopiclient.gcode(command='M190 S70')
    #     octopiclient.gcode(command='G29')

    def doneStep(self):
        '''
        decides weather to go to full calibration of return to calibration screen
        :return:
        '''

        self.stackedWidget.setCurrentWidget(self.calibratePage)
        self.movie4.stop()
        octopiclient.gcode(command='M501')
        octopiclient.home(['x', 'y', 'z'])

    def cancelStep(self):
        octopiclient.gcode(command='M501')
        self.stackedWidget.setCurrentWidget(self.calibratePage)
        try:
            self.movie1.stop()
            self.movie2.stop()
            self.movie3.stop()
            self.movie4.stop()
        except:
            pass
