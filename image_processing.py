import numpy as np
import cv2
from skimage import io, color
from matplotlib import pyplot as plt
import numpy as np

URL = 'http://10.134.97.49:5000/camera/last_frame'

image_bgr = io.imread(URL)
image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_RGB2HSV)
io.imshow(image_hsv)
plt.show()


