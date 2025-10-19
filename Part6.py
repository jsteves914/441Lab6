# bug.py
import time
import RPi.GPIO as GPIO
from Part5 import Bug

s1 = int(input("Enter s1 pin (BCM): "))
s2 = int(input("Enter s2 pin (BCM): "))
s3 = int(input("Enter s3 pin (BCM): "))

GPIO.setmode(GPIO.BCM)
GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

b = Bug()  # defaults: timestep=0.1, x=3, isWrapOn=False
base_dt = b.timestep
prev_s2 = GPIO.input(s2)

try:
    while True:
        s1v = GPIO.input(s1)
        s2v = GPIO.input(s2)
        s3v = GPIO.input(s3)

        if s1v:
            b.start()
        else:
            b.stop()

        if s2v != prev_s2:
            b.isWrapOn = not b.isWrapOn
            prev_s2 = s2v

        b.timestep = max(0.001, base_dt / 3.0) if s3v else base_dt

        time.sleep(0.02)
except KeyboardInterrupt:
    pass
finally:
    b.stop()
    GPIO.cleanup()
