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

#CANNY EDGE DETECTION-----------------------------------------------------------
#Procedure for this is below:
#1) 5x5 Gaussian Filter to remove noise
#2) Get 1st Derivatives Gx and Gy
#3) Obtain Magnitude M = sqrt(Gx^2 +Gy^2) and Angle theta = atan(Gx/Gy)
#4) Nonminima Suppression -> keep only maxima/peaks
#5) Hysterisis Threshold, user selects thresholds tHigh and tLow
    #if above tHigh -> edge
    #if below tLow  -> not edge
    #if between tHigh and tLow -> edge only if near other edge points
tLow  = 100
tHigh = 200
processedImage = cv2.Canny(original,tLow,tHigh)
