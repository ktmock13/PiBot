from __future__ import division
import RPi.GPIO as GPIO
import time

# Import the PCA9685 module.
import Adafruit_PCA9685
#constants
CHANNEL_X = 3
CHANNEL_Y = 11
LASER_PIN = 37
ROUGH_CENTER = (221, 427)


class LaserArm:

    def __init__(self, maxInputs):
        GPIO.setup(LASER_PIN, GPIO.OUT)
        GPIO.output(LASER_PIN, 1)
        self.reset(maxInputs)

    def reset(self, maxInputs):
        self.pwm = Adafruit_PCA9685.PCA9685() # uses pins 3,5 by default (i2c)
        self.pwm.set_pwm_freq(50)
        self.currentPercents = { 'x': 0.5, 'y': 0.5 } # simulate start right in the middle
        self.maxInputs = { 'x': maxInputs[0], 'y': maxInputs[1] } 
        self.center = { 'x': ROUGH_CENTER[0], 'y': ROUGH_CENTER[1] } # values to correct true center, since far center could be different than close center (camera is above laser beam)
        self.range = { 'x': 50, 'y': 50 }  # 'point' distance servo may deviate from center on X,Y axis = 100
        self.duties = self.center

    def setLaser(self, value):
        GPIO.output(LASER_PIN, value)
    
    def amputate(self):
        print("amputating arm")
        self.setLaser(0)

    def position(self, x, y):
        self.currentPercents = { 'x': x / self.maxInputs['x'], 'y': y / self.maxInputs['y'] } 
        dutyX = ((self.center['x']) - (((x / self.maxInputs['x']) * self.range['x'] * 2) - self.range['x'])) +100
        dutyY = ((self.center['y']) + (((y / self.maxInputs['y']) * self.range['y'] * 2) - self.range['y'])) +100
        self.pwm.set_pwm(CHANNEL_X, 50, int(round(dutyX)))
        self.pwm.set_pwm(CHANNEL_Y, 50, int(round(dutyY)))
        self.duties = { 'x': int(round(dutyX)), 'y': int(round(dutyY))}

    def directionalMove(self, direction):
        positionPercent()
        print (direction)

    def positionPercent(self, xPercent, yPercent):
        self.position(self.maxInputs['x'] * xPercent, self.maxInputs['y'] * yPercent)

    def captureCenter(self):
        self.center = self.duties
    
    def printSettings(self):
        print ('currentPercents:', self.currentPercents)
        print ('maxInputs: ', self.maxInputs)
        print ('center: ', self.center)
        print ('range: ', self.range)
        print ('duties: ', self.duties)

    def setDefaults(self):
        self.reset((self.maxInputs['x'], self.maxInputs['y']))

    def captureRange(self, axis):
        self.range[axis] = abs(self.duties[axis] - self.center[axis])

    def motion(self, event):
        print "x %d y %d mouse input" % (event.x, event.y)
        self.position(event.x, event.y)



('maxInputs: ', {'y': 360.0, 'x': 480.0})
('center: ', {'y': 427, 'x': 221})
('range: ', {'y': 49, 'x': 54})
('duties: ', {'y': 446, 'x': 228})
