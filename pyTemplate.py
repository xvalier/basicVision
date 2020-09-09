import cv2 as cv 
import os
'''
#SKU3
operation1 = cv.MORPH_CLOSE #Closing
k1_x = 26
k1_y = 8
itr1 = 4
operation2 = cv.MORPH_GRADIENT #Opening
k2_x = 16
k2_y = 14
itr2 = 1
morphxoffset = 162
morphyoffset = 89
'''
#SKU5
operation1 = cv.MORPH_HITMISS #Closing
k1_x = 1
k1_y = 4
itr1 = 7
operation2 = cv.MORPH_CLOSE #Opening
k2_x = 60
k2_y = 60
itr2 = 1
morphxoffset = 162
morphyoffset = 89

'''
#Hyperparameters for configuration (edit as needed)
operation1 = cv.MORPH_CLOSE #Closing
k1_x = 26
k1_y = 23
itr1 = 1
operation2 = cv.MORPH_OPEN #Opening
k2_x = 1
k2_y = 34
itr2 = 2
morphxoffset = 61 
morphyoffset = 137
'''







def main():
    images, names  = import_images()
    results = morph_images(images)
    export_images(results, names)

#Import all images from specified input directory
def import_images():
    path = os.getcwd() + '\\input\\'
    images = []
    names = []
    for file in os.listdir(path):
        print(path+file)
        names.append(file)
        image = cv.imread(path + file, 0)
        images.append(image)
    return images, names

#Normalize images to outlines of white contours by binarizing and then morphing images
def morph_images(images):

    kernel_1 = cv.getStructuringElement(cv.MORPH_RECT,(k1_x, k1_y))
    kernel_2 = cv.getStructuringElement(cv.MORPH_RECT,(k2_x, k2_y))
    results = []
    for img in images:
        t, binarized_img = cv.threshold(img, 0, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)
        morph_1 = cv.morphologyEx(binarized_img, operation1, kernel_1, iterations=itr1)
        morph_2 = cv.morphologyEx(morph_1, operation2, kernel_2, iterations=itr2)
        results.append(morph_2)
    return results

#Export all images to specified output directory
def export_images(images, names):
    path = os.getcwd() + '\\templates\\'
    for i in range(0, len(images)):
        cv.imwrite(path+"t"+names[i]+".bmp", images[i])

main()