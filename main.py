import os
import cv2

#Get list of all images in a given directory
def getImages(path):
    if not os.path.exists(path):
        path = input('Please specify location where images are stored: ')
    return [path+item for item in os.listdir(path)]

#Read image from specified path as a numpy array
def readImageGrayScale(file):
    return cv2.imread(file, 0)

def readImageColor(file):
    return cv2.imread(file)

def splitColorChannel(image):
    return cv2.split(image)

#Display an image, fitted in window
def displayImage(imageMatrix):
    cv2.namedWindow("Display",cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Display",600,600)
    cv2.imshow("Display",imageMatrix)
    cv2.waitKey(0)
    cv2.destoryAllWindows()

#Canny Edge Detector
def edgeDetectCanny(image, thresholdLow, thresholdHigh):
    edges = cv2.Canny(image, thresholdLow, thresholdHigh)
    return edges

#Write image array to specified file
def writeImage(path,name, image):
    cv2.imwrite(path+name, image)

path = '/home/xvalier/Documents/snippets_openCV/images/Receipts/'
tl = 50
th = 150
choice =0
a = getImages(path)

#Simple Edge Detection
b = readImageGrayScale(a[choice])
c = edgeDetectCanny(b,tl,th)
displayImage(c)

#Color Splitting
#b = readImageColor(a[choice])
#b,g,r = splitColorChannel(b)
#displayImage(b)
#displayImage(g)
#displayImage(r)
