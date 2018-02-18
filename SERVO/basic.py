import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

servo_output_pin = 29

GPIO.setup(servo_output_pin, GPIO.OUT)

servo_pulse = GPIO.PWM(servo_output_pin,50)
servo_pulse.start(7.5)

try:
    while True:
        servo_pulse.ChangeDutyCycle(12.5)
        time.sleep(2)
        servo_pulse.ChangeDutyCycle(2.5)
        time.sleep(2)

except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
