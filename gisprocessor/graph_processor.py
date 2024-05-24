import numpy as np
import cv2

# Read the image and create a blank mask
img = cv2.imread('graph.png')
h, w = img.shape[:2]
mask = np.zeros((h, w), np.uint8)

# Transform to gray colorspace and threshold the image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

# Search for contours and select the biggest one and draw it on mask
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnt = max(contours, key=cv2.contourArea)
cv2.drawContours(mask, [cnt], 0, 255, -1)

# Perform a bitwise operation
res = cv2.bitwise_and(img, img, mask=mask)

# Convert black pixels back to white
black = np.where(res == 0)
res[black[0], black[1], :] = [255, 255, 255]

# Display the image
cv2.imshow('img', res)
cv2.waitKey(0)
cv2.destroyAllWindows()
