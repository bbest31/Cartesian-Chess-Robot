from ev3dev.ev3 import *
from time import sleep

class Robot:
    def __init__(self):
        self.yTouchSensor = TouchSensor(INPUT_1)
        self.xTouchSensor = TouchSensor(INPUT_2)
        self.yMotor = LargeMotor(OUTPUT_A)
        self.xMotor = LargeMotor(OUTPUT_C)
        self.zMotor = LargeMotor(OUTPUT_D)

        #Home the X axis
        homeX()
        #Home the Y axis
        homeY()
        #Lift the claw
        clawUp()

        #After the claw has been lifted we initialze it
        self.claw = Claw()

    def openClaw(self):
        self.claw.open()

    def closeClaw(self):
        self.claw.close()

    def homeX(self):
        while not xTouchSensor.is_pressed:
            self.xMotor.run_forever(speed_sp=230)
        self.xMotor.stop()

    def homeY(self):
        while not yTouchSensor.is_pressed:
            self.yMotor.run_forever(speed_sp=230)
        self.yMotor.stop()

    def moveX(self, degrees):
        timer = degrees/230 + 0.1
        self.xMotor.run_to_rel_pos(position_sp=degrees, speed_sp = 230)
        sleep(timer)
        self.xMotor.stop()

    def moveY(self, degrees)
        timer = degrees/230 + 0.1
        self.yMotor.run_to_rel_pos(position_sp=degrees, speed_sp = 230)
        sleep(timer)
        self.yMotor.stop()

    def clawUp(self):
        self.zMotor.run_to_rel_pos(position_sp=-120, speed_sp = 100, stop_action="hold")
        sleep(1.8)
        self.zMotor.stop()

    def clawDown(self):
        self.zMotor.run_to_rel_pos(position_sp=120, speed_sp = 100, stop_action="coast")
        sleep(1.8)
        self.zMotor.stop()

