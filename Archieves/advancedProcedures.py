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

original = imageResize(cv2.imread(name, 1), scaleFactor)

#CANNY EDGE DETECTION-----------------------------------------------------------
#Procedure for this is below:
#1) 5x5 Gaussian Filter to remove noise
#2) Get 1st Derivatives Gx and Gy
#3) Obtain Magnitude M = sqrt(Gx^2 +Gy^2) and Angle theta = atan(Gx/Gy)
#4) Nonminima Suppression -> keep only maxima/peaks
#5) Hysterisis Threshold, user selects thresholds tHigh and tLow
    #if above tHigh -> edge
    #if below tLow  -> not edge
    #if between tHigh and tLow -> edge only if near other edge points
tLow  = 100
tHigh = 200
processedImage = cv2.Canny(original,tLow,tHigh)

#TEMPLATE MATCHING--------------------------------------------------------------
img = cv2.imread('messi5.jpg',0)
img2 = img.copy()
template = cv2.imread('template.jpg',0)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = eval(meth)

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)

    cv2.rectangle(img,top_left, bottom_right, 255, 2)

    plt.subplot(121),plt.imshow(res,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)

    plt.show


#With Multiple objects
import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('mario.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('mario_coin.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)


#WATERSHED ALGORITHM FOR IMAGE SEGMENTATION-------------------------------------
#1) OSTU Thresholding
#2) Morphological Opening to separate objects further
    #(use Closing if there are holes inside objects) (remove noise)
#3) Perform distance transform
#4) Threshold to get segmented objects
#5) Label markers
#6) Perform watershed

img = cv2.imread('coins.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

#Sure Background Area = where we know there is no object
sure_bg = cv2.dilate(opening,kernel,iterations=3)

#Sure Foreground Area = where we know there IS an object
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

#Unknown ForeGround Area = area where object presence is uncertain
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

#Marker Labelling, background becomes 0, everything else becomes integer starting at 1
#Label other objects as integers (counts) starting at 1
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
#This distinguishes background from unknown foreground
markers = markers+1

# Now, mark the region of unknown with zero
markers[unknown==255] = 0

#Perform watershed
markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]
