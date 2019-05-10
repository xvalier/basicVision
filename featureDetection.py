#Harris Corner Detector
#Theory:
    #Find 1st derivates Ix and Iy (can be done via sobel)
    #Perform M = Summation( window(x,y) * [IxIx IxIy, IxIy IyIy])
    #R = det(M) - k (trace(M))^2
        #lamba1 * lamba2 = det(M)
        #lamba1 + lamba2 = trace(M)
        #Essentially R = lamda1*lamda2 - k(lamda1 +lamda2)^2
        #lamba1 and lamda2 are eigenvalues of M
        #if abs(R) is small (thus both lambas small), region is flat
        #if R < 0 (when lamda1 >> lamba2), region is edge
        #if R = large (when both lamdas large and lamda1 ~ lamda2), region is corner
        #opencv function needs image, blockSize, ksize (aperature param of sobel derivative), and k (harris parameter)

import cv2
import numpy as np

filename = 'chessboard.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

gray = np.float32(gray)
dst = cv2.cornerHarris(gray,2,3,0.04)

#result is dilated for marking the corners, not important
dst = cv2.dilate(dst,None)

# Threshold for an optimal value, it may vary depending on the image.
img[dst>0.01*dst.max()]=[0,0,255]

cv2.imshow('dst',img)
if cv2.waitKey(0) & 0xff == 27:
    cv2.destroyAllWindows()

#Shi Tomasi Corner Detector
#Generally works better than Harris, finds N strongest corners
#Theory:
    #R = min(lamda1, lamda2)
    #params = image, N,
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
corners = np.int0(corners)

for i in corners:
    x,y = i.ravel()
    cv2.circle(img,(x,y),3,255,-1)
