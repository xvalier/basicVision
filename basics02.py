#This application does the following (in script form):
    #Get dims, split/merge channels, get/set pixels in image
    #Image addition and Blending
    #Putting logo on another image via bitwise masking
    #Timers to clock CV performance
    #Zero-padding/borders

import os
import cv2
import numpy as np
from matplotlib import pyplot as plot

#Choose test image based on path
file = 'Receipt.jpg'
path = os.getcwd() + '/images/'
name = path + file
#Parameters
scaleFactor = .25
windowName  = 'ImageWindow'
controlName = 'Controls'


image = cv2.imread(name, 1)

#Get dimensions
dim   = image.shape
#Get value of pixel at specified location
x = 100
y = 200
channel = 2
pixelLocation = (x,y,channel)
value = image.item(pixelLocation)
#Set pixel value at specified location
newValue = int(value/10)
image.item((pixelLocation), newValue)

#Split and merge channels (can use to change BGR to RGB)
b,g,r = cv2.split(image)
newImage = cv2.merge((r,g,b))

#Add 10px border (Border/Zero Padding) to aid in convolution
paddedImage = cv2.copyMakeBorder(image, 10,10,10,10, cv2.BORDER_REPLICATE)

#Image Addition/Subtraction
path = os.getcwd() + '/images/'
file1 = 'Receipt.jpg'
file2 = 'n64.png'
image1 = cv2.imread(path+file1, 1)
image2 = cv2.imread(path+file2, 1)
addedImages = cv2.add(image1,image2)

#Image Blending
weight1 = .7
weight2 = .3
blendedImages = cv2.addWeighed(image1, weight1, image2, weight2)

#Image Masking (Put N64 Logo on Receipt)
receipt = image1
n64     = image2
#Create ROI on receipt image to put n64 logo on
rows, cols, channels = n64.shape
roi = receipt[0:rows, 0:cols]
# Now create a mask of logo and create its inverse mask also
#Create mask (and inverse mask) of logo
grayN64  = cv2.cvtColor(n64,cv2.COLOR_BGR2GRAY)
ret, maskN64 = cv2.threshold(grayN64, 10, 255, cv2.THRESH_BINARY)
maskINVN64   = cv2.bitwise_not(maskn64)
#Cut out sections of ROI that logo will go on using inverse MASK (keep only background)
backgroundROI       = cv2.bitwise_and(roi,roi,mask = mask_inv)
#Take only object from logo image (keep only foreground)
logo                = cv2.bitwise_and(n64,n64,mask = mask)
#Combine ROI background with logo, add to original receipt image
combo = cv2.add(backgroundROI,logo)
receipt[0:rows, 0:cols ] = combo
cv2.imshow('Window',receipt)
cv2.waitKey(0)
cv2.destroyAllWindows()

#-----------------------------------------------
#Object that tracks openCV time performance
class timeCV:
    def __init__(self):
        self.time  = 0
        self.start = 0
    start = 0
    time  = 0

    def start():
        self.reset()
        self.start = cv2.getTickCount()

    def stop():
        stop = cv2.getTickCount()
        self.time = (stop-self.start)/cv2.getTickFrequency()

    def reset():
        self.start = 0
        self.time  = 0

    def getTime():
        return self.time
#Example Usage:
#timeCV.start()
#**put code here
#timeCV.stop()
#performance = timeCV.getTime()
#--------------------------------------------
