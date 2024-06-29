import mainGUI
from logger import *

class controlScreen(mainGUI.Ui_MainWindow):
    def __init__(self):
        log_info("Starting control screen init.")
        self.octopiclient = None
        super().__init__()
        
    
    def setup(self, octopiclient):
        self.octopiclient = octopiclient
        self.moveYPButton.pressed.connect(lambda: self.octopiclient.jog(y=self.step, speed=1000))
        self.moveYMButton.pressed.connect(lambda: self.octopiclient.jog(y=-self.step, speed=1000))
        self.moveXMButton.pressed.connect(lambda: self.octopiclient.jog(x=-self.step, speed=1000))
        self.moveXPButton.pressed.connect(lambda: self.octopiclient.jog(x=self.step, speed=1000))
        self.moveZPButton.pressed.connect(lambda: self.octopiclient.jog(z=self.step, speed=1000))
        self.moveZMButton.pressed.connect(lambda: self.octopiclient.jog(z=-self.step, speed=1000))
        self.extruderButton.pressed.connect(lambda: self.octopiclient.extrude(self.step))
        self.retractButton.pressed.connect(lambda: self.octopiclient.extrude(-self.step))
        self.motorOffButton.pressed.connect(lambda: self.octopiclient.gcode(command='M18'))
        self.fanOnButton.pressed.connect(lambda: self.octopiclient.gcode(command='M106'))
        self.fanOffButton.pressed.connect(lambda: self.octopiclient.gcode(command='M107'))
        self.cooldownButton.pressed.connect(self.coolDownAction)
        self.step100Button.pressed.connect(lambda: self.setStep(100))
        self.step1Button.pressed.connect(lambda: self.setStep(1))
        self.step10Button.pressed.connect(lambda: self.setStep(10))
        self.homeXYButton.pressed.connect(lambda: self.octopiclient.home(['x', 'y']))
        self.homeZButton.pressed.connect(lambda: self.octopiclient.home(['z']))
        self.controlBackButton.pressed.connect(lambda: self.stackedWidget.setCurrentWidget(self.homePage))
        self.setToolTempButton.pressed.connect(lambda: self.octopiclient.setToolTemperature(
            self.toolTempSpinBox.value()))
        self.setBedTempButton.pressed.connect(lambda: self.octopiclient.setBedTemperature(self.bedTempSpinBox.value()))

        self.setFlowRateButton.pressed.connect(lambda: self.octopiclient.flowrate(self.flowRateSpinBox.value()))
        self.setFeedRateButton.pressed.connect(lambda: self.octopiclient.feedrate(self.feedRateSpinBox.value()))

        # self.moveZPBabyStep.pressed.connect(lambda: self.octopiclient.gcode(command='SET_GCODE_OFFSET Z_ADJUST=0.025 MOVE=1'))
        # self.moveZMBabyStep.pressed.connect(lambda: self.octopiclient.gcode(command='SET_GCODE_OFFSET Z_ADJUST=-0.025 MOVE=1'))
        self.moveZPBabyStep.pressed.connect(lambda: self.octopiclient.gcode(command='M290 Z0.025'))
        self.moveZMBabyStep.pressed.connect(lambda: self.octopiclient.gcode(command='M290 Z-0.025'))


    @classmethod
    def control(self):
        self.stackedWidget.setCurrentWidget(self.controlPage)
        self.toolTempSpinBox.setProperty("value", float(self.tool0TargetTemperature.text()))
        self.bedTempSpinBox.setProperty("value", float(self.bedTargetTemperature.text()))

    def setStep(self, stepRate):
        '''
        Sets the class variable "Step" which would be needed for movement and jogging
        :param stepRate: step multiplier for movement in the move
        :return: nothing
        '''
        
        if stepRate == 100:
            self.step100Button.setFlat(True)
            self.step1Button.setFlat(False)
            self.step10Button.setFlat(False)
            self.step = 100
        if stepRate == 1:
            self.step100Button.setFlat(False)
            self.step1Button.setFlat(True)
            self.step10Button.setFlat(False)
            self.step = 1
        if stepRate == 10:
            self.step100Button.setFlat(False)
            self.step1Button.setFlat(False)
            self.step10Button.setFlat(True)
            self.step = 10

    @classmethod
    def coolDownAction(self):
        '''
        Turns all heaters and fans off
        '''
        self.octopiclient.gcode(command='M107')
        self.octopiclient.setToolTemperature({"tool0": 0})
        self.octopiclient.setBedTemperature(0)
        self.toolTempSpinBox.setProperty("value", 0)
        self.bedTempSpinBox.setProperty("value", 0)
