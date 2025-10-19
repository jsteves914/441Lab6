import time
import RPi.GPIO as GPIO

class Shifter:
    def __init__(self, serialPin, clockPin, latchPin):
        self.serialPin = serialPin
        self.clockPin = clockPin
        self.latchPin = latchPin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.serialPin, GPIO.OUT)
        GPIO.setup(self.clockPin, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latchPin, GPIO.OUT, initial=GPIO.LOW)

    def _ping(self, pin, delay=0.0005):
        GPIO.output(pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(pin, GPIO.LOW)
        time.sleep(delay)

    def shiftByte(self, value):
        value &= 0xFF
        GPIO.output(self.latchPin, GPIO.LOW)
        for i in range(8):
            bit = (value >> i) & 1
            GPIO.output(self.serialPin, bit)
            self._ping(self.clockPin)
        self._ping(self.latchPin)

    def cleanup(self):
        GPIO.cleanup()
