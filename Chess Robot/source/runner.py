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
#After the robot is instantiated and initialized in its starting position, we will move thwe end effector carriage
#100mm backwards so that the remote player has a clear picture of the board
robot.moveY(100)
#After the robot moves the 100mm backwards, set the new position as the home for the Y axis
#This will make homing back easier, as whenever we decide to home the Y axis again, it will home 
#100mm behind the board leaving a clear picture
robot.currentY = 0

while True:
    #Block until a command/message from the server is received
    data = str(client.pollData())
    if(data == 'EXIT'):
        #Terminate the routine on the client
        robot.stop()
        break
    elif(data == "LOWER_CLAW"):
        robot.clawDown()
    elif(data == "RAISE_CLAW"):
        robot.clawUp()
    elif(data == "OPEN_CLAW"):
        robot.openClaw()
    elif(data == "CLOSE_CLAW"):
        robot.closeClaw()
    elif(data == "HOME"):
        #Home the robot. This is usually done after a movement has been executed 
        #So that the remote player has a clear view of the board for their next movement
        robot.homeX()
        robot.homeY()
        client.sendDone()
    else:
        # #If the data we got from the server is not one of the predifined messages
        # #We assume (big assumption) that the message will contain the angles in the 
        # #Agreed format: x_distance,y_distance (both given in milimetres)
        print("data "+str(data))
        x_distance, y_distance = map(float,map(str,data.split(','))) 
        #Move the robot by the specified amount in milimetres.
        robot.moveX(x_distance)
        robot.moveY(y_distance)
        client.sendDone()