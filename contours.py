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

#CONTOUR DETECTION AND DISPLAY--------------------------------------------------
#Contours are object boundaries (perimeters of a blob)
#Below is similar to boundary following algorithm
    #4th argument in findContours is approx method, which is like polyfitting (compressing # of points)
    #contours output is a list of contours. Each contour is a list of x,y boundary points
#Before finding contours, it is necessary to get a grayscale binary image (only black and white)
grayscaleImage = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
ret,binaryImage = cv2.threshold(grayscaleImage,127,255,0)
image, contours, hierarchy = cv2.findContours(binaryImage,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#Draw all contours on image
newImage = cv2.drawContours(image, contours, -1, (0,255,0), 3)
#Draw a specific contour on image based on index
newImage = cv2.drawContours(image, contours, 3, (0,255,0), 3)
#After detecting contour, extract properties for each (blob parameters)
contour = contours[3]
M = cv2.moments(contour)
centroidX = int(M['m10']/M['m00'])
centroidY = int(M['m01']/M['m00'])
area = cv2.contourArea(contour)
perimeter = cv2.arcLength(contour,True)

#Calculate general shape of feature with less features using Douglas Peucker Algorithm
epsilon = 0.1*cv2.arcLength(cnt,True)
approx = cv2.approxPolyDP(cnt,epsilon,True)

#Convex hulls are outlines of feature 'without valleys'
hull = cv2.convexHull(cnt)

#Bounding Boxes----
#Rectangle
x,y,w,h = cv2.boundingRect(cnt)
img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
#Rotated Rectangle
rect = cv2.minAreaRect(cnt)
box = cv2.boxPoints(rect)
box = np.int0(box)
im = cv2.drawContours(im,[box],0,(0,0,255),2)
#Circle
(x,y),radius = cv2.minEnclosingCircle(cnt)
center = (int(x),int(y))
radius = int(radius)
img = cv2.circle(img,center,radius,(0,255,0),2)
#Fitting
#Fitting ellipse on features
ellipse = cv2.fitEllipse(cnt)
im = cv2.ellipse(im,ellipse,(0,255,0),2)

#Fitting line on features
rows,cols = img.shape[:2]
[vx,vy,x,y] = cv2.fitLine(cnt, cv2.DIST_L2,0,0.01,0.01)
lefty = int((-x*vy/vx) + y)
righty = int(((cols-x)*vy/vx)+y)
img = cv2.line(img,(cols-1,righty),(0,lefty),(0,255,0),2)


#Get general contour parameters
x,y,w,h = cv2.boundingRect(cnt)
aspect_ratio = float(w)/h           #Aspect Ratio of bounding box
area = cv2.contourArea(cnt)
x,y,w,h = cv2.boundingRect(cnt)
rect_area = w*h
extent = float(area)/rect_area      #Extent = object area / bounding box area
area = cv2.contourArea(cnt)
hull = cv2.convexHull(cnt)
hull_area = cv2.contourArea(hull)
solidity = float(area)/hull_area    #Solidity = contour area / convex hull area
(x,y),(MA,ma),angle = cv2.fitEllipse(cnt)   #Orientation of object

#Convexity Defects
#Considered any deviation from convex hull (which shows general shape of object)
#Convex hull allows more flexibility than contour, thus these devations would be major
hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

#Full code to find convexity defects
import cv2
import numpy as np

img = cv2.imread('star.jpg')
img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(img_gray, 127, 255,0)
contours,hierarchy = cv2.findContours(thresh,2,1)
cnt = contours[0]

hull = cv2.convexHull(cnt,returnPoints = False)
defects = cv2.convexityDefects(cnt,hull)

for i in range(defects.shape[0]):
    s,e,f,d = defects[i,0]
    start = tuple(cnt[s][0])
    end = tuple(cnt[e][0])
    far = tuple(cnt[f][0])
    cv2.line(img,start,end,[0,255,0],2)
    cv2.circle(img,far,5,[0,0,255],-1)

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

#Point Polygon Test
#Shortest distance between any point in image and contour
#Negative if outside, positive if inside
dist = cv2.pointPolygonTest(cnt,(50,50),True)

#Match Shape Test
#Allows similarity comparison between two contours (lower is more similar)
import cv2
import numpy as np

img1 = cv2.imread('star.jpg',0)
img2 = cv2.imread('star2.jpg',0)

ret, thresh = cv2.threshold(img1, 127, 255,0)
ret, thresh2 = cv2.threshold(img2, 127, 255,0)
contours,hierarchy = cv2.findContours(thresh,2,1)
cnt1 = contours[0]
contours,hierarchy = cv2.findContours(thresh2,2,1)
cnt2 = contours[0]

ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
print ret

#Contour Hierarchy
#This is used when shapes are inside other shapes
#Hierarchy defines parent-child relationship between shapes/objects
#Definitions below (similar to graph theory):
    #External Contour = outermost, these contours are root level
    #Parent Contour   = has children/inner shapes
    #Child Contour    = has parent contour that it fixed to
    #First child      = if two children, this is the one at first index

#Each contour in contours list has corresponding hierarchy structure:
    #[Next, Previous, First Child, Parent]
        #Next = next contour on same hierarchial level
        #Previous = previous at same hierarchial level (if first, it is -1)
#Contour Retrieval Modes
    #RETR_LIST ---> gets contours but no hierarchy
    #RETR_EXTERNAL ---> gets contours but only returns external contours in hierarchy
    #RETR_CCOMP --> hierarhcy is only 2 levels
        #only shows 'local scope' of direct parent to children
    #RETR_TREE --> shows full hierarchy
#Hierarchy is returned with findContours
grayscaleImage = cv2.cvtColor(original,cv2.COLOR_BGR2GRAY)
ret,binaryImage = cv2.threshold(grayscaleImage,127,255,0)
image, contours, hierarchy = cv2.findContours(binaryImage,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#Can be used manually to link objects together (need to find out how later)
