from Tkinter import *
import RPi.GPIO as GPIO
import time
import os
import threading
from multiprocessing import Process, Manager

#constants
TWO_PHASE_FULL_SEQUENCE = [ [1,0,0,1],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1] ]

SETPPER_OUT_PINS = [16,18,22,32]

STEPPER_SPEED = 0.004


class TurretPlatform:
    #relays information to 4 pins where there all steppers invloving rotation should be plugged
    def __init__(self):
        self.rotationProcess = None
        for pin in SETPPER_OUT_PINS:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin,0)

    def rotateLeft(self):
        while True:
            for halfstep in range(4):
                for pin in range(4):
                        GPIO.output(SETPPER_OUT_PINS[pin], TWO_PHASE_FULL_SEQUENCE[halfstep][pin])
                time.sleep(STEPPER_SPEED)

    def rotateRight(self):
        while True:
            for halfstep in reversed(range(4)):
                for pin in range(4):
                        GPIO.output(SETPPER_OUT_PINS[pin], TWO_PHASE_FULL_SEQUENCE[halfstep][pin])
                time.sleep(STEPPER_SPEED)

    def startRotation(self, direction):
        if(self.rotationProcess):
            self.rotationProcess.terminate()
        if(direction == 'L'):
            self.rotationProcess = Process(target = self.rotateLeft)
        else:
            self.rotationProcess = Process(target = self.rotateRight)
        self.rotationProcess.start()

    def stopRotation(self):
        if(self.rotationProcess):
            self.rotationProcess.terminate()
            self.rotationProcess = None
