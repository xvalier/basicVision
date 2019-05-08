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

#HISTOGRAMS---------------------------------------------------------------------
#Histograms are graphs showing intensity distributions for pixels
#You can even graph color via three different lines (one for each channel)
#calcHist(iamge, numChannels, mask, numBins, intensityRange)
#bins = instead of 1 value per pixel, can do intervals
#mask = looking at a specific part of image, if none you use entire image

#For 1D Histogram, use a grayscal Image
grayImage = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
histogram = cv2.calcHist([grayImage],[0],None,[256],[0,256])
mask = np.zeros(original.shape[:2], np.uint8)
mask[100:300, 100:400] = 255
maskedHistogram = cv2.calcHist([grayImage],[0],mask,[256],[0,256])

#Easiest way to plot histogram is using matplotlib. Below is color example
color = ('b','g','r')
for i,col in enumerate(color):
    plt.plot(histogram,color = col)
    plt.xlim([0,256])
plt.show()

#If histogram has values concentrated in specific range, you can 'stretch out the histogram'
#This is called Histogram Equalization, and it improves contrast for overly bright or dark images
equalizedImage = cv2.equalizeHist(grayImage)

#Histogram Equalization only helps for global contrasts.
#It doesn't work well for situations for lighting varies between dark and light areas
#To resolve this, use CLAHE (Contrast Limited Adaptive Histogram Equalization)
#CLAHE Procedure:
    #1 -- Image is divided into blocks of user specified size
    #2 -- Histogram taken for each block
    #3 -- Contrast limiting done if noise is above clip limit
    #4 -- Edge artifacts (due to diff equalization) are removed via bilinear interpolation
blockSize = 8
clipLimit = 2.0
clahe = cv2.createCLAHE(clipLimit=clipLimit, tileGridSize=(blockSize,blockSize))
equalizedImage = clahe.apply(grayImage)

#Perform 2D Histogram on HSV Color Images
#Channels = 0 for hue, 1 for Sat. Bins = 180 for hue, 256 for Sat
#Range = 0 to 180 for hue and 0 to 256 for sat
hsvImage = cv2.cvtColor(original,cv2.COLOR_BGR2HSV)
hist = cv2.calcHist([hsvImage], [0, 1], None, [180, 256], [0, 180, 0, 256])
#Use imshow() to display 2D Histogram
#Might be better to use matplotlib to customize and colorize each 'line'

#Histogram Backprojection outputs a 'heatmap' for probability that a pixel belongs to desired object
#It outputs a 2D image with 1 channel (0s and 255s), and is generally better with a color image
#USE THIS IN GENERAL TO MAKE HEATMAPS
#Procedure to do this is below:
    #1) Obtain a color (HSV) template of object to look for (try to only have object in template)
    #2) Calculate 2D Histogram for object template
    #3) For a new image (that could have object), calculate 2D histogram
    #4) R = M/I , where M = object hist and I = image histogram
    #5) Create heatmap B with each pixel representing its probability
    #6) Apply B = min(B,1) so that 1 is maximum value
    #7) Apply convolution with disc kernel --> B = B * D, where D= disc kernel
    #8) Threshold heatmap B to detect object if it exists

#For openCV, a lot of this is simplified
#Get object template and image
template = cv2.imread('object.png') #examples, don't have actual images
target   = cv2.imread('image.png')
#Convert to HSV images
hsvTemplate = cv2.cvtColor(template,cv2.COLOR_BGR2HSV)
hsvTarget   = cv2.cvtColor(target,cv2.COLOR_BGR2HSV)
#Find 2D Histogram for Object, then normalize it
histOBJ = cv2.calcHist([hsvTemplate],[0, 1], None, [180, 256], [0, 180, 0, 256] )
cv2.normalize(histOBJ,histOBJ,0,255,cv2.NORM_MINMAX)
#Apply BackProjection (Steps 4,5,6)
heatmap = cv2.calcBackProject([hsvTarget],[0,1],histOBJ,[0,180,0,256],1)
#Apply disc kernel convolution
disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
cv2.filter2D(heatmap,-1,disc,heatmap)
#Apply threshold
ret,detectMap = cv2.threshold(heatmap,50,255,0)
