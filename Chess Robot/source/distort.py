from webcam import Webcam
import cv2
from datetime import datetime
from time import sleep
import numpy as np

#webcam = Webcam()
#webcam.start()

image = cv2.imread("board.jpg")
#in milimeters
side_length = 307


def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        corners.append((x, y))

#As explained in http://paulbourke.net/geometry/pointlineplane/
def closest_point(line_start, line_end, point):
    #First element is delta x, second one is delta y
    delta_vector = np.subtract(line_end,line_start)
    u = ((point[0]-line_start[0])*(line_end[0]-line_start[0])+(point[1]-line_start[1])*(line_end[1]-line_start[1]))/np.dot(delta_vector, delta_vector)
    x = line_start[0] + u*(line_end[0]-line_start[0])
    y = line_start[1] + u*(line_end[1]-line_start[1])
    return (x,y)


def calculate_coordinates(event, x,y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Distance to left corner")
        print(str(closest_point(corners[0],corners[1], (x,y))))
        current_point = (x,y)
        closest = closest_point(corners[0],corners[1], (x,y))
        print(str(np.subtract(current_point,closest)))
        #Now we get the percentage eg (current position x)/total length of the x line )both in pixels. This will give us a percentage
        #Then multiply that percentage by 307 to the the milimiter length

#[lower_left, upper_left, upper_right, lower_right]
corners = []

 
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while len(corners) < 4:
     
    # get image from webcam
    #image = webcam.get_current_frame()
    for center_position in corners:
        cv2.circle(image, center_position, 5, (0, 0, 255), -1)
    # display image
    cv2.imshow('Frame', image)
    
    key = cv2.waitKey(1)

cv2.setMouseCallback("Frame", calculate_coordinates)

current_point = None

while True:
    # get image from webcam
    #image = webcam.get_current_frame()
    for center_position in corners:
        cv2.circle(image, center_position, 5, (0, 0, 255), -1)
    # display image
    cv2.imshow('Frame', image)
    if current_point is not None:
        cv2.circle(image, current_point, 5, (0, 0, 0), -1)
    
    key = cv2.waitKey(1)
 
cv2.destroyAllWindows()