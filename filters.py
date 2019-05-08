import os
import cv2
import numpy as np
import math
from math import cos, sin

#Choose test image based on path
file = 'Receipt.jpg'
path = os.getcwd() + '/images/'
name = path + file
#Parameters
scaleFactor = .25
windowName  = 'ImageWindow'
controlName = 'Controls'

original = imageResize(cv2.imread(name, 1), scaleFactor)

#Create any spatial filter using the following format
kernel = np.array([1,2,1],[0,0,0],[-1,-2,-1]])  #Example sobel kernel
filteredImage = cv2.filter2D(original, -1, kernel)

#LOW PASS FILTERS (for smoothing and noise removal)-----------------------------
#Smooth image using average filter
kernelSize = 5
blurredImage = cv.blur(original, (kernelSize, kernelSize))

#Use Gaussian Filter to remove gaussian noise and also smooth
kernelSize = 5
stdDeviation = 2
filteredImage = cv.GaussianBlur(original, (kernelSize, kernelSize), stdDeviation)

#Use Median Filter to remove salt and pepper noise
kernelSize = 5      #Must always be odd num and greater than 3
filteredImage = cv.medianBlur(original, kernelSize)

#Use Bilaterial filter if you want to remove noise without blurring (it is slower though)
kernelSize = 5
colorVariance = 75  #This means that only pixels of similar color/intensity are considered
spaceVariance = 75
filteredImage = cv.bilaterialBlur(original, kernelSize, colorVariance, spaceVariance)

#HIGH PASS FILTERS (for gradients and edge detection)---------------------------
#Sobel Filter is a combination of gaussian and 1st derivative. It is more resistant to noise
kernelSize = 5
sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=kernelSize)
sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=kernelSize)

#Scharr Filter is simply a 1st derivative. It is more precise, but more sensitive
kernelSize = 5
scharrx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=kernelSize)
scharry = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=kernelSize)

#Laplacian Filter is a sum of 2nd derivatives in X and Y direction
laplacian = cv2.Laplacian(original,cv2.CV_64F)


#FOURIER TRANSFORMS-------------------------------------------------------------
#CONCEPT
#If a 'signal' varies in amplitude (intensity) a lot, it is high frequency
#If a 'signal' varies slowly or not much, it is low frequency
#For images, noises and edges are 'high frequency'
#The general 'outline' is low frequency
#Should have array size of 2s,3s,or 5s. Zeropad to get this in OpenCV

#Found optimal array size to compute DFT efficiently
rows, cols = original.shape[0:2]
optimalRows = cv2.getOptimalDFTSize(rows)
optimalCols = cv2.getOptimalDFTSize(cols)
#ZeroPad the image to make it the optimal array size
horizPad = optimalCols - cols
vertPad   = optimalRows - rows
paddedImage   = cv2.copyMakeBorder(original, 0, vertPad, 0, horizPad,cv2.BORDER_CONSTANT, value = 0)
#Perform 2D DFT on padded image
spectrum = cv2.dft(np.float32(paddedImage),flags = cv2.DFT_COMPLEX_OUTPUT)
#Shift spectrum so that low freq portions are in center of image
shiftedSpectrum = np.fft.fftshift(spectrum)
#Create a simple high pass filter in frequency domain
originX,originY = rows/2 , cols/2
filt = np.zeros((rows,cols,2),np.uint8)
filt[originX-30:originX+30, originY-30:originY+30] = 1
#Apply filter, then shift it back to 'normal position'
filteredSpectrum = shiftedSpectrum*filt
filteredSpectrum = np.fft.ifftshift(filteredSpectrum)
#Perform 2D inverse DFT
filteredImage = cv2.idft(filteredSpectrum)
