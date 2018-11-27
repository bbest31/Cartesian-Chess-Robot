#!/usr/bin/python
# RUN ON LAPTOP USING PYTHON 3.6

#This class handles the Server side of the comunication between the laptop and the brick.

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
        


    #Sends set of angles to the brick via TCP. 
    #input: base_angle [Float]: The angle by which we want the base to move
    #       joint_angle [Float]: The angle by which we want to joint to move
    #       queue [Thread-safe Queue]: Mutable data structure to store (and return)
    #             the messages received from the client
    def sendAngles(self, x_motor_angle, y_motor_angle, queue):
        #Format in which the client expects the data
        # angle1    angle2
        print(str(x_motor_angle) +  " " + str(y_motor_angle))
        data = str(x_motor_angle)+","+str(y_motor_angle)
        print("Sending Data: (" + data + ") to robot.")
        self.cs.send(data.encode("UTF-8"))
        #Waiting for the client (ev3 brick) to let the server know
        #That it is done moving
        reply = self.cs.recv(128).decode("UTF-8")
        queue.put(reply)

    #Sends a termination message to the client. This will cause the client
    #to exit "cleanly", after stopping the motors.
    def sendTermination(self):
        self.cs.send("EXIT".encode("UTF-8"))



