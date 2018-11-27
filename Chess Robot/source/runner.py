from client import Client
from robot import *
import socket
from threading import Event, Thread
from time import sleep

#This routine will run on the lego Brick. It initalizes the client and will listen 
#for commands from the server.

#Instantiate robot
robot = Robot()
#Attempt to connect to server
client = Client(9999)

while True:
    #Block until a command/message from the server is received
    data = str(client.pollData())
    if(data == 'EXIT'):
        #Terminate the routine on the client
        #robot.stop()
        break
    else:
        #If the data we got from the server is not one of the predifined messages
        #We assume (big assumption) that the message will contain the angles in the 
        #Agreed format: x_motor_angle,y_motor_angle
        #We convert the angles to float after splitting the message on the tab
        x_motor_angle, y_motor_angle = map(float,map(str,data.split(','))) 
        #This will make sure that both angles are at most 360 degrees. In addition,
        #it will consider both, the clockwise and counterclockwise rotations to reach
        #the desired position for each motor and will pick the smallest one. So that the chances of making
        #very large rotations are lessened.
        #x_motor_angle = int(x_motor_angle) % 360  
        #x_motor_angle = min([x_motor_angle, x_motor_angle - 360], key=lambda x: abs(x))
        #y_motor_angle = int(y_motor_angle) % 360
        #y_motor_angle = min([y_motor_angle, y_motor_angle - 360], key=lambda x: abs(x))
        #After the proper rotation angle has been selected, we send the move command to the motors
        print("Moving X: " + str(x_motor_angle)+ " Moving Y: " + str(y_motor_angle))
        robot.moveX(x_motor_angle)
        robot.moveY(y_motor_angle)
        client.sendDone()