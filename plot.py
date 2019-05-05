import numpy as np
import matplotlib.pyplot as plt

#General plotting
x = np.arange(0, 5, 0.1);
y = np.sin(x)
plt.plot(x, y)


#Since openCV is BGR and matplotlib is RGB, need to flip channels if color
img = cv2.imread('messi4.jpg')
b,g,r = cv2.split(img)
img2 = cv2.merge([r,g,b])
plt.subplot(121);plt.imshow(img) # expects distorted color
plt.subplot(122);plt.imshow(img2) # expect true color
plt.show()

cv2.imshow('bgr image',img) # expects true color
cv2.imshow('rgb image',img2) # expects distorted color
cv2.waitKey(0)
cv2.destroyAllWindows()

#Or use the following
cv2.cvtColor(img, cv2.BGR2RGB)
