
#This application uses code from basic01. New things it does:
    #ControlBox with threshold parameters
    #Shows before, after for thresholding functions
    #Simple/Adaptive/OSTU Thresholding is implemented

import os
import cv2
import numpy as np
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
    #Create windows for image display and controls
    cv2.namedWindow(windowName)
    sliders = createTransformationControl(controlName)
    while(1):
        #Use controlBox to choose color channels that are output
        parameters = getTransformationControl(controlName, sliders)
        modified = transformationProcess(original, parameters)
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
def createTransformationControl(controlName):
    def nothing(x):
        pass
    cv2.namedWindow(controlName)
    cv2.createTrackbar('ScalingX', controlName, 0,255,nothing)
    cv2.createTrackbar('ScalingY', controlName, 0,255,nothing)
    cv2.createTrackbar('TranslationX', controlName,0,2000,nothing)
    cv2.createTrackbar('TranslationY', controlName,0,2000,nothing)
    cv2.createTrackbar('Rotation', controlName,0,360,nothing)
    cv2.createTrackbar('ShearX', controlName,0,2000,nothing)
    cv2.createTrackbar('ShearY', controlName,0,2000,nothing)
    cv2.imshow(controlName, np.zeros((100,700,1), np.uint8))
    sliders = ['ScalingX','ScalingY', 'TranslationX',
        'TranslationY', 'Rotation', 'ShearX', 'ShearY']
    return sliders

#Get values from all sliders on GUI controlBox
def getTransformationControl(controlName, sliders):
    parameters = {}
    for n in sliders:
        value = cv2.getTrackbarPos(n, controlName)
        parameters[n] = value
    return parameters

#TODO:Find how to put all values in 2x3 M matrix
#TODO:Only rotation working now
#TODO:Rotation is not centered at origin
#
def transformationProcess(image, parameters):
    newImage = np.copy(image)
    #Extract scaling Parameters
    sx = max(parameters['ScalingX'],1)
    sy = max(parameters['ScalingY'],1)
    tx = parameters['TranslationX']
    ty = parameters['TranslationY']
    r  = parameters['Rotation']
    shx = parameters['ShearX']
    shy = parameters['ShearY']
    #Create transformation matrix
    M  = np.float32([[sx, shx, tx], [sy,shy, ty]])
    #Rotation matrix needs special function to scale
    cols= newImage.shape[0]
    rows= newImage.shape[1]
    Mr = cv2.getRotationMatrix2D((cols,rows), r, 1)
    #Combine all transformations via scalar multiplication
    M  = np.multiply(Mr, M)
    newImage = cv2.warpAffine(newImage, M, (rows, cols))
    return newImage
