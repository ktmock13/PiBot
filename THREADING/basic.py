import time
import threading
from threading import Thread

def printForever(word):
    while True:
        print word
        timesleep(1)

Thread(target = printForever, args=("HI",)).start()
time.sleep(0.5)
Thread(target = printForever, args=("HO",)).start()
