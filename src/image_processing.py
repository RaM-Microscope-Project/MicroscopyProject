import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

#this was an experiment to extract a depthmap from stereo photography scans
#the result was very noisy but I included it in case anyone can figure out how to fix it (:

imgR = cv.imread('/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/SP_test/L.jpg', cv.IMREAD_GRAYSCALE)
imgL = cv.imread('/home/xxpepxx/Desktop/GitProject/MicroscopyProject/src/captures/SP_test/R.jpg', cv.IMREAD_GRAYSCALE)

stereo = cv.StereoBM_create(numDisparities=64, blockSize=5)
disparity = stereo.compute(imgL,imgR)
plt.imshow(disparity,'gray')
plt.show()
