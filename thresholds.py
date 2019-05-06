
#This application uses code from basic01. New things it does:
    #ControlBox with threshold parameters
    #Shows before, after for thresholding functions
    #Simple/Adaptive/OSTU Thresholding is implemented

import os
import cv2
import numpy as np

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
    sliders = createThresholdControl(controlName)
    refresh = True
    while(1):
        #Use controlBox to choose color channels that are output
        parameters = getThresholdControl(controlName, sliders)
        modified = thresholdProcess(original, parameters)
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
def createThresholdControl(controlName):
    def nothing(x):
        pass
    cv2.namedWindow(controlName)
    cv2.createTrackbar('OverallType', controlName, 0,2,nothing)
    cv2.createTrackbar('ThresholdType', controlName,0,2,nothing)
    cv2.createTrackbar('AdaptiveMethod', controlName,0,1,nothing)
    cv2.createTrackbar('Threshold', controlName,255,255,nothing)
    cv2.createTrackbar('BlockSize', controlName,1,100,nothing)
    cv2.imshow(controlName, np.zeros((100,700,1), np.uint8))
    sliders = ['OverallType','ThresholdType', 'AdaptiveMethod', 'Threshold', 'BlockSize']
    return sliders

#Get values from all sliders on GUI controlBox
def getThresholdControl(controlName, sliders):
    parameters = {}
    for n in sliders:
        value = cv2.getTrackbarPos(n, controlName)
        parameters[n] = value
    return parameters

#Choose appropiate threshold tool based on user selection
def thresholdProcess(image, parameters):
    if parameters['OverallType'] == 0:
        modified = simpleThreshold(image, parameters)
    elif parameters['OverallType'] == 1:
        modified = adaptiveThreshold(image, parameters)
    elif parameters['OverallType'] == 2:
        modified = otsuThreshold(image, parameters)
    return modified

#Global Absolute thresholding tool
def simpleThreshold(image, parameters):
    newImage = np.copy(image)
    #Convert to grayscale
    newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    #Extract parameters.
    threshold = parameters['Threshold']
    thresholdType  = getThresholdType(parameters['ThresholdType'])
    #Perform threshold
    ret, thresholdImage = cv2.threshold(newImage, threshold, 255, thresholdType)
    thresholdImage = cv2.cvtColor(thresholdImage, cv2.COLOR_GRAY2BGR)
    return thresholdImage

#'Local Relative Neighborhood Thresholding', better for inconsistent lighting
def adaptiveThreshold(image, parameters):
    newImage = np.copy(image)
    #Convert to grayscale
    newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    #Apply median filter with specified size (size is 2n+1 * slider (ex: 1 becomes 3, 2 becomes 5))
    blockSize = max(2*parameters['BlockSize']+1, 3)
    newImage  = cv2.medianBlur(newImage, blockSize)
    #Extract Parameters
    threshold = parameters['Threshold']
    adaptiveMethod = parameters['AdaptiveMethod']                  #0=Mean, 1=Gaussian
    #Perform threshold, convert back to color so it can Concantenate with Window
    thresholdImage = cv2.adaptiveThreshold(newImage, 255, adaptiveMethod, 0, blockSize, 2)
    thresholdImage = cv2.cvtColor(thresholdImage, cv2.COLOR_GRAY2BGR)
    return thresholdImage

#OTSU Thresholding uses histrogram to find best global threshold. Better for noisy(salt/pepper) images
def otsuThreshold(image, parameters):
    newImage = np.copy(image)
    #Convert to grayscale
    newImage = cv2.cvtColor(newImage, cv2.COLOR_BGR2GRAY)
    #Apply median filter with specified size (size is 2n+1 * slider (ex: 1 becomes 3, 2 becomes 5))
    blockSize = 2*parameters['BlockSize']+1
    newImage  = cv2.GaussianBlur(newImage, (blockSize, blockSize),0)
    #Extract Parameters
    threshold = parameters['Threshold']
    thresholdType  = getThresholdType(parameters['ThresholdType']) #0=Binary, 1=Truncate, #2=Floor
    #Perform threshold (automatically gets optimal threshold value)
    optimalThreshold    = ostuValue(newImage)
    ret, thresholdImage = cv2.threshold(newImage,optimalThreshold, 255, thresholdType+cv2.THRESH_OTSU)
    #Convert back to color so it can Concantenate with Window
    thresholdImage = cv2.cvtColor(thresholdImage, cv2.COLOR_GRAY2BGR)
    return thresholdImage

#Types are stored as enums, convert to right number below to skip over un-unsed enums
def getThresholdType(type):
    if type == 2:      #0=Binary (Below threshold is 0, above is 255)
        type = 3       #3=Floor (Below threshold is all 0, else normal)
    if type == 1:
        type = 2       #2=Truncate (Above threshold is 255, else normal)
    return type

#Manual Method to get OSTU Threshold value using histograms
def ostuValue(image):
    #Find normalized histogram and then cumulative distributive function
    histogram = cv2.calcHist([image],[0],None,[256],[0,256])
    normalizedHistogram = histogram.ravel()/histogram.max()
    cdf = normalizedHistogram.cumsum()
    bins = np.arange(256)
    fnMin = np.inf
    threshold = -1
    for i in range(1,256):
        #Probability, sum, weights of each class (two peaks)
        p1,p2 = np.hsplit(normalizedHistogram,[i])
        q1,q2 = cdf[i],cdf[255]-cdf[i]
        b1,b2 = np.hsplit(bins,[i])
        #Obtain means and variances
        m1,m2 = np.sum(p1*b1)/q1, np.sum(p2*b2)/q2
        v1,v2 = np.sum(((b1-m1)**2)*p1)/q1,np.sum(((b2-m2)**2)*p2)/q2
        #Calculate minimization function
        fn = v1*q1 + v2*q2
        if fn < fnMin:
            fnMin = fn
            threshold = i
    return threshold

main(name)
