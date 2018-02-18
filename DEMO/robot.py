from Tkinter import *
import RPi.GPIO as GPIO
import time
import os
import threading
from multiprocessing import Process, Manager
from turret import TurretPlatform
from arm2 import LaserArm
from eye import Eye

BOX_MAX_X =499.000
BOX_MAX_Y = 499.000

class Robot:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        # self.platform = TurretPlatform()
        self.arm = LaserArm(BOX_MAX_X, BOX_MAX_Y)
        self.root = Tk()
        self.eye = Eye(320,240,30)
        self.inputFrame = Frame(self.root, width=BOX_MAX_X, height=BOX_MAX_Y)
        self.inputFrame.bind('<Motion>', lambda event: self.arm.motion(event))
        # self.inputFrame.bind('<ButtonPress-1>', lambda event: self.platform.startRotation("L"))
        # self.inputFrame.bind('<ButtonRelease-1>', lambda event: self.platform.stopRotation())
        # self.inputFrame.bind('<ButtonPress-3>', lambda event: self.platform.startRotation("R"))
        # self.inputFrame.bind('<ButtonRelease-3>', lambda event: self.platform.stopRotation())
        self.root.bind('<space>', lambda event: self.kill())
    def run(self):

        # self.eye.camPreview()
        # self.eye.recognizeFace(True)
        self.eye.followFaceWithArm(self.arm)

        #mouse control window
        # self.inputFrame.pack()
        # self.inputFrame.mainloop()

    def kill(self):
        self.root.destroy()
        self.root.quit()
        self.arm.laserOff()
