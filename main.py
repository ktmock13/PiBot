from robot import Robot
import signal
import sys

if __name__ == '__main__':

    dick = Robot()

    def dont_explode(signal, frame):
        print("NOT EXPLODING, goodbye")
        dick.kill()
        sys.exit(0)

    signal.signal(signal.SIGINT, dont_explode)

    dick.run()
