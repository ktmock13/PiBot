import RPi.GPIO as GPIO

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

sequences = [half, twophasefull, onephasefull]


def spinClockwise():
    for i in range(2):
        for halfstep in range(4):
            for pin in range(4):
                GPIO.output(ControlPin[pin], twophasefull[halfstep][pin])
            time.sleep(0.002)

def spinCounterClockwise():
    for i in range(2):
        for halfstep in reversed(range(4)):
            for pin in range(4):
                GPIO.output(ControlPin[pin], twophasefull[halfstep][pin])
            time.sleep(0.002)


def on_press(key):
    if key == keyboard.Key.right:

        spinClockwise()

    else:
        spinCounterClockwise()

def on_release(key):
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


GPIO.cleanup()
