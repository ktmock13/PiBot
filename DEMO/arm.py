from Tkinter import *
import RPi.GPIO as GPIO
import time
import os
import threading
from multiprocessing import Process, Manager
from turret import TurretPlatform
#constants

SERVOX_OUT_PIN = 11
SERVOY_OUT_PIN = 7

LASER_PIN = 13

SERVO_MIN_POS = 2.500
SERVO_NEUTRAL = 7.500
SERVO_MAX_POS = 12.500

SERVO_RANGE = SERVO_MAX_POS - SERVO_MIN_POS

LIMIT_RANGE_X=.3
LIMIT_RANGE_Y=.3

OFFSETX = 1.15
OFFSETY = .85

class LaserArm:

    def __init__(self, maxXInput, maxYInput):
        GPIO.setup(SERVOX_OUT_PIN, GPIO.OUT)
        GPIO.setup(SERVOY_OUT_PIN, GPIO.OUT)
        GPIO.setup(LASER_PIN, GPIO.OUT)
        GPIO.output(LASER_PIN, 1)
        self.maxXInput = maxXInput
        self.maxYInput =maxYInput
        self.servo_pulseX = GPIO.PWM(SERVOX_OUT_PIN,60)
        self.servo_pulseY = GPIO.PWM(SERVOY_OUT_PIN,60)
        self.resetLaser()

    def resetLaser(self):
        self.servo_pulseX.start(SERVO_NEUTRAL)
        self.servo_pulseY.start(SERVO_NEUTRAL)

    def laserOff(self):
        GPIO.output(LASER_PIN, 0)
        self.resetLaser(self)

    def position(self, x, y):
        dutyX = ((SERVO_NEUTRAL+OFFSETX) - (((x/self.maxXInput)*SERVO_RANGE)-SERVO_RANGE/2) * LIMIT_RANGE_X)
        dutyY = ((SERVO_NEUTRAL+OFFSETY) - (((y/self.maxYInput)*SERVO_RANGE)-SERVO_RANGE/2) * LIMIT_RANGE_Y)
        self.servo_pulseX.ChangeDutyCycle(round(dutyX,3))
        self.servo_pulseY.ChangeDutyCycle(round(dutyY,3))

    def positionPercent(self, xPercent, yPercent):
        self.position(self.maxXInput*xPercent, self.maxYInput*yPercent)


    def motion(self, event):
        self.position(event.x, event.y)
