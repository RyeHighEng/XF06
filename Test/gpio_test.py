#Test setting the raspberry pi gpio pins:
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
def test():
    for i in range(10)
        GPIO.output(8, True)
        GPIO.output(10, False)
        GPIO.output(12, False)
        time.sleep(1)
        GPIO.output(8, False)
        GPIO.output(10, True)
        GPIO.output(12, False)
        time.sleep(1)
        GPIO.output(8, False)
        GPIO.output(10, False)
        GPIO.output(12, True)
        time.sleep(1)
        GPIO.output(8, True)
        GPIO.output(10, True)
        GPIO.output(12, True)
        time.sleep(1)
        InitState()
def InitState():
    GPIO.output(8, False)
    GPIO.output(10, False)
    GPIO.output(12, False)
InitState()
test()
