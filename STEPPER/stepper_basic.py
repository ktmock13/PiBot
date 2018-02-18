import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

ControlPin = [16,18,22,32]

button_input_pin = 13
GPIO.setup(button_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

for pin in ControlPin:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)

half = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1] ]

twophasefull = [ [1,0,0,1],
        [1,1,0,0],
        [0,1,1,0],
        [0,0,1,1] ]

onephasefull = [ [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [0,0,0,1] ]

while True:
    if GPIO.input(button_input_pin):
        for halfstep in range(4):
            for pin in range(4):
                    GPIO.output(ControlPin[pin], twophasefull[halfstep][pin])
            time.sleep(0.002)

GPIO.cleanup()
