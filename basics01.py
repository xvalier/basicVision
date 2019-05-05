#This application does the following:
    #Imports an image from designated path
    #Resizes image based on a scaleFactor
    #Displays image using openCV imshow
    #Creates a controlBox with RGB sliders
    #Refreshs image with disabled/enabled color channels based on sliders
    #Destroys windows/saves images to path based on keystrokes

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

#Continually refresh image in window
def main(name):
    #Import image and then resize based on scale factor
    image = cv2.imread(name, 1)
    height = int(image.shape[0] * scaleFactor)
    width  = int(image.shape[1] * scaleFactor)
    resizedImage = cv2.resize(image, (height, width))
    #Create window to display image
    cv2.namedWindow(windowName)
    #Create controlBox with BGR sliders
    def nothing(x):
        pass
    cv2.namedWindow(controlName)
    cv2.createTrackbar('Red', controlName,1,1,nothing)
    cv2.createTrackbar('Blue', controlName,1,1,nothing)
    cv2.createTrackbar('Green', controlName,1,1,nothing)
    cv2.imshow(controlName, np.zeros((100,100,1), np.uint8))
    while(1):
        #Use controlBox to choose color channels that are output
        switches = {}
        switches['Blue'] = cv2.getTrackbarPos('Blue', controlName)
        switches['Green'] = cv2.getTrackbarPos('Green', controlName)
        switches['Red'] = cv2.getTrackbarPos('Red', controlName)
        #Display image channels based on sliders
        image    = colorChannels(resizedImage, switches)
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

#Enable/disable color channels based on sliders
def colorChannels(image, switches):
    newImage = np.copy(image)
    if switches['Blue'] == 0:
        newImage[:,:,0] = 0
    if switches['Green'] == 0:
        newImage[:,:,1] = 0
    if switches['Red'] == 0:
        newImage[:,:,2] = 0
    return newImage
