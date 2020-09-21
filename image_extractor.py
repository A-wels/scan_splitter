import cv2,sys, imutils
import numpy as np
import os

path = '/home/alex/ScannedImages/unprocessed/'
target = "/home/alex/ScannedImages/processed/"

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
i=0
for file in os.listdir(path):
    print(path+file)
    image = cv2.imread(path+file)
    x=5100
    y=7015

    image = image[20:y-50, 5:x-5]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, th = cv2.threshold(gray,210,235,1)
    cv2.imshow("Image", th)
    cv2.waitKey(0)
    cnts, hierarchy = cv2.findContours(th.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
    i=0
    for c in cnts:
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        Area = image.shape[0]*image.shape[1]
        if Area/10 < cv2.contourArea(box) < Area*2/3:
            cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
            roi = image[box[2][1]:box[1][1], box[1][0]:box[0][1]]
            x_0 = min(box[0][0],box[1][0], box[2][0], box[3][0])
            x_1 = max(box[0][0],box[1][0], box[2][0], box[3][0])
            y_0 = min(box[0][1],box[1][1], box[2][1], box[3][1])
            y_1 = max(box[0][1],box[1][1], box[2][1], box[3][1])
            roi = image[y_0:y_1, x_0:x_1]
            print(target+str(i)+"-"+file)
            try:
                cv2.imwrite(target+str(i)+"-"+file, roi)

            except:
                pass
            i = i+1
    cv2.imshow("Image", image)
    cv2.waitKey(0)