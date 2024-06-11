from MainUIClass.decorators import run_async
import time
from MainUIClass.config import Development

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