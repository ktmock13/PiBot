from Tkinter import *
import RPi.GPIO as GPIO
import time
import os
import threading
from threading import Thread

GPIO.setmode(GPIO.BOARD)

stepper_output_pins = [16,18,22,32]
for pin in stepper_output_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)

twophasefull = [ [1,0,0,1],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1] ]

servoX_output_pin = 7
servoY_output_pin = 11

laser_pin = 13

GPIO.setup(servoX_output_pin, GPIO.OUT)
GPIO.setup(servoY_output_pin, GPIO.OUT)

GPIO.setup(laser_pin, GPIO.OUT)
GPIO.output(laser_pin, 1)

servo_pulseX = GPIO.PWM(servoX_output_pin,50)
servo_pulseY = GPIO.PWM(servoY_output_pin,50)

BOX_MAX_X =799.000
BOX_MAX_Y = 799.000

SERVO_MIN_POS = 2.500
SERVO_NEUTRAL = 7.500
SERVO_MAX_POS = 12.500

SERVO_RANGE = SERVO_MAX_POS - SERVO_MIN_POS

servo_pulseX.start(SERVO_MAX_POS - (SERVO_RANGE/2))
servo_pulseY.start(SERVO_MAX_POS - (SERVO_RANGE/2))

STEPPER_SPEED = 0.002

LIMIT_RANGE_X=1
LIMIT_RANGE_Y=1


calibrateX = 0.00
calibrateY = 0.00


# def getDutyCycle(currentPosition, maxPosition)

root = Tk()
frame = Frame(root, width=BOX_MAX_X, height=BOX_MAX_Y)

def moveLeft():
    for repeat in range(100):
        for halfstep in range(4):
            for pin in range(4):
                    GPIO.output(stepper_output_pins[pin], twophasefull[halfstep][pin])
            time.sleep(STEPPER_SPEED)

def moveRight():
    frame.focus_set()
    for repeat in range(100):
        for halfstep in reversed(range(4)):
            for pin in range(4):
                    GPIO.output(stepper_output_pins[pin], twophasefull[halfstep][pin])
            time.sleep(STEPPER_SPEED)

def callbackL(event):
    Thread(target = moveLeft).start()

def callbackR(event):
    Thread(target = moveRight).start()

def motion(event):
    x, y = event.x, event.y
    servo_pulseX.ChangeDutyCycle((SERVO_NEUTRAL - (((x/BOX_MAX_X)*SERVO_RANGE)-SERVO_RANGE/2) * LIMIT_RANGE_X) - SERVO_NEUTRAL * calibrateX)
    servo_pulseY.ChangeDutyCycle((SERVO_NEUTRAL - (((y/BOX_MAX_Y)*SERVO_RANGE)-SERVO_RANGE/2) * LIMIT_RANGE_Y) - SERVO_NEUTRAL * calibrateY)

frame.bind('<Motion>', motion)
frame.bind("<Button-1>", callbackL)
frame.bind("<Button-3>", callbackR)
frame.pack()

frame.mainloop()
frame.destroy()
