from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from time import sleep
from claw import *

'''
This class abstracts the control of the robot. In includes all the necessary functions
'''


class Robot:
    def __init__(self):
        #How many milimeters the robot will move along the Y axis for each tick of the motor
        self.millimetersPerTickY = 0.14444444
        #How many milimeters the robot will move along the Y axis for each tick of the motor
        self.millimetersPerTickX = 0.0642
        #Once The robot is at the home position (with the end effector over the rook in a1) the robot will move yOffset milimetres
        #backwards for the camera to have clear view of the board.
        self.yOffset = 100

        self.yMotor = LargeMotor(OUTPUT_A)
        self.yMotor.stop_action = 'brake'
        self.xMotor = LargeMotor(OUTPUT_C)
        self.zMotor = LargeMotor(OUTPUT_D)
        #This two variables will keep track of the current position of the robot by logging the encoder changes from the
        #starting position.
        self.currentY = 0 
        self.currentX = 0

        self.xMotor.reset()
        self.yMotor.reset()
        self.zMotor.reset()

        #Lift the claw
        self.clawUp()
        #Home the X axis
        self.homeX()
        #Home the Y axis
        self.homeY()


        #After the claw has been lifted we initialze it
        self.claw = Claw()
        
    #Desturctor, to make sure all the stop actions of the motors are cleared when the program terminates    
    def __del__(self):
        self.stop()
    
    #Open end effector
    def openClaw(self):
        self.claw.open()

    #Close end effector
    def closeClaw(self):
        self.claw.close()

    #Return X axis to initial position
    def homeX(self):
        degrees = -(self.currentX/self.millimetersPerTickX)
        self.xMotor.on_for_degrees(SpeedPercent(23), abs(degrees))
        self.xMotor.stop()
        self.currentX = 0
    
    #Return Y axis to initial position
    def homeY(self):
        degrees = (self.currentY/self.millimetersPerTickY)
        self.yMotor.on_for_degrees(SpeedPercent(23),abs(degrees))
        self.yMotor.stop()
        self.currentY = 0

    #Input milli: float. Milimitres to move along the X axis. The sign will determine the direction (towards or away from the origin)
    #This function will move the robot the desired amount of milimetres (in the specified direction) at a constant speed of 23% the max speed of the motor
    def moveX(self, milli):
        degrees = abs(milli)/self.millimetersPerTickX
        if(milli < 0):
            self.xMotor.on_for_degrees(SpeedPercent(-23),degrees)
        else:
            self.xMotor.on_for_degrees(SpeedPercent(23),degrees)
        self.xMotor.stop()
        self.currentX += milli

    #Input milli: float. Milimitres to move along the Y axis. The sign will determine the direction (towards or away from the origin)
    #This function will move the robot the desired amount of milimetres (in the specified direction) at a constant speed of 23% the max speed of the motor
    def moveY(self, milli):
        degrees = abs(milli)/self.millimetersPerTickY
        if(milli < 0):
            self.yMotor.on_for_degrees(SpeedPercent(-23),degrees)
        else:
            self.yMotor.on_for_degrees(SpeedPercent(23),degrees)

        self.yMotor.stop()
        self.currentY += milli

    #This function will bring the end effector up and hold it there (otherwise it would drop because of gravity)
    #The distance that the end effector will go up is the maximum possible based on our design (More than that and some cables will get on the way)
    #It was determined empirically after multiple runs
    def clawUp(self):
        self.zMotor.run_to_rel_pos(position_sp=-170, speed_sp = 50, stop_action="hold")
        sleep(3.5)
        self.zMotor.stop()

    #This function will bring the end effector down to a certain level and then coast to let gravity finish lowering it
    #The constants in this function were determined empirically. The reason why we didn't want to force it to move 170 degrees downwards (even though its being moved upwards by that amount)
    #Is that the height of our chessboard varied a little bit at the centre, also if there was a piece in the way of the end effector going down, we
    #didnt wanted to exert force over that piece from above. Thats why decided to lower it to a certain point and then let gravity take over.
    def clawDown(self):
        self.zMotor.run_to_rel_pos(position_sp=100, speed_sp = 50, stop_action="coast")
        sleep(3.5)
        self.zMotor.stop()

    #Stop the robot, this will reset all the motors.
    def stop(self):
        self.yMotor.reset()
        self.xMotor.reset()
        self.zMotor.reset()
        self.claw.stop()

