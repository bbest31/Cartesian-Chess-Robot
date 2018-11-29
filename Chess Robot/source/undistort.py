from webcam import Webcam
import cv2
from datetime import datetime
from time import sleep
import numpy as np

w = 640
h = 480
mtx = np.loadtxt('camera_matrix.out')
dist = np.loadtxt('distortion_coeffs.out')
newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
webcam = Webcam()
webcam.start()
while True:
    
    img = webcam.get_current_frame()
    dst = cv2.remap(img,mapx,mapy,cv2.INTER_LINEAR)
    cv2.imshow('grid', dst)
    cv2.waitKey(300)

