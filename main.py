import os
import cv2
path = '/home/xvalier/Documents/snippets_openCV/images/'

#TODO: Learn to use matplotlib to display data better
    #Includes drawing boxes, ROIs, taking in data like histograms

#Currently loads images from specified path and displays in grayscale
def main():
    #path = os.getcwd() + '/images/'
    images = getImages(path)
    for image in images:
        img = readImageGrayScale(image)
        #name = input('what should image be called?')
        #writeImage = writeImage(img, image)
        displayImage(img)



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

#Display an image
def displayImage(imageMatrix):
    cv2.imshow('image',imageMatrix)
    cv2.waitKey(0)
    cv2.destoryAllWindows()

#Canny Edge Detector
def edgeDetectCanny(image, thresholdLow, thresholdHigh):
    edges = cv2.Canny(image, thresholdLow, thresholdHigh)
    return edges

#Write image array to specified file
def writeImage(path,name, image):
    cv2.imwrite(path+name, image)

path = '/home/xvalier/Documents/snippets_openCV/images/'
tl = 50
th = 150
choice =0
a = getImages(path)

#Simple Edge Detection
#b = readImageGrayScale(a[choice])
#c = edgeDetectCanny(b,tl,th)
#displayImage(c)

#Color Splitting
b = readImageColor(a[choice])
b,g,r = splitColorChannel(b)
displayImage(b)
displayImage(g)
displayImage(r)
