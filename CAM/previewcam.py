import time
import picamera
camera = picamera.PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
