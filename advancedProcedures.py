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


#CONTOUR DETECTION AND DISPLAY--------------------------------------------------
#Contours are object boundaries (perimeters of a blob)
#Below is similar to boundary following algorithm
    #4th argument in findContours is approx method, which is like polyfitting (compressing # of points)
    #contours output is a list of contours. Each contour is a list of x,y boundary points
#Before finding contours, it is necessary to get a grayscale binary image (only black and white)
grayscaleImage = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
ret,binaryImage = cv2.threshold(grayscaleImage,127,255,0)
image, contours, hierarchy = cv2.findContours(binaryImage,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#Draw all contours on image
newImage = cv2.drawContours(image, contours, -1, (0,255,0), 3)
#Draw a specific contour on image based on index
newImage = cv2.drawContours(image, contours, 3, (0,255,0), 3)
#After detecting contour, extract properties for each (blob parameters)
contour = contours[3]
cnt = contours[0]
M = cv2.moments(cnt)
print M
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
area = cv2.contourArea(cnt)
perimeter = cv2.arcLength(cnt,True)
