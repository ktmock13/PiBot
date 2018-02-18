from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (160, 128)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(160, 128))

# allow the camera to warmup
time.sleep(0.1)
face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	image = frame.array
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	for (x,y,w,h) in faces:
	    cv2.rectangle(gray,(x,y),(x+w,y+h),(255,255,0),1)
	# show the frame
	cv2.imshow("Frame", gray)
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for the next frame
	rawCapture.truncate(0)

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break
