from webcam import Webcam
import cv2
from datetime import datetime
from time import sleep
import numpy as np

from queue import Queue
from server import *

'''
This file is meant to be run on the laptop. This is the file that has all the routine to start the game of chess on the laptop (server side).
It will instantiate a TCP socket server, the webcam, a queue, will handle coordinate calculation and will send messages to the brick (client)
using the instantiated server.
'''

#Thread-safe queue to get data from threads
queue = Queue()
server = Server(9999)

#Start camera and frame thread
webcam = Webcam()
webcam.start(queue)

#length of a side of the chessboard in milimeters
side_length = 307



#Note: this function works in image space, all the cooridnates given here are in pixels.
#Calculate the closest point projection of an arbitrary on a line as explained in http://paulbourke.net/geometry/pointlineplane/
#Inputs: line_start [(Float, Float)]: A tuple of float values that represent the starting point of a line
#       line_end [(Float, Float)]: A tuple of float values that represent the ending point of a line
#       point [(Float, Float)]: A tuple of float values that represent the point that we want to project onto the line.
#Returns [(Float,Float)]: A tuple of float values that correspond to the closest on the given line in relation to the given point
def closest_point(line_start, line_end, point):
    delta_vector = np.subtract(line_end,line_start)
    u = ((point[0]-line_start[0])*(line_end[0]-line_start[0])+(point[1]-line_start[1])*(line_end[1]-line_start[1]))/np.dot(delta_vector, delta_vector)
    x = line_start[0] + u*(line_end[0]-line_start[0])
    y = line_start[1] + u*(line_end[1]-line_start[1])
    return (x,y)

#This function takes a point (u,v) in image space and translates it into a point (x,y) in world coordinates (milimetres)
#Input: u [Float]: u coordinate in image space
#       v [Float]: v coordinate in image space
#Output: ([Float,Float]) A tuple of float values that represent the world coordinates (in milimetres) of the given point in image space
def calculate_coordinates(u,v):
    #Calculate the closest points to the given point on each of the corners
    closest_left = closest_point(corners[0],corners[1], (u,v))
    closest_bottom = closest_point(corners[0],corners[3], (u,v))
    closest_right = closest_point(corners[3],corners[2], (u,v))
    closest_top = closest_point(corners[1],corners[2], (u,v))
    current_point = (u,v)
    #Get Horizontal Length from left corner closest (projected) point to the given point by Pythagoras Theorem
    horizontal_length_1 = ((current_point[0] - closest_left[0])**2+(current_point[1] - closest_left[1])**2)**(0.5)
    #Get Horizontal Length the given point to the right corner closest (projected) point to by Pythagoras Theorem
    horizontal_length_2 = ((closest_right[0] - current_point[0])**2+(closest_right[1] - current_point[1])**2)**(0.5)

    #Get Horizontal Length from bottom corner closest (projected) point to the given point by Pythagoras Theorem
    vertical_length_1 = ((current_point[0] - closest_bottom[0])**2+(current_point[1] - closest_bottom[1])**2)**(0.5)
    #Get Horizontal Length the given point to the top corner closest (projected) point to by Pythagoras Theorem
    vertical_length_2 = ((closest_top[0] - current_point[0])**2+(closest_top[1] - current_point[1])**2)**(0.5)

    #Get the position of the points in image space as a proportion of how far is the point from the origin (lower left corner)
    proportionX = horizontal_length_1/(horizontal_length_1 + horizontal_length_2)
    propotionY = vertical_length_1/(vertical_length_1 + vertical_length_2)
    #Once we have proportions, we multiply each proportion by the side length in milimetres of the chessboard. This will give us
    #a good approximation of the world coordinates (in milimetres) that correspond to the (u,v) in he chessboard
    return (side_length*proportionX, side_length*propotionY)

#The four corners of the chessboard are specified in clockwise order. The list will have the corners stored in the following order:
#[lower_left, upper_left, upper_right, lower_right]
corners = []

#First we specify we four corners of the chessboard (specified in clockwise order starting from the lower left corner)
while len(corners) < 4:
    #get point from the camera by using the queue
    point = queue.get()
    corners.append(point)
    #Add the point that we just got to the list of permament points
    webcam.add_permament_points(point)

#Array meant to store the two points that the user will have to specify for a movement    
current_points = []
while True:
    #Get a user defined point from the camera thread
    point = queue.get()
    current_points.append(point)
    #Add it to the list of temporary points
    webcam.add_temporary_points(point)
    #Once we have two points defined (the one corresponding to the piece we want to pick up and the other one corresponding to the destionation or drop location)
    #we are ready to initiate a move
    if (len(current_points) == 2):
        #First, take the initial and position end effector over it
        #Make sure to account for the 100 mm in offset for the y axis since the initial position of the y axis is now set to be 100mm behind the board
        #There should also be an offset of  19mm for x and y since the length of each cell of the board is 38mm, and the initial position of the end effector
        #is in the centre of the cell a1 right on top of the rook in the that position. Since it is the centre of the first cell, then the end effector effectively
        #will start at (19,19) in world coordinates
        (x1,y1) = calculate_coordinates(current_points[0][0], current_points[0][1])
        #After the coordinates in milimetres are calculated we move the robot to the desired initial point to pick the piece while taking the offsets into account
        #Note: The negative signs are because of the robot design, we have to invert the direction for the movements to be in tune with how we define the origin of the chessboard
        server.sendDistances(-x1 + 19, -(100 + y1) + 19)
        server.sendLowerClaw()
        server.sendCloseClaw()
        server.sendRaiseClaw()
        #After piece is grabbed, we move it to the desired position specified in the second point
        (x2,y2) = calculate_coordinates(current_points[1][0], current_points[1][1])
        #After we get the coordinates in milimitres for the second point, getting the movement required in the X and Y axis is straight forward.
        #Since we already moved to the first point, we just calculate the delta between the first point (our current location) and the second once
        delta_x = x2 - x1
        delta_y = y2 - y1
        #After we have the delta, we move in that direction
        #Note: The negative signs are because of the robot design, we have to invert the direction for the movements to be in tune with how we define the origin of the chessboard
        server.sendDistances(-delta_x, -delta_y)
        #Once we arrive to the second point, we drop the piece.
        server.sendLowerClaw()
        server.sendOpenClaw()
        server.sendRaiseClaw()
        #After the piece is dropped, we home the robot, and clear the two points for specifying the movement from the current_points list and the temporar_points list in 
        #the camera frame
        server.sendHome()
        current_points.clear()
        webcam.remove_temporary_points()

server.sendTermination() 