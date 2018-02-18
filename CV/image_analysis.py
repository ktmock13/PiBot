#https://www.youtube.com/watch?v=Z78zbnLlPUA&index=1&list=PLQVvvaa0QuDdttJXlLtAJxJetJcqmqlQq

#!/home/pi/.virtualenvs/CV/bin/python

import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('pupper.jpg', cv2.IMREAD_GRAYSCALE)
