#https://www.youtube.com/watch?v=uUn0KWwwkq8

import RPi.GPIO as GPIO
import time

#set mode for pin numbering
GPIO.setmode(GPIO.BOARD)

#setup channel 7 for output
GPIO.setup(7, GPIO.OUT)


#rather than setting the pin (hi/lo), instead create and instance 'p'
#modulate @ 50hz, high enough to not see blinking
p = GPIO.PWM(7,120)


#start the instance of 'p', param is duty cycle, or, how often (% of time) the pin is high
#start instance at cycle of 0, or off
p.start(1)

#constants for main execution (modulation)
pace = 0.02
cycles = 25

#this block give us a safe way to end program with key input (ctrl+c)
try:
    while True:
        for i in range(cycles):
            #change duty cycle (brightness) of p
            p.ChangeDutyCycle(i)
            #pace this for loop
            time.sleep(pace)
        for i in range(cycles):
            #change duty cycle (brightness) of p
            p.ChangeDutyCycle(25-i)
            #pace this for loop
            time.sleep(pace)
except KeyboardInterrupt:
    pass

p.stop()

GPIO.cleanup()
