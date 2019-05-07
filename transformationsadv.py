#This application uses code from basic01. New things it does:
    #In future, make this a 'mouse event'
    #Advanced Perspective/Affine Transformations using selected INs
    #Function doesn't work now, perform later

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

#Continually refresh image in window
def main(name):
    #Import image and then resize based on scale factor
    original = imageResize(cv2.imread(name, 1), scaleFactor)
    rows = original.shape[0]
    cols = original.shape[1]
    #Create windows for image display and controls
    cv2.namedWindow(windowName)
    sliders = createTransformationControl(controlName, cols, rows)
    while(1):
        #Use controlBox to choose color channels that are output
        parameters = getTransformationControl(controlName, sliders)
        modified = transformationProcess(original, parameters, cols, rows)
        #Combine three images for one window
        image = cv2.hconcat([original,modified])
        cv2.imshow(windowName,image)
        if(closeWindow(cv2.waitKey(1) & 0xFF, name, image)):
            break

#Resize image based on scaleFactor
def imageResize(image, scale):
    height = int(image.shape[0] * scaleFactor)
    width  = int(image.shape[1] * scaleFactor)
    resizedImage = cv2.resize(image, (height, width))
    return resizedImage

#Controls to close window and save image based on key strokes
def closeWindow(key, file, image):
    if key == 27:            #Quit if ESC is pressed
        cv2.destroyAllWindows()
        return 1
    elif key == ord('s'):   #Save and quit if 's' is pressed
        cv2.imwrite(name+'01',image)
    return 0

#Create controlBox with HSV limit sliders (create object/factory later)
#TODO:Find a way to add negatives for translation/scaling
def createTransformationControl(controlName, cols, rows):
    def nothing(x):
        pass
    cv2.namedWindow(controlName)
    #0 = Affine with 3 Points, 1= Perspective with 4 Points
    cv2.createTrackbar('Type',controlName,0,1, nothing)
    cv2.createTrackbar('IN1X',controlName,0,cols, nothing)
    cv2.createTrackbar('IN1Y',controlName,0,rows, nothing)
    cv2.createTrackbar('IN2X',controlName,0,cols, nothing)
    cv2.createTrackbar('IN2Y',controlName,0,rows, nothing)
    cv2.createTrackbar('IN3X',controlName,0,cols, nothing)
    cv2.createTrackbar('IN3Y',controlName,0,rows, nothing)
    cv2.createTrackbar('IN4X',controlName,0,cols, nothing)
    cv2.createTrackbar('IN4Y',controlName,0,rows, nothing)
    cv2.createTrackbar('OUT1X',controlName,0,cols, nothing)
    cv2.createTrackbar('OUT1Y',controlName,0,rows, nothing)
    cv2.createTrackbar('OUT2X',controlName,0,cols, nothing)
    cv2.createTrackbar('OUT2Y',controlName,0,rows, nothing)
    cv2.createTrackbar('OUT3X',controlName,0,cols, nothing)
    cv2.createTrackbar('OUT3Y',controlName,0,rows, nothing)
    cv2.createTrackbar('OUT4X',controlName,0,cols, nothing)
    cv2.createTrackbar('OUT4Y',controlName,0,rows, nothing)
    cv2.imshow(controlName, np.zeros((100,700,1), np.uint8))
    sliders = ['Type', 'IN1X', 'IN1Y', 'IN2X', 'IN2Y', 'IN3X', 'IN3Y', 'IN4X', 'IN4Y',
        'OUT1X', 'OUT1Y', 'OUT2X', 'OUT2Y', 'OUT3X', 'OUT3Y', 'OUT4X', 'OUT4Y']
    return sliders

#Get values from all sliders on GUI controlBox
def getTransformationControl(controlName, sliders):
    parameters = {}
    for n in sliders:
        value = cv2.getTrackbarPos(n, controlName)
        parameters[n] = value
    return parameters

def transformationProcess(image, parameters, cols, rows):
    newImage = np.copy(image)
    #Extract scaling Parameters
    type = parameters['Type']
    p1i = [parameters['IN1X'],parameters['IN1Y']]
    p2i = [parameters['IN2X'],parameters['IN2Y']]
    p3i = [parameters['IN3X'],parameters['IN3Y']]
    p4i = [parameters['IN4X'],parameters['IN4Y']]
    p1o = [parameters['IN1X'],parameters['IN1Y']]
    p2o = [parameters['IN2X'],parameters['IN2Y']]
    p3o = [parameters['IN3X'],parameters['IN3Y']]
    p4o = [parameters['IN4X'],parameters['IN4Y']]
    if type == 0:
        coordIN  = np.float32([p1i, p2i, p3i])
        coordOUT = np.float32([p1o, p2o, p3o])
        M = cv2.getAffineTransform(coordIN, coordOUT)
        newImage = cv2.warpAffine(newImage, M, (cols, rows))
    else:
        coordIN  = np.float32([p1i, p2i, p3i, p4i])
        coordOUT = np.float32([p1o, p2o, p3o, p4i])
        M = cv2.getPerspectiveTransform(coordIN, coordOUT)
        newImage = cv2.warpPerspective(newImage, M, (cols, rows))
    return newImage
