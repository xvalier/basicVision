import os
import cv2
path = '/home/xvalier/Documents/snippets_openCV/images/Receipts/'
tl = 50
th = 150
choice =0

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
