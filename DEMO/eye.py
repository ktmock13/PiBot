from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import Tkinter
import Image, ImageTk

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

    def recognizeFace(self, showPreview):
        face_cascade = cv2.CascadeClassifier('../CAM/haar/haarcascade_frontalface_default.xml')
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            # grab the raw NumPy array representing the image, then initialize the timestamp
            # and occupied/unoccupied text
            image = frame.array

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x,y,w,h) in faces:
                self.xPercent = float(x+(w/2))/float(self.camera.resolution[0]);
                self.yPercent = float(y+(h/2))/float(self.camera.resolution[1]);
                if showPreview:
                    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,255,0),1)
            # print the coords
            print 'face percents on screen'
            print (self.xPercent, self.yPercent);

            # show the frame
            if showPreview:
            	cv2.imshow("Frame", gray)

            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("c"):
                break

    def followFaceWithArm(self, arm):
        face_cascade = cv2.CascadeClassifier('../CAM/haar/haarcascade_frontalface_default.xml')
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):

            image = frame.array

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.1, 5)
            for (x,y,w,h) in faces:
                self.xPercent = float(x+(w/2))/float(self.camera.resolution[0]);
                self.yPercent = float(y+(h/2))/float(self.camera.resolution[1]);
                self.objectWidth = w
                self.objectHeight = h
                arm.positionPercent(self.xPercent,self.yPercent)
                arm.setScale(w,h)

            print ('Face at percents...', self.xPercent,self.yPercent, '  Face dims...', self.objectWidth, self.objectHeight)
            # go to face

            key = cv2.waitKey(1) & 0xFF

            # clear the stream in preparation for the next frame
            self.rawCapture.truncate(0)

            # if the `q` key was pressed, break from the loop
            if key == ord("c"):
                break

    def camPreview(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
        	# grab the raw NumPy array representing the image, then initialize the timestamp
        	# and occupied/unoccupied text
        	image = frame.array

        	cv2.imshow("Frame", image)
        	key = cv2.waitKey(1) & 0xFF

        	# clear the stream in preparation for the next frame
        	self.rawCapture.truncate(0)

        	# if the `q` key was pressed, break from the loop
        	if key == ord("x"):
        		break
