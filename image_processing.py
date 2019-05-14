import numpy as np
import cv2
from skimage import io, color
from matplotlib import pyplot as plt
import numpy as np

URL = 'http://10.134.97.49:5000/camera/last_frame'

image_bgr = io.imread(URL)

image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)

# rouge-orange
lower_orange = np.array([100, 100, 100])  #RGB ???? (fait par tatonement)
upper_orange = np.array([130, 255, 255])

mask = cv2.inRange(image_hsv, lower_orange, upper_orange)

io.imshow(mask)
#io.imshow(image_bgr)

plt.show()


