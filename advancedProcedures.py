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
