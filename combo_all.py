
import RPi.GPIO as GPIO
import time
import threading
from threading import Thread

#set mode for pin numbering
GPIO.setmode(GPIO.BOARD)

#setup channel 7,11 for output, constants

stepper_output_pins = [16,18,22,32]
for pin in stepper_output_pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin,0)


#input pin on 13 & 36 set  as input, use pull down resistor on this pin to elimate floating value
button_input_pin1 = 13
GPIO.setup(button_input_pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
button_input_pin2 = 36
GPIO.setup(button_input_pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#input pin on 13 & 36 set  as input, use pull down resistor on this pin to elimate floating value
button_input_pin2 = 36
GPIO.setup(button_input_pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#rather than setting the pin (hi/lo), instead create and instance 'pulse'
#to modulate @ 50hz (or 60hz), high enough to not see blinking
hz = 60
pulse = GPIO.PWM(pulse_output_pin,hz)


#setup servo
servo_output_pin = 29

GPIO.setup(servo_output_pin, GPIO.OUT)

servo_pulse = GPIO.PWM(servo_output_pin,50)
servo_pulse.start(7.5)

#start the instance of 'pulse', param is duty cycle, or, how often (% of time) the pin is high
#start instance at cycle of 0, or off
pulse.start(0)

#constants for main execution (modulation)
pace = 0.02
cycles = 40

#stepper sequences

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

#this block give us a safe way to end program with key input (ctrl+c)
def lights():
    try:
        #cycle one LED from dim to bright and check for button press on other LED
        while True:
            for i in range(cycles):
                #change duty cycle (brightness) of p
                pulse.ChangeDutyCycle(i)
                #set 7 to whatever 13 is (hi/lo)
                GPIO.output(button1_output_pin, GPIO.input(button_input_pin1))
                GPIO.output(button2_output_pin, GPIO.input(button_input_pin2))

                #pace this for loop
                time.sleep(pace)
            for i in range(cycles):
                #change duty cycle (brightness) of p
                pulse.ChangeDutyCycle(cycles-i)
                #set 7 to whatever 13 is (hi/lo)
                GPIO.output(button1_output_pin, GPIO.input(button_input_pin1))
                GPIO.output(button2_output_pin, GPIO.input(button_input_pin2))

                #pace this for loop
                time.sleep(pace)
    except KeyboardInterrupt:
        pulse.stop()
        GPIO.cleanup()
        pass

def stepper():
    try:
        while True:
            if GPIO.input(button_input_pin2):
                for halfstep in range(4):
                    for pin in range(4):
                            GPIO.output(stepper_output_pins[pin], twophasefull[halfstep][pin])
                    time.sleep(0.002)
            if GPIO.input(button_input_pin1):
                for halfstep in reversed(range(4)):
                    for pin in range(4):
                            GPIO.output(stepper_output_pins[pin], twophasefull[halfstep][pin])
                    time.sleep(0.002)

    except KeyboardInterrupt:
        GPIO.cleanup()
        pass

def servo():
    try:
        while True:
            servo_pulse.ChangeDutyCycle(7.5)
            time.sleep(.25)
            servo_pulse.ChangeDutyCycle(12.5)
            time.sleep(.25)
            servo_pulse.ChangeDutyCycle(2.5)
            time.sleep(.25)

    except KeyboardInterrupt:
        p.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    Thread(target = lights).start()
    Thread(target = stepper).start()
    # Thread(target = servo).start()
