from time import sleep
from gpiozero import DigitalOutputDevice

seq =   [[1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1]]

class Stepper:
    def __init__(self, stepperpins, startpos):
        self.stepperpins = [DigitalOutputDevice(pin) for pin in stepperpins]
        self.pos = startpos
        self.step = 0

    def moveto(self, pos, d):
        while self.pos < pos:
            self.singlestep(1)
            self.pos += 1
            sleep(d)
        while self.pos > pos:
            self.singlestep(0)
            self.pos -= 1
            sleep(d)

    def singlestep(self, dir):
        if dir == 1:
            if self.step < 7:
                self.step += 1
            else:
                self.step = 0
        if dir == 0:
            if self.step > 0:
                self.step -= 1
            else:
                self.step = 7

        for pin in range(4):
            self.stepperpins[pin].value = seq[self.step][pin]


stepper = Stepper([4,23,24,25], 0)

for i in range(512):
    stepper.singlestep(1)
    sleep(0.001)
for i in range(512):
    stepper.singlestep(0)
    sleep(0.001)

stepper.moveto(10000,0.001)
sleep(1)
stepper.moveto(0,0.001)