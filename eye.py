from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
from Tkinter import *
from PIL import Image
from PIL import ImageTk

class Eye:
    #relays information to 4 pins where there all steppers invloving rotation should be plugged
    def __init__(self, resWidth, resHeight, framerate):
        self.camera = PiCamera()
        self.camera.resolution = (resWidth, resHeight)
        self.camera.framerate = framerate
        self.rawCapture = PiRGBArray(self.camera, size=(resWidth, resHeight))
        self.objectWidth = 50
        self.objectHeight = 50
        self.xPercent = resHeight/2;
        self.yPercent = resWidth/2;

    def getCenter(self):
        return (self.xPercent, self.yPercent);

    def videoLoop(self, outputWindow):
        try:
            for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
                image = frame.array
                grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                outputWindow.drawGuidesAndText(grayImg, ['MM', 'FM', 'MF'])

                if outputWindow.robot.isTracking:
                    faces = outputWindow.robot.trackingHaar.detectMultiScale(grayImg, 1.1, 5)
                    for (x,y,w,h) in faces:
                        xPercent = float(x+(w/2))/float(outputWindow.robot.eye.camera.resolution[0]);
                        yPercent = float(y+(h/2))/float(outputWindow.robot.eye.camera.resolution[1]);
                        outputWindow.robot.arm.positionPercent(xPercent, yPercent)

                grayImg= Image.fromarray(grayImg)
                grayPhotoImg = ImageTk.PhotoImage(grayImg)
                if outputWindow.panel is None: # create and mount panel if it's not there
                    outputWindow.panel = Label(outputWindow.frame, image=grayPhotoImg)
                    outputWindow.panel.image = grayPhotoImg
                    outputWindow.panel.pack(padx=10, pady=10)
                else:
                    outputWindow.panel.configure(image=grayPhotoImg)
                    outputWindow.panel.image = grayPhotoImg
                self.rawCapture.truncate(0)

        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")
