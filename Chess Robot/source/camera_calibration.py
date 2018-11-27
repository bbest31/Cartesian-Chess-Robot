from webcam import Webcam
import cv2
from datetime import datetime
from time import sleep
import numpy as np

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#7x9 Grid
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:9].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

total_images = 0

webcam = Webcam()
webcam.start()
 
while total_images < 15:
     
    # get image from webcam
    image = webcam.get_current_frame()
 
    # display image
    cv2.imshow('grid', image)
    cv2.waitKey(3000)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    # save image to file, if pattern found
    ret, corners = cv2.findChessboardCorners(gray, (7,9), None)
 
    if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        cv2.drawChessboardCorners(image, (7,9), corners2, ret)
        cv2.imshow('grid', image)
        cv2.waitKey(500)
        total_images = total_images + 1
        print(total_images)

cv2.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#cv.undistort