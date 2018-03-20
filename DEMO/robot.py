from Tkinter import *
import RPi.GPIO as GPIO
import time
import os
import cv2
import threading
from multiprocessing import Process, Manager
from turret import TurretPlatform
from arm import LaserArm
from eye import Eye
from PIL import Image
from PIL import ImageTk

BOX_MAX_X = 499.000
BOX_MAX_Y = 499.000

CAM_RES = (640, 480)

class InputWindow:
    def __init__(self, robot):
        self.robot = robot
        self.inputFrame = Frame(self.robot.root, width=BOX_MAX_X, height=BOX_MAX_Y)
        self.inputFrame.bind('<Motion>', lambda event: robot.arm.motion(event))
        self.inputFrame.bind('<ButtonPress-1>', lambda event: robot.platform.startRotation("L"))
        self.inputFrame.bind('<ButtonRelease-1>', lambda event: robot.platform.stopRotation())
        self.inputFrame.bind('<ButtonPress-3>', lambda event: robot.platform.startRotation("R"))
        self.inputFrame.bind('<ButtonRelease-3>', lambda event: robot.platform.stopRotation())
        self.inputFrame.pack()

class OutputWindow:
    def __init__(self, root, robot):
        self.root = root
        self.robot = robot
        self.frame = Frame(self.root)
        self.calibrating = None
        self.quitButton = Button(self.frame, text = 'Done', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.panel = None
        self.frame.pack()

    def drawGuidesAndText(self, frame, guides, infoText):
        # draw guides on the image based on list 'guides.' Ex 3x3 box guides position naming (x, y), F= first, M = mid, L = last
        # FF, MF, LF
        # FM, MM, LM
        # FL, ML, LL
        # print the provided guides otherwise print all the guides
        guides = ['FF', 'FM', 'FL', 'MF', 'MM', 'ML', 'LF', 'LM', 'LL'] if len(guides) ==0 or guides[0] == 'All' else guides
        guideBoxSize = 10 # size of guide box
        guidePositions = { # lambda fn to find top-left starting point of the guide boxes M & L (always 0 for 'F = first')
            'M': lambda axis: CAM_RES[axis]/2 - guideBoxSize/2,
            'L': lambda axis:CAM_RES[axis] - guideBoxSize
        }

        for guideKey in guides:
            guideStartPos = map(lambda (i, x): 0 if x == 'F' else guidePositions[x](i), enumerate(guideKey)) # map the x and y for the start point of the guidebox depending on the letter Fist,Middle,Last
            guideEndPos = (guideStartPos[0] + guideBoxSize, guideStartPos[1] + guideBoxSize) # guide ends at the position ex. 10,10 from start
            cv2.rectangle(frame, tuple(guideStartPos), guideEndPos, (255,255,255), 1) # paint this guide

        cv2.putText(frame ,infoText, (10,50), cv2.FONT_HERSHEY_SIMPLEX, .5, (255,255,255), 2) # place text over image

    def videoLoop(self):
        try:
            for frame in self.robot.eye.camera.capture_continuous(self.robot.eye.rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                self.drawGuidesAndText(grayImg, ['All'], 'Hi Mom!')
                grayImg= Image.fromarray(grayImg)
                grayPhotoImg = ImageTk.PhotoImage(grayImg)
                if self.panel is None:
                    self.panel = Label(self.frame, image=grayPhotoImg)
                    self.panel.image = grayPhotoImg
                    self.panel.pack(padx=10, pady=10)
                else:
                    self.panel.configure(image=grayPhotoImg)
                    self.panel.image = grayPhotoImg
                self.robot.eye.rawCapture.truncate(0)

        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")

    def close_windows(self):
        self.root.destroy()

class Robot:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.platform = TurretPlatform()
        self.arm = LaserArm(BOX_MAX_X, BOX_MAX_Y)
        self.root = Tk()
        self.eye = Eye(CAM_RES[0],CAM_RES[1],30)
        self.inputFrame = Frame(self.root, width=BOX_MAX_X, height=BOX_MAX_Y)
        self.inputFrame.bind('<Motion>', lambda event: self.arm.motion(event))
        self.inputFrame.bind('<ButtonPress-1>', lambda event: self.platform.startRotation("L"))
        self.inputFrame.bind('<ButtonRelease-1>', lambda event: self.platform.stopRotation())
        self.inputFrame.bind('<ButtonPress-3>', lambda event: self.platform.startRotation("R"))
        self.inputFrame.bind('<ButtonRelease-3>', lambda event: self.platform.stopRotation())
        self.inputFrame.bind('<ButtonPress-2>', lambda event: self.calibrateTest('w'))

    def calibrateTest(self, textMsg):
        print textMsg

    def run(self):
        self.app = InputWindow(self)
        self.app = OutputWindow(Toplevel(self.root), self)
        self.root.bind('<space>', lambda event: self.kill())
        self.root.mainloop()

    def kill(self):
        self.arm.setLaser(0)
        self.root.destroy()
        self.root.quit()
