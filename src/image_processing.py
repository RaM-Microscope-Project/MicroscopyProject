import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

imgR = cv.imread('/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/SP_test/L.jpg', cv.IMREAD_GRAYSCALE)
imgL = cv.imread('/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/SP_test/R.jpg', cv.IMREAD_GRAYSCALE)

stereo = cv.StereoBM_create(numDisparities=64, blockSize=5)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
