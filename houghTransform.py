#HOUGH TRANSFORMS
#If shape can be represented in math form (line, rectangle, circle, etc),
    #We can use hough transform to detect them, even if there is some distortion
#Example Procedure:
    #A line can be represented as p = xcos(theta) + ysin(theta)
    #Create an output 'accumulator' image mapping p and theta values
    #On 100x100 image with horizontal line in middle
    #Go to first point on line (x,y)
        #Try multiple theta values and check resulting p values
        #Add +1 for every (p,theta) pair found with first point
    #Go to second point on line, repeat steps of first point
    #Repeat until you get all points
    #Output image's bright spots show (p,theta) combinations that could be possible lines
import cv2
import numpy as np

img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)

lines = cv2.HoughLines(edges,1,np.pi/180,200)
for rho,theta in lines[0]:
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a*rho
    y0 = b*rho
    x1 = int(x0 + 1000*(-b))
    y1 = int(y0 + 1000*(a))
    x2 = int(x0 - 1000*(-b))
    y2 = int(y0 - 1000*(a))

    cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)

cv2.imwrite('houghlines3.jpg',img

#Since Hough Transform is computationally expensive,
    #Can use probabilistic Hough Transform to select random points on line, rather than all
    import cv2
import numpy as np

img = cv2.imread('dave.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(gray,50,150,apertureSize = 3)
minLineLength = 100
maxLineGap = 10
lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)
for x1,y1,x2,y2 in lines[0]:
    cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

cv2.imwrite('houghlines5.jpg',img)

#For circles, you can use r^2 = (x-x_center)^2 + (y-y_center)^2
    #Since there are three params (r,x,y), we need 3D accumulator for hough transform
import cv2
import numpy as np

img = cv2.imread('opencv_logo.png',0)
img = cv2.medianBlur(img,5)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,1,20,
                            param1=50,param2=30,minRadius=0,maxRadius=0)

circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

cv2.imshow('detected circles',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
