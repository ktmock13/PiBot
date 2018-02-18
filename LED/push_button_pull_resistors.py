#https://www.youtube.com/watch?v=Bqk6M_XdIC0&feature=youtu.be&t=1m39s

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

#input pin on 11, set this as input, use pull down resistor on this pin
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#setup output pin on 7,
GPIO.setup(7, GPIO.OUT)

#start off
GPIO.output(7,0)

#user press ctrl+c exits
try:
    while True:
        #output on 7, whatever the input is at on 11
        GPIO.output(7, GPIO.input(13))
        ###
except KeyboardInterrupt:
    GPIO.cleanup()
