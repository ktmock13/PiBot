#https://www.youtube.com/watch?v=uUn0KWwwkq8

import RPi.GPIO as GPIO
import time

#set mode for pin numbering
GPIO.setmode(GPIO.BOARD)

#setup channel 7,11 for output, constants

pulse_output_pin = 7
button_output_pin = 11
GPIO.setup(pulse_output_pin, GPIO.OUT)
GPIO.setup(button_output_pin, GPIO.OUT)

#input pin on 13, set this as input, use pull down resistor on this pin
button_input_pin = 13
GPIO.setup(button_input_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#rather than setting the pin (hi/lo), instead create and instance 'pulse'
#to modulate @ 50hz (or 60hz), high enough to not see blinking
hz = 60
pulse = GPIO.PWM(pulse_output_pin,hz)


#start the instance of 'pulse', param is duty cycle, or, how often (% of time) the pin is high
#start instance at cycle of 0, or off
pulse.start(0)

#constants for main execution (modulation)
pace = 0.02
cycles = 50

#this block give us a safe way to end program with key input (ctrl+c)
try:
    while True:
        for i in range(cycles):
            #change duty cycle (brightness) of p
            pulse.ChangeDutyCycle(i)
            #set 7 to whatever 13 is (hi/lo)
            GPIO.output(button_output_pin, GPIO.input(button_input_pin))
            #pace this for loop
            time.sleep(pace)
        for i in range(cycles):
            #change duty cycle (brightness) of p
            pulse.ChangeDutyCycle(cycles-i)
            #set 7 to whatever 13 is (hi/lo)
            GPIO.output(button_output_pin, GPIO.input(button_input_pin))
            #pace this for loop
            time.sleep(pace)
except KeyboardInterrupt:
    pass

p.stop()

GPIO.cleanup()
