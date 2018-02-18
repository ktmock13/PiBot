import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 100)
p.start(5)
time.sleep(2)

for angle in range (25, 180):

    duty = float(angle) / 10 + 2.5
    print duty

    p.ChangeDutyCycle(duty)
    time.sleep(0.002)
