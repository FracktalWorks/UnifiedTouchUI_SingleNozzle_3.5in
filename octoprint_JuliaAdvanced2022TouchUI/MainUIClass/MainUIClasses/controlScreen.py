from MainUIClass.config import octopiclient

class controlScreen:
    def __init__(self, MainUIObj):
        self.MainUIObj = MainUIObj
        
    def connect(self):
        self.MainUIObj.moveYPButton.pressed.connect(lambda: octopiclient.jog(y=self.step, speed=1000))
        self.MainUIObj.moveYMButton.pressed.connect(lambda: octopiclient.jog(y=-self.step, speed=1000))
        self.MainUIObj.moveXMButton.pressed.connect(lambda: octopiclient.jog(x=-self.step, speed=1000))
        self.MainUIObj.moveXPButton.pressed.connect(lambda: octopiclient.jog(x=self.step, speed=1000))
        self.MainUIObj.moveZPButton.pressed.connect(lambda: octopiclient.jog(z=self.step, speed=1000))
        self.MainUIObj.moveZMButton.pressed.connect(lambda: octopiclient.jog(z=-self.step, speed=1000))
        self.MainUIObj.extruderButton.pressed.connect(lambda: octopiclient.extrude(self.step))
        self.MainUIObj.retractButton.pressed.connect(lambda: octopiclient.extrude(-self.step))
        self.MainUIObj.motorOffButton.pressed.connect(lambda: octopiclient.gcode(command='M18'))
        self.MainUIObj.fanOnButton.pressed.connect(lambda: octopiclient.gcode(command='M106'))
        self.MainUIObj.fanOffButton.pressed.connect(lambda: octopiclient.gcode(command='M107'))
        self.MainUIObj.cooldownButton.pressed.connect(self.coolDownAction)
        self.MainUIObj.step100Button.pressed.connect(lambda: self.setStep(100))
        self.MainUIObj.step1Button.pressed.connect(lambda: self.setStep(1))
        self.MainUIObj.step10Button.pressed.connect(lambda: self.setStep(10))
        self.MainUIObj.homeXYButton.pressed.connect(lambda: octopiclient.home(['x', 'y']))
        self.MainUIObj.homeZButton.pressed.connect(lambda: octopiclient.home(['z']))
        self.MainUIObj.controlBackButton.pressed.connect(lambda: self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.homePage))
        self.MainUIObj.setToolTempButton.pressed.connect(lambda: octopiclient.setToolTemperature(
            self.MainUIObj.toolTempSpinBox.value()))
        self.MainUIObj.setBedTempButton.pressed.connect(lambda: octopiclient.setBedTemperature(self.MainUIObj.bedTempSpinBox.value()))

        self.MainUIObj.setFlowRateButton.pressed.connect(lambda: octopiclient.flowrate(self.MainUIObj.flowRateSpinBox.value()))
        self.MainUIObj.setFeedRateButton.pressed.connect(lambda: octopiclient.feedrate(self.MainUIObj.feedRateSpinBox.value()))

        # self.MainUIObj.moveZPBabyStep.pressed.connect(lambda: octopiclient.gcode(command='SET_GCODE_OFFSET Z_ADJUST=0.025 MOVE=1'))
        # self.MainUIObj.moveZMBabyStep.pressed.connect(lambda: octopiclient.gcode(command='SET_GCODE_OFFSET Z_ADJUST=-0.025 MOVE=1'))
        self.MainUIObj.moveZPBabyStep.pressed.connect(lambda: octopiclient.gcode(command='M290 Z0.025'))
        self.MainUIObj.moveZMBabyStep.pressed.connect(lambda: octopiclient.gcode(command='M290 Z-0.025'))

    def control(self):
        self.MainUIObj.stackedWidget.setCurrentWidget(self.MainUIObj.controlPage)
        self.MainUIObj.toolTempSpinBox.setProperty("value", float(self.MainUIObj.tool0TargetTemperature.text()))
        self.MainUIObj.bedTempSpinBox.setProperty("value", float(self.MainUIObj.bedTargetTemperature.text()))

    def setStep(self, stepRate):
        '''
        Sets the class variable "Step" which would be needed for movement and jogging
        :param stepRate: step multiplier for movement in the move
        :return: nothing
        '''
        
        if stepRate == 100:
            self.MainUIObj.step100Button.setFlat(True)
            self.MainUIObj.step1Button.setFlat(False)
            self.MainUIObj.step10Button.setFlat(False)
            self.step = 100
        if stepRate == 1:
            self.MainUIObj.step100Button.setFlat(False)
            self.MainUIObj.step1Button.setFlat(True)
            self.MainUIObj.step10Button.setFlat(False)
            self.step = 1
        if stepRate == 10:
            self.MainUIObj.step100Button.setFlat(False)
            self.MainUIObj.step1Button.setFlat(False)
            self.MainUIObj.step10Button.setFlat(True)
            self.step = 10

    def coolDownAction(self):
        '''
        Turns all heaters and fans off
        '''
        octopiclient.gcode(command='M107')
        octopiclient.setToolTemperature({"tool0": 0})
        octopiclient.setBedTemperature(0)
        self.MainUIObj.toolTempSpinBox.setProperty("value", 0)
        self.MainUIObj.bedTempSpinBox.setProperty("value", 0)
