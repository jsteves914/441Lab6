import time, random
from shifter import Shifter

serial = int(input("Enter the serial/data pin (BCM): "))
clock = int(input("Enter the clock pin (BCM): "))
latch = int(input("Enter the latch pin (BCM): "))

s = Shifter(serial, clock, latch)

pos = 3
dt = 0.05

try:
    while True:
        s.shiftByte(1 << pos)
        time.sleep(dt)
        step = -1 if random.random() < 0.5 else 1
        if pos == 0 and step == -1:
            step = 1
        elif pos == 7 and step == 1:
            step = -1
        pos += step
finally:
    s.cleanup()
