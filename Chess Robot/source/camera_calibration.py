from webcam import Webcam
import cv2
from datetime import datetime
from time import sleep
import numpy as np

'''
This file handles camera calibration in OpenCV. It will take 30 images from the webcam and use them to infer the camera parameters and distortion coefficients
Then these values will be saved into two files for future use.
'''

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
#We are using a 7x9 Grid to calibrate the camera
objp = np.zeros((7*9,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:9].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

total_images = 0

#Initialize webcam
vc = cv2.VideoCapture(0)
#Get the first frame
if vc.isOpened():
    rval, frame = vc.read()
else:
    rval = False

#This loop makes sure that the camera has time to properly initialize and adjust to the
#lighting conditions. If this loop is not present, then the frame object which is used 
#To specify the regions of interest further down the code would be too dark
i = 0
while rval and i < 100:
    # Read a new frame
    rval, frame = vc.read()
    i = i + 1
 
while total_images < 30:
     
    # get image from webcam
    rval, image = vc.read()
 
    # display image
    cv2.imshow('grid', image)
    
    cv2.waitKey(3000)

    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    #Try to identify the 7x9 chessboard pattern in the current image
    ret, corners = cv2.findChessboardCorners(gray, (7,9), None)
    
    #If chessboard pattern was found
    if ret == True:
        objpoints.append(objp)
        #Get accurate location of the corners for each cell in the calibration chessboard
        #using an interative method until the termination criteria is met.
        corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        imgpoints.append(corners)
        #Draw the refined chessboard corners on top of the image
        cv2.drawChessboardCorners(image, (7,9), corners2, ret)
        cv2.imshow('grid', image)
        cv2.waitKey(1500)
        total_images = total_images + 1
        print(total_images)

cv2.destroyAllWindows()
#After we have all the images and image points. Then we will run the camera calibration. This function will take care of inferring the intrinsic parameters of the
#camera as well as the distortion coefficients (for tangential and radial distortion)
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#Save the parameters to disk
np.savetxt('camera_matrix.out', mtx)
np.savetxt('distortion_coeffs.out', dist)
