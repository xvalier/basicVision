import os
import cv2
import numpy as np
from matplotlib import pyplot as plot

#Choose test image
path = os.getcwd() + '/images/'
file = 'Receipt.jpg'
name = path + file

#Import image
image = cv2.imread(name, 1) #Import image in grayscale

#General display
cv2.namedWindow('Window-1',cv2.WINDOW_NORMAL)
cv2.imshow('Window-1',image)
k = cv2.waitKey(0) & 0xFF
if k == 27:                                     #Quit if ESC is pressed
    cv2.destroyAllWindows()
elif k == ord('s'):                             #Save and quit if 's' is pressed
    cv2.imwrite(path+file+'01',image)
    cv2.destroyAllWindows()

#Display through matplotlib
plot.imshow(image, cmap = 'gray', interpolation = 'bicubic')
plot.xticks([]), plot.yticks([])                  #Hide ticks
plot.show()

#APPLICATION----------------use sliders to change image contents
import os
import cv2
import numpy as np
from matplotlib import pyplot as plot

#Choose test image
path = os.getcwd() + '/images/'
file = 'Receipt.jpg'
name = path + file
scaleFactor = .25
windowName = 'Window-2'

image = cv2.imread(name, 1) #Import image in grayscale
def nothing(x):
    pass
cv2.namedWindow(windowName,cv2.WINDOW_NORMAL)
cv2.createTrackbar('R',windowName,0,255,nothing)
cv2.createTrackbar('G',windowName,0,255,nothing)
cv2.createTrackbar('B',windowName,0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, windowName,0,1,nothing)

while(1):
    height = floor(image.shape[0] * scaleFactor)
    width = floor(image.shape[0] * scaleFactor)
    resizedImage = cv2.resize(image, (height, width))
    cv2.imshow(windowName,image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R',windowName)
    g = cv2.getTrackbarPos('G',windowName)
    b = cv2.getTrackbarPos('B',windowName)
    s = cv2.getTrackbarPos(switch,windowName)
    if s == 0:
        image[:] = 0
    else:
        image[:] = [b,g,r]

cv2.destroyAllWindows()






#Steps to take
#1) Receipt Orientation and Extraction
#2) Blob Detection via 'Morphological Close' + Threshold
    #Find edges of receipt (via Edge Detection on BLOB)
    #Calculate angle
    #ROI Extraction of ORIGINAL Receipt
    #Linear Rotation Transformation of ORIGINAL receipt
#3) OTSU Thresholding (Binarization)
#4) OCR Recognition (maybe using Tessaract)
#5) Extraction of OCR Strings (which are readable)




tl = 50
th = 150
choice =0




def main(path, tl, th, choice):
    a = getImages(path)
    b = readImageGrayScale(a[choice])
    c = extractReceipt(b)

#Get list of all images in a given directory
def getImages(path):
    if not os.path.exists(path):
        path = input('Please specify location where images are stored: ')
    return [path+item for item in os.listdir(path)]

#Read image from specified path as a numpy array
def readImageGrayScale(file):
    return cv2.imread(file, 0)

#Display an image, fitted in window
def displayImage(imageMatrix):
    cv2.namedWindow("Display",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Display",600,600)
    cv2.imshow("Display",imageMatrix)
    cv2.waitKey(0)
    cv2.destoryAllWindows()

#Find receipt object from background and extract it
def extractReceipt(rawImage):






#Un-used snippets---------------------------------------------------------------
def readImageColor(file):
    return cv2.imread(file)

def splitColorChannel(image):
    return cv2.split(image)

#Canny Edge Detector
def edgeDetectCanny(image, thresholdLow, thresholdHigh):
    edges = cv2.Canny(image, thresholdLow, thresholdHigh)
    return edges

#Write image array to specified file
def writeImage(path,name, image):
    cv2.imwrite(path+name, image)
