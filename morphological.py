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

#NOTE: Another name for pixel neighborhoods are structuring elements/ kernels
#Usually kernel size is just 3x3 (only immediate neighbors), but you can increase it

#Erosion --> Pixel is only '1' if all images inside kernel is 1
#Has effect of removing 1s (if white on black) and making everything thinner
kernel = np.ones((3,3),np.uint8)
processedImage = cv2.erode(original,kernel,iterations = 1)

#Dilation --> Pixel is one if at least one pixel in kernel is 1
#has effect of making everything 'bold'
kernel = np.ones((3,3),np.uint8)
processedImage  = cv2.dilate(original,kernel,iterations = 1)

#Opening --> eroding then dilating. Useful for removing noise outside object
kernel = np.ones((3,3),np.uint8)
processedImage  = cv2.morphologyEx(original, cv2.MORPH_OPEN, kernel)

#Closing --> dilating then eroding. useful for 'filling in' object
kernel = np.ones((3,3),np.uint8)
processedImage  = cv2.morphologyEx(original, cv2.MORPH_CLOSE, kernel)

#Morphological Gradient --> Difference between dilate and erode
#Useful for getting outline of object
kernel = np.ones((3,3),np.uint8)
processedImage  = cv2.morphologyEx(original, cv2.MORPH_GRADIENT, kernel)

#Top Hat --> Difference between Input image and closing image
kernel = np.ones((3,3),np.uint8)
processedImage  = cv2.morphologyEx(original, cv2.MORPH_TOPHAT, kernel)

#Black hat --> Difference between input and opening image
kernel = np.ones((3,3),np.uint8)
processedImage  = cv2.morphologyEx(original, cv2.MORPH_BLACKHAT, kernel)
