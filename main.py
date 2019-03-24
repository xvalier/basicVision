import os
import cv2

#Currently loads images from specified path and displays in grayscale
def main():
    path = os.getcwd() + '/images/'
    images = getImages(path)
    for image in images:
        img = readImageGrayScale(image)
        writeImage = writeImage(img, image+'00')
        displayImage(img)

#Get list of all images in a given directory
def getImages(path):
    if not os.path.exists(path):
        path = input('Please specify location where images are stored: ')
    return [path+item for item in os.listdir(path)]

#Read image from specified path as a numpy array
def readImageGrayScale(file):
    return cv2.read(file, 0)

#Display an image
def displayImage(imageMatrix):
    cv2.imshow('image',imageMatrix)
    cv2.waitKey(0)
    cv2.destoryAllWindows()

#Write image array to specified file
def writeImage(imageMatrix, file):
    cv2.imwrite(file, imageMatrix)

main()
