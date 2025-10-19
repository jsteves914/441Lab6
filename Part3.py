#shifter.py
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
            GPIO.output(self.serialPin, (value >> i) & 1)
            self._ping(self.clockPin)
        self._ping(self.latchPin)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    serial = int(input("Enter the serial/data pin (BCM): "))
    clock = int(input("Enter the clock pin (BCM): "))
    latch = int(input("Enter the latch pin (BCM): "))
    s = Shifter(serial, clock, latch)
    pattern = 0b01100110
    s.shiftByte(pattern)
    input("Press Enter to exit...")
    s.cleanup()
