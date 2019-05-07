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



#CONTOUR DETECTION AND DISPLAY--------------------------------------------------
#Contours are object boundaries (perimeters of a blob)
#Below is similar to boundary following algorithm
#4th argument in findContours is approx method, which is like polyfitting (compressing # of points)
#contours output is a list of contours. Each contour is a list of x,y boundary points 
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(imgray,127,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
