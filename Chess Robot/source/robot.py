from ev3dev2.motor import *
from ev3dev2.sensor.lego import *
from time import sleep
from claw import *

class Robot:
    def __init__(self):
        self.millimetersPerTickY = 0.14444444
        #self.millimetersPerTickX = 0.05833333
        self.millimetersPerTickX = 0.0642
        self.yOffset = 100
        self.yMotor = LargeMotor(OUTPUT_A)
        self.yMotor.stop_action = 'brake'
        self.xMotor = LargeMotor(OUTPUT_C)
        self.zMotor = LargeMotor(OUTPUT_D)
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
        
    def __del__(self):
        self.stop()
        
    def openClaw(self):
        self.claw.open()

    def closeClaw(self):
        self.claw.close()

    def homeX(self):
        degrees = -(self.currentX/self.millimetersPerTickX)
        self.xMotor.on_for_degrees(SpeedPercent(23), abs(degrees))
        self.xMotor.stop()
        self.currentX = 0

    def homeY(self):
        degrees = (self.currentY/self.millimetersPerTickY)
        self.yMotor.on_for_degrees(SpeedPercent(23),abs(degrees))
        self.yMotor.stop()
        self.currentY = 0

    def moveX(self, milli):
        degrees = abs(milli)/self.millimetersPerTickX
        if(milli < 0):
            self.xMotor.on_for_degrees(SpeedPercent(-23),degrees)
        else:
            self.xMotor.on_for_degrees(SpeedPercent(23),degrees)
        self.xMotor.stop()
        self.currentX += milli

    def moveY(self, milli):

        degrees = abs(milli)/self.millimetersPerTickY
        if(milli < 0):
            self.yMotor.on_for_degrees(SpeedPercent(-23),degrees)
        else:
            self.yMotor.on_for_degrees(SpeedPercent(23),degrees)

        self.yMotor.stop()
        self.currentY += milli

    def clawUp(self):
        self.zMotor.run_to_rel_pos(position_sp=-120, speed_sp = 50, stop_action="hold")
        sleep(1.8)
        self.zMotor.stop()

    def clawDown(self):
        self.zMotor.run_to_rel_pos(position_sp=120, speed_sp = 50, stop_action="coast")
        sleep(3.5)
        self.zMotor.stop()

    def stop(self):
        self.yMotor.reset()
        self.xMotor.reset()
        self.zMotor.reset()
        self.claw.stop()

