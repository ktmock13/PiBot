# Import required libraries
import time
from gpiozero import OutputDevice as stepper

IN1 = stepper(23)
IN2 = stepper(18)
IN3 = stepper(15)
IN4 = stepper(14)
StepPins = [IN1, IN2, IN3, IN4]

# Define sequence
# as shown in manufacturers datasheet
Seq = [[1, 0, 0, 1],
       [1, 0, 0, 0],
       [1, 1, 0, 0],
       [0, 1, 0, 0],
       [0, 1, 1, 0],
       [0, 0, 1, 0],
       [0, 0, 1, 1],
       [0, 0, 0, 1]]

StepCount = len(Seq)
StepDir = -1
WaitTime = 0.5
StepCounter = 0

while True:

    print(StepCounter)
    print(Seq[StepCounter])
    for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin] != 0:
            xpin.on()
        else:
            xpin.off()

    StepCounter += StepDir
    # If we reach the end of the sequence
    # start again
    if (StepCounter >= StepCount):
        StepCounter = 0
    if (StepCounter < 0):
        StepCounter = StepCount+StepDir
    # Wait before moving on
    time.sleep(WaitTime)
