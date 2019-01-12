from robot import Robot
import signal
import sys
import time

if __name__ == '__main__':

    dick = Robot()

    def dont_explode(signal, frame):
        print("NOT EXPLODING, goodbye")
        dick.kill()
        time.sleep(3)
        sys.exit(0)

    signal.signal(signal.SIGINT, dont_explode)

    dick.run()
