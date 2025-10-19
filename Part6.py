#bug.py
import time
import RPi.GPIO as GPIO
from Part5 import Bug

GPIO.setmode(GPIO.BCM)

s1 = int(input("Enter s1 pin (BCM): "))
s2 = int(input("Enter s2 pin (BCM): "))
s3 = int(input("Enter s3 pin (BCM): "))

GPIO.setup(s1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(s3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

serial = int(input("Enter the serial/data pin (BCM): "))
clock  = int(input("Enter the clock pin (BCM): "))
latch  = int(input("Enter the latch pin (BCM): "))

b = Bug(serial=serial, clock=clock, latch=latch)
base_dt = b.timestep
prev_s2 = GPIO.input(s2)
last_change = 0.0
DEBOUNCE = 0.03

try:
    while True:
        now = time.time()
        s1v = GPIO.input(s1)
        s2v = GPIO.input(s2)
        s3v = GPIO.input(s3)

  
        if s1v:
            b.start()
        else:
            b.stop()            

     
        if s2v != prev_s2 and (now - last_change) > DEBOUNCE:
            b.isWrapOn = not b.isWrapOn
            prev_s2 = s2v
            last_change = now

    
        b.timestep = max(0.001, base_dt / 3.0) if s3v else base_dt

        time.sleep(0.01)
except KeyboardInterrupt:
    pass
finally:
    b.close()
