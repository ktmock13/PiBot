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

INPUT_WINDOW_SIZE = (480.000, 360.000)
CAM_RES = (480, 360)

class InputWindow:
    def __init__(self, robot):
        self.robot = robot
        text = StringVar()
        text.set("Mouse around to guide laser, L/R click to pan, Press ESC to close")
        self.inputFrame = Frame(robot.root, width=INPUT_WINDOW_SIZE[0], height=INPUT_WINDOW_SIZE[1])
        self.label = Label(robot.root, textvariable=text)
        self.inputFrame.bind('<Motion>', lambda event: robot.arm.motion(event))
        self.inputFrame.bind('<ButtonPress-1>', lambda event: robot.platform.startRotation("R"))
        self.inputFrame.bind('<ButtonRelease-1>', lambda event: robot.platform.stopRotation())
        self.inputFrame.bind('<ButtonPress-3>', lambda event: robot.platform.startRotation("L"))
        self.inputFrame.bind('<ButtonRelease-3>', lambda event: robot.platform.stopRotation())
        self.robot.root.bind('<space>', lambda event: robot.arm.captureCenter())
        self.robot.root.bind('f', lambda event: robot.toggleTracking())
        self.robot.root.bind('x', lambda event: robot.arm.captureRange('x'))
        self.robot.root.bind('y', lambda event: robot.arm.captureRange('y'))
        self.robot.root.bind('r', lambda event: robot.arm.setDefaults())
        self.robot.root.bind('<Escape>', lambda event: robot.kill())
        self.label.pack()
        self.inputFrame.pack()

class OutputWindow:
    def __init__(self, root, robot):
        self.root = root
        self.robot = robot
        self.frame = Frame(self.root)
        self.quitButton = Button(self.frame, text = 'Close', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.thread = threading.Thread(target=robot.eye.videoLoop, args=(self,))
        self.thread.start()
        self.panel = None
        self.frame.pack()

    def drawGuidesAndText(self, frame, guides):

        modeText = 'MANUAL CONTROL + TRACKING' if self.robot.isTracking else 'MANUAL CONTROL'
        cv2.putText(frame , modeText, (0,10), cv2.FONT_HERSHEY_SIMPLEX, .4, (255,255,255), 1) # place text over image
        cv2.putText(frame, '<f> to toggle face tracking', (0,25), 16, .3, (255,255,255), 1)


        # draw guides on the image based on list 'guides.' Ex 3x3 box guides position naming (x, y), F= first, M = mid, L = last
        getPosition = lambda (i, x): 0 if x == 'F' else guidePositions[x](i)
        guides = ['FF', 'FM', 'FL', 'MF', 'MM', 'ML', 'LF', 'LM', 'LL'] if len(guides) ==0 or guides[0] == 'All' else guides
        guideBoxSize = 10 # size of guide box
        guidePositions = { # lambda fn to find top-left starting point of the guide boxes M & L (always 0 for 'F = first')
            'M': lambda axis: CAM_RES[axis]/2 - guideBoxSize/2,
            'L': lambda axis:CAM_RES[axis] - guideBoxSize
        }

        if self.robot.isTracking:
            faces = self.robot.trackingHaar.detectMultiScale(frame, 1.1, 5)
            for (x,y,w,h) in faces:
                xPercent = float(x+(w/2))/float(self.robot.eye.camera.resolution[0]);
                yPercent = float(y+(h/2))/float(self.robot.eye.camera.resolution[1]);
                print ('Face at percents...', xPercent, yPercent)
                self.robot.arm.positionPercent(xPercent,yPercent)
        else:
            for guideKey in guides:
                guideStartPos = map(getPosition, enumerate(guideKey)) # map the x and y for the start point of the guidebox depending on the letter Fist,Middle,Last
                guideEndPos = (guideStartPos[0] + guideBoxSize, guideStartPos[1] + guideBoxSize) # guide ends at the position ex. 10,10 from start
                cv2.rectangle(frame, tuple(guideStartPos), guideEndPos, (255,255,255), 1) # paint this guide

            # calibrate instructions
            cv2.putText(frame, 'CALIBRATION STEPS,  <r> reset defaults', (0,50), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,255,255), 1) # place text over image
            cv2.putText(frame, '  Focus laser into box and press <key>', (0,65), 16, .3, (255,255,255), 1) # place text over image

            middleTextPos = tuple(map(getPosition, enumerate('MM')))
            cv2.putText(frame, '1. <SPACE> capture center', (middleTextPos[0], middleTextPos[1]+guideBoxSize*2+5), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,255,255), 1) # place text over image

            leftTextPos = tuple(map(getPosition, enumerate('FM')))
            cv2.putText(frame, '2. <x> capture x-edge', (leftTextPos[0], leftTextPos[1]+guideBoxSize*2+5), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,255,255), 1) # place text over image
            #
            topTextPos = tuple(map(getPosition, enumerate('MF')))
            cv2.putText(frame, '3. <y> capture y-edge', (topTextPos[0], topTextPos[1]+guideBoxSize*2+5), cv2.FONT_HERSHEY_SIMPLEX, .3, (255,255,255), 1) # place text over image

    def close_windows(self):
        self.root.destroy()

class Robot:

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        self.platform = TurretPlatform()
        self.arm = LaserArm(INPUT_WINDOW_SIZE)
        self.root = Tk()
        self.eye = Eye(CAM_RES[0],CAM_RES[1],10)
        self.isTracking = False
        self.trackingHaar = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

    def toggleTracking(self):
        self.isTracking = not self.isTracking

    def run(self):
        self.app = InputWindow(self)
        self.app = OutputWindow(Toplevel(self.root), self)
        self.root.mainloop()

    def kill(self):
        self.arm.setLaser(0)
        self.root.destroy()
        self.root.quit()
