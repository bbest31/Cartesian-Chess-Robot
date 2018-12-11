from ev3dev2.motor import *
from time import sleep

'''
Class meant to abstract claw functionlaity, it handles claw initialization and calibration.
Also functions intrinsic to the claw such as opening and closing it.
'''

class Claw(MediumMotor):
    def __init__(self, port = OUTPUT_B):
        MediumMotor.__init__(self,port)
        self.reset()
        convergence_counter = 0
        time_delta = 0.01
        tachometer_reading = self.position
        #Calibrate the claw by closing it until it is tight enough that the 
        #tachometer count wont increase anymore
        while convergence_counter < 3:
            self.on(-24)
            sleep(time_delta)
            if tachometer_reading == self.position:
                convergence_counter = convergence_counter + 1
            #Once the tachometer count hasn't increased for 3 iterations, we assume that the 
            #claw is tightly closed and record the current tachometer reading as our "starting" position
            #for the claw
            tachometer_reading = self.position
        self.stop()
        #Claw is closed at this point
        
        #By empirical measurements, we determined that the best input to send to the motor in order to open the claw was 700 degrees
        #We open the claw after the calibration.
        self.on_for_degrees(24,700)
        sleep(3)
        #Instance variable that keeps track of the current state of the claw. In order to avoid opening it or closing it too much.
        self.isOpen = True

    #Open the claw by moving the motor 700 degrees clockwise. This will only run if the claw is not open
    def open(self):
        if not self.isOpen:
            self.on_for_degrees(24,700)
            sleep(3)
            self.isOpen = True

    #Close the claw by moving the motor 700 degrees counter clockwise. This will only run if the claw is open
    def close(self):
        if self.isOpen:
            self.on_for_degrees(-24,700)
            sleep(3)
            self.isOpen = False

    def stop(self):
        self.reset()

