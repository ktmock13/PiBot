from robot import Robot
import signal
import sys
import time

if __name__ == '__main__':

    dick = Robot()
    dick.run()

    def dont_explode(signal, frame):
        print("NOT EXPLODING, goodbye")
        dick.kill()
        print("waiting 5 seconds to die...")
        time.sleep(5)
        print("dying")
        sys.exit()


    signal.signal(signal.SIGINT, dont_explode)

