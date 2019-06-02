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

#SIFT (Learn this more in depth later)
#Hariss and Shi Tomasi are rotation-invariant, but not scale-invariant
#We need larger windows to detect larger corners
#Can use LoG (Laplacian of Gaussian), finds blobs of various size based on sigma (scaling param)
    #ex: guassian with low sigma = high value for small corner, high sigma = better fit on large corner
#LoG is expense, so DoG (Difference of Gaussian) is used to find approximation of LoG
    #Perform Gaussian at different sigmas (sigma, then k*sigma, ...)
    #Diff between Gaussians
#Steps
#1) DoG is used to find feature at various scales (based diff sigma values)
#2) At optimal sigma scale, look for potential keypoint x,y
#3) Check if keypoint passes contrastThreshold, edgeThreshold for intensity/edge tolerance
    #used to eliminate low contrast/bad edge keypoints
#4) For remaining keypoints, 36 orientation bins (for each 10 degree rotation) is calcualted
    #Only orientation bins with highest peak and 80% are kept for rotation invariance
#5) Keypoint description is created
    #16x16 pixel neighborhood around keypoint is calculated
    #16 subblock of 4x4 size
    #8 bins histogram for each subblock (total 128 bins)
    #used to be robust against illimuniation/rotation changes
#6) Now keypoints are matched
#GET THIS MORE IN DEPTH, IT IS IMPORTANT
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

sift = cv2.SIFT()
keypoint = sift.detect(gray,None) #None can be replaced with a mask
image    = cv2.drawKeypoints(gray, keypoint)
cv2.imwrite('new.jpg',image)

#SURF (Faster version of SIFT)
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

hessian = 400 #can lower amount of features detected by increasing hessianthreshold
surf = cv2.SURF(hessian)
keypoints, descriptions = surf.detectAndCompute(img, None)
img2 = cv2.drawKeypoints(img, keypoints, None, (255,0,0),4)
#For cases where orientation tolerance is not needed, can do below
surf.upright = True
keypoints = surf.detect(img, None)
img2 = cv2.drawKeypoints(img, keypoints, None, (255,0,0),4)

#FAST (faster real time corner detector for applications like SLAM)
#1) Get a set of images for training
#2) On each one, run FAST Algorithm
    #a) Select pixel p in image as interest point with intensity Ip
    #b) Choose a threshold t
    #c) Get 16 pixel neighborhood of interest point
    #d) If any pixel is Ip +t (brighter), IP-t (darker),
#3) for All feature points, store 16 pixel neighborhood as vector
#4) Each pixel in feature vector can be either darker, brighter, or similar
#FIND VIDEO ON THIS LATER
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

fast = cv2.FastFeatureDetector()
keypoints = fast.detect(img,None)
#Choose color of graphics overlay
img2 = cv2.drawKeypoints(img, keypoints, color=(255,0,0))
cv2.imwrite('new.png',img2)

#ORB (faster and free version of SURF and SIFT)
#Uses FAST for keypoint detection
#Harris Corner Detector then used to find best keypoints
#BRIEF for descriptors
import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('simple.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
orb = cv2.ORB()
keypoints = orb.detect(img,None) #Include Mask if needed
keypoints, descriptors = orb.compute(img, keypoints)
img2 = cv2.drawKeypoints(img,keypoints,color=(0,255,0), flags=0)
