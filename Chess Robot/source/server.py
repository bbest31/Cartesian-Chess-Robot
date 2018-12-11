#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

#This class handles the Server side of the comunication between the laptop and the brick via TCP sockets

import socket
import time
from queue import Queue

class Server:
    def __init__(self,port):
       # setup server socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #We need to use the ip address that shows up in ipconfig for the usb ethernet adapter
        #That handles the comunication between the PC and the crick
        host = "169.254.137.85"
        print ("host: ", host)                        
        port = 9999
        serversocket.bind((host, port))                                  
        # queue up to 5 requests
        serversocket.listen(5) 
        self.cs,addr = serversocket.accept()  
        print ("Connected to: " +str(addr) )
        


    #Sends a distance tuple to the brick via TCP. 
    #input: x_distance [Float]: The distance in milimitres by which we want the X axis to move (sign determines direction)
    #       y_distance [Float]: The distance in milimitres by which we want the Y axis to move (sign determines direction)
    def sendDistances(self, x_distance, y_distance):
        #Format in which the client expects the data
        # x_distance,y_distance
        data = str(x_distance)+","+str(y_distance)
        print("Sending Data: (" + data + ") to robot.")
        self.cs.send(data.encode("UTF-8"))
        #Waiting for the client (ev3 brick) to let the server know
        #That it is done moving
        reply = self.cs.recv(128).decode("UTF-8")

    #Sends a termination message to the client. This will cause the client
    #to exit "cleanly", after stopping the motors.
    def sendTermination(self):
        self.cs.send("EXIT".encode("UTF-8"))

    def sendLowerClaw(self):
        self.cs.send("LOWER_CLAW".encode("UTF-8"))
        time.sleep(3.5)
    
    def sendRaiseClaw(self):
        self.cs.send("RAISE_CLAW".encode("UTF-8"))
        time.sleep(3.5)

    def sendOpenClaw(self):
        self.cs.send("OPEN_CLAW".encode("UTF-8"))
        time.sleep(3.5)

    def sendCloseClaw(self):
        self.cs.send("CLOSE_CLAW".encode("UTF-8"))
        time.sleep(3.5)

    #Send message to the brick via TCP with the home command.
    #This will make sure that the brick sends both the X and Y axis to their initial positions
    def sendHome(self):
        self.cs.send("HOME".encode("UTF-8"))
        reply = self.cs.recv(128).decode("UTF-8")




