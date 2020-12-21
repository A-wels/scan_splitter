import cv2,sys, imutils
import numpy as np
import os

path = '/home/alex/ScannedImages/images'

cv2.namedWindow('image', cv2.WINDOW_NORMAL)
i=0
for dir in os.walk(path):
    target = dir[0]+"/processed/"
    for file in os.listdir(dir[0]):
        if  file.endswith(".tif") or file.endswith(".tiff") or file.endswith(".png") or file.endswith(".PNG"):
            if not os.path.exists(target):
                os.makedirs(target)   
            img_path = dir[0]+"/"+file
            print(img_path)
            image = cv2.imread(img_path)
            bordersize = 10
            x=5110
            y=7025

            image = image[20:y-40, 5:x-5]
  

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            hsv=cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

            # Define lower and uppper limits of what we call "brown"
            brown_lo=np.array([0,0,0])
            brown_hi=np.array([13,13,13])

            # Mask image to only select browns
            mask=cv2.inRange(hsv,brown_lo,brown_hi)

            # Change image to red where we found brown
            gray[mask>0]=(255)

            
          #  imS = cv2.resize(image, (1280, 720))                    # Resize image
        #    cv2.imshow("Image", imS)
         #   cv2.waitKey(0)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)

            ret, th = cv2.threshold(gray,210,235,1)

            
            cnts, hierarchy = cv2.findContours(th.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
            i=0
            for c in cnts:
                box = cv2.minAreaRect(c)
                box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
                box = np.array(box, dtype="int")
                Area = image.shape[0]*image.shape[1]
                if Area/10 < cv2.contourArea(box) < Area*1/4:
                    x, y, width, height = cv2.boundingRect(c)
                    roi = image[y:y+height, x:x+width]
                    print(target+str(i)+"-"+file)
                    try:
                        cv2.imwrite(target+str(i)+"-"+file, roi)
                      #  cv2.drawContours(image, [box], -1, (0, 255, 0), 20)
                        i = i+1


                    except:
                        pass
        # ratio = image.shape[0] / 400.0
        # image = imutils.resize(image, height = 800)

        # cv2.imshow("Image", image)
        # cv2.waitKey(0)