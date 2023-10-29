from gpiozero import LED
from time import sleep

led = LED(21)

while True:
    led.off()
    sleep(.1)
    led.on()
    sleep(1)
