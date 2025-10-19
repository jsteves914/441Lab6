import time, random, threading
from Lab6Part3 import Shifter

class Bug:
    def __init__(self, timestep=0.1, x=3, isWrapOn=False, serial=None, clock=None, latch=None):
        if serial is None or clock is None or latch is None:
            raise ValueError("Provide serial, clock, and latch pins")
        self.timestep = float(timestep)
        self.x = int(x)
        self.isWrapOn = bool(isWrapOn)
        self.__shifter = Shifter(serial, clock, latch)
        self.__running = False
        self.__thread = None

    def __step_once(self):
        step = random.choice([-1, 1])
        if self.isWrapOn:
            self.x = (self.x + step) % 8
        else:
            if self.x == 0 and step == -1:
                step = 1
            elif self.x == 7 and step == 1:
                step = -1
            self.x += step

    def start(self):
        if self.__running:
            return
        self.__running = True
        def loop():
            try:
                while self.__running:
                    self.__shifter.shiftByte(1 << self.x)
                    time.sleep(self.timestep)
                    self.__step_once()
            finally:
                # leave GPIO configured; just blank the LEDs
                self.__shifter.shiftByte(0)
        self.__thread = threading.Thread(target=loop, daemon=True)
        self.__thread.start()

    def stop(self):
        if not self.__running:
            self.__shifter.shiftByte(0)
            return
