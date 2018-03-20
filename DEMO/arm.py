from __future__ import division
import RPi.GPIO as GPIO
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
#constants
CHANNEL_X = 1
CHANNEL_Y = 0
LASER_PIN = 37

SERVO_MIN_POS = 200
SERVO_NEUTRAL = 400
SERVO_MAX_POS = 600

SERVO_RANGE = SERVO_MAX_POS - SERVO_MIN_POS

#settings for face @ 4 feet
LIMIT_RANGE_X=.4
LIMIT_RANGE_Y=.3

OFFSETX = -25
OFFSETY =30


class LaserArm:

    def __init__(self, maxXInput, maxYInput):
        GPIO.setup(LASER_PIN, GPIO.OUT)
        GPIO.output(LASER_PIN, 1)
        self.pwm = Adafruit_PCA9685.PCA9685()
        self.pwm.set_pwm_freq(60)
        self.maxXInput = maxXInput
        self.maxYInput =maxYInput
        # default face size @ 4 feet
        self.objectHeight = 55
        self.objectWidth = 55

    def setLaser(self, value):
        GPIO.output(LASER_PIN, value)

    def position(self, x, y):
        dutyX = ((SERVO_NEUTRAL+OFFSETX) - (((x/self.maxXInput)*SERVO_RANGE)-SERVO_RANGE/2) * LIMIT_RANGE_X)
        dutyY = ((SERVO_NEUTRAL+OFFSETY) + (((y/self.maxYInput)*SERVO_RANGE)-SERVO_RANGE/2) * LIMIT_RANGE_Y)

        self.pwm.set_pwm(CHANNEL_X, 0, int(round(dutyX)))
        self.pwm.set_pwm(CHANNEL_Y, 0, int(round(dutyY)))
        print ('Laser moving to...', dutyX, dutyY, 'pwm...', int(round(dutyX)), int(round(dutyX)))

    def positionPercent(self, xPercent, yPercent):
        self.position(self.maxXInput*xPercent, self.maxYInput*yPercent)

    def setScale(self, width, height):
        self.objectWidth = width
        self.objectHeight = height

    def motion(self, event):
        self.position(event.x, event.y)
