#This application uses code from basic01. New things it does:
    #ControlBox with min/max for HSV
    #Shows before, after, and mask images all in one window
    #Masking, BGR to HSV color conversion

import os
import cv2
import numpy as np
from matplotlib import pyplot as plot

#Choose test image based on path
file = 'Receipt.jpg'
path = os.getcwd() + '/images/'
name = path + file
#Parameters
scaleFactor = .1
windowName  = 'ImageWindow'
controlName = 'Controls'

#Continually refresh image in window
def main(name):
    #Import image and then resize based on scale factor
    image = cv2.imread(name, 1)
    height = int(image.shape[0] * scaleFactor)
    width  = int(image.shape[1] * scaleFactor)
    resizedImage = cv2.resize(image, (height, width))
    #Create window to display image
    cv2.namedWindow(windowName)
    #Create controlBox with HSV limit sliders (create object/factory later)
    def nothing(x):
        pass
    cv2.namedWindow(controlName)
    cv2.createTrackbar('Hue Min', controlName,0,255,nothing)
    cv2.createTrackbar('Hue Max', controlName,255,255,nothing)
    cv2.createTrackbar('Saturation Min', controlName,0,255,nothing)
    cv2.createTrackbar('Saturation Max', controlName,255,255,nothing)
    cv2.createTrackbar('Value Min', controlName,0,255,nothing)
    cv2.createTrackbar('Value Max', controlName,255,255,nothing)
    cv2.imshow(controlName, np.zeros((100,500,1), np.uint8))
    while(1):
        #Use controlBox to choose color channels that are output
        switches = {}
        switches['HMin'] = cv2.getTrackbarPos('Hue Min', controlName)
        switches['HMax'] = cv2.getTrackbarPos('Hue Max', controlName)
        switches['SMin'] = cv2.getTrackbarPos('Saturation Min', controlName)
        switches['SMax'] = cv2.getTrackbarPos('Saturation Max', controlName)
        switches['VMin'] = cv2.getTrackbarPos('Value Min', controlName)
        switches['VMax'] = cv2.getTrackbarPos('Value Max', controlName)
        #Display image channels based on sliders (Convert mask into 3 channel)
        original, mask, modified = maskColors(resizedImage, switches)
        mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        original
        #Combine three images for one window
        image = cv2.hconcat([original,mask,modified])
        cv2.imshow(windowName,image)
        if(closeWindow(cv2.waitKey(1) & 0xFF, name, image)):
            break

#Controls to close window and save image based on key strokes
def closeWindow(key, file, image):
    if key == 27:            #Quit if ESC is pressed
        cv2.destroyAllWindows()
        return 1
    elif key == ord('s'):   #Save and quit if 's' is pressed
        cv2.imwrite(name+'01',image)
    return 0

#Mask out all colors besides limits chosen on
def maskColors(image, s):
    #Convert image to HSV
    newImage = np.copy(image)
    newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2HSV)
    #Concantenate slider values as HSV thresholds
    lowThreshold = np.array([s['HMin'],s['SMin'],s['VMin']])
    highThreshold = np.array([s['HMax'],s['SMax'],s['VMax']])
    #Create mask based on thresholds, convolve it with image
    mask = cv2.inRange(newImage, lowThreshold, highThreshold)
    newImage = cv2.bitwise_and(newImage, newImage, mask=mask)
    #Convert from HSV back to BGR for proper showing
    newImage = cv2.cvtColor(newImage, cv2.COLOR_HSV2BGR)
    return image, mask, newImage

main(name)
