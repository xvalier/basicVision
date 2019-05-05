#APPLICATION----------------use sliders to change image contents
import os
import cv2
import numpy as np
from matplotlib import pyplot as plot

#Choose test image based on path
path = os.getcwd() + '/images/'
file = 'Receipt.jpg'
name = path + file

#Other Parameters
scaleFactor = .25
windowName  = 'Window-3'
controlName = 'Controls'

#Import image and then resize based on scale factor
image = cv2.imread(name, 1)
height = int(image.shape[0] * scaleFactor)
width  = int(image.shape[1] * scaleFactor)
resizedImage = cv2.resize(image, (height, width))
#Create window to display image
cv2.namedWindow(windowName)#,cv2.WINDOW_NORMAL)

#Sliders for color channels
def nothing(x):
    pass
#cv2.createTrackbar('R',windowName,0,255,nothing)
#cv2.createTrackbar('G',windowName,0,255,nothing)
#cv2.createTrackbar('B',windowName,0,255,nothing)

#Switch for grayscale vs color
cv2.namedWindow(controlName)
cv2.createTrackbar('Red', controlName,0,1,nothing)
cv2.createTrackbar('Blue', controlName,0,1,nothing)
cv2.createTrackbar('Green', controlName,0,1,nothing)

#Continually refresh image in window
while(1):
    #Use controlBox to choose color channels that are output
    cv2.imshow(controlName, np.zeros((100,100,1), np.uint8))
    switches = {}
    switches['Blue'] = cv2.getTrackbarPos('OnlyBlue', controlName)
    switches['Green'] = cv2.getTrackbarPos('OnlyGreen', controlName)
    switches['Red'] = cv2.getTrackbarPos('OnlyRed', controlName)
    image    = colorChannels(resizedImage, switches)
    cv2.imshow(windowName,image)
    #Controls to close window and save image based on key strokes
    k = cv2.waitKey(1) & 0xFF
    if k == 27:            #Quit if ESC is pressed
        cv2.destroyAllWindows()
        break
    elif k == ord('s'):   #Save and quit if 's' is pressed
        cv2.imwrite(path+file+'01',image)

def colorChannels(image, switches):
    if switches['Blue'] == 0:
        image[:,:,0] = 0
    if switches['Green'] == 0:
        image[:,:,1] = 0
    if switches['Red'] == 0:
        image[:,:,2] = 0
    return image





#-----------------------------------------------------------------
#Display through matplotlib
plot.imshow(image, cmap = 'gray', interpolation = 'bicubic')
plot.xticks([]), plot.yticks([])                  #Hide ticks
plot.show()


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
