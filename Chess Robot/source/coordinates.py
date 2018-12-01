from webcam import Webcam
import cv2
from datetime import datetime
from time import sleep
import numpy as np

from queue import Queue
from server import *

#Thread-safe queue to get data from threads
queue = Queue()
server = Server(9999)

webcam = Webcam()
webcam.start()

#image = cv2.imread("board.jpg")
#in milimeters
side_length = 307


def mouse_drawing(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        corners.append((x, y))

def add_target(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Left click")
        current_points.append((x, y))

#As explained in http://paulbourke.net/geometry/pointlineplane/
def closest_point(line_start, line_end, point):
    #First element is delta x, second one is delta y
    delta_vector = np.subtract(line_end,line_start)
    u = ((point[0]-line_start[0])*(line_end[0]-line_start[0])+(point[1]-line_start[1])*(line_end[1]-line_start[1]))/np.dot(delta_vector, delta_vector)
    x = line_start[0] + u*(line_end[0]-line_start[0])
    y = line_start[1] + u*(line_end[1]-line_start[1])
    return (x,y)


def calculate_coordinates(x,y):
    print("Distance to left corner")
    closest_left = closest_point(corners[0],corners[1], (x,y))
    closest_bottom = closest_point(corners[0],corners[3], (x,y))
    closest_right = closest_point(corners[3],corners[2], (x,y))
    closest_top = closest_point(corners[1],corners[2], (x,y))
    print(str(closest_point(corners[0],corners[1], (x,y))))
    current_point = (x,y)
    #Get Horizontal Length by Pythagoras Theorem
    horizontal_length = ((closest_right[0] - closest_left[0])**2+(closest_right[1] - closest_left[1])**2)**(0.5)
    #Get Vertical Length by Pythagoras Theorem
    vertical_length = ((closest_top[0] - closest_bottom[0])**2+(closest_top[1] - closest_bottom[1])**2)**(0.5)

    #Horizontal length until the closest point  (from left to right)
    horizontal_distance_to_point = ((current_point[0] - closest_left[0])**2+(current_point[1] - closest_left[1])**2)**(0.5)
    #Vertical length until the closest point (from bottom to top)
    vertical_distance_to_point = ((current_point[0] - closest_bottom[0])**2+(current_point[1] - closest_bottom[1])**2)**(0.5)

    #In pixels
    print("Current Point: " + str(current_point))
    #Now we get the percentage eg (current position x)/total length of the x line )both in pixels. This will give us a percentage
    print("Proportion in X: " + str(horizontal_distance_to_point/horizontal_length) + " Proportion in Y: " + str(vertical_distance_to_point/vertical_length))
    #Then multiply that percentage by 307 to the the milimiter length
    proportionX = horizontal_distance_to_point/horizontal_length 
    propotionY = vertical_distance_to_point/vertical_length
    return (side_length*proportionX, side_length*propotionY)

#[lower_left, upper_left, upper_right, lower_right]
corners = []

 
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", mouse_drawing)

while len(corners) < 4:
     
    # get image from webcam
    image = webcam.get_current_frame()
    for center_position in corners:
        cv2.circle(image, center_position, 5, (0, 0, 255), -1)
    # display image
    cv2.imshow('Frame', image)
    
    key = cv2.waitKey(1)

cv2.setMouseCallback("Frame", add_target)

current_points = []

while True:
    # get image from webcam
    print("Get Frame")
    image = webcam.get_current_frame()
    for center_position in corners:
        cv2.circle(image, center_position, 5, (0, 0, 255), -1)
    # display image
    for current_point in current_points:
        cv2.circle(image, current_point, 5, (0, 0, 0), -1)

    cv2.imshow('Frame', image)

    if (len(current_points) == 2):
        #First, take the initial and position end effector over it
        #Make sure to account for the 100 mm in offset for the y axis and the 19mm for x and y
        (x1,y1) = calculate_coordinates(current_points[0][0], current_points[0][1])
        server.sendDistances(-x1 + 19, -(100 + y1) + 19, queue)
        server.sendLowerClaw()
        server.sendCloseClaw()
        server.sendRaiseClaw()
        #After piece is grabbed, we move it to the desired position specified in the second point
        (x2,y2) = calculate_coordinates(current_points[1][0], current_points[1][1])
        delta_x = x2 - x1
        delta_y = y2 - y1
        server.sendDistances(-delta_x, -delta_y, queue)
        server.sendLowerClaw()
        server.sendOpenClaw()
        server.sendRaiseClaw()
        server.sendHome()
        current_points.clear()
    key = cv2.waitKey(1)
    if 'q' == chr(key & 255):
        break

server.sendTermination() 
cv2.destroyAllWindows()