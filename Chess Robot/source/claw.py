from ev3dev.ev3 import *
from time import sleep

class Claw:
    def __init__(self, port = OUTPUT_B):
        self.motor = MediumMotor(port)
        self.motor.reset()
        #Close the gripper completely
        convergence_counter = 0
        time_delta = 0.01
        tachometer_reading = self.motor.position
        while convergence_counter < 3:
            self.motor.run_forever(speed_sp=-360)
            sleep(time_delta)
            if tachometer_reading == self.motor.position:
                convergence_counter = convergence_counter + 1
            tachometer_reading = self.motor.position
        self.motor.stop()
        #Gripper is closed at this point
        self.motor.run_to_rel_pos(position_sp=700, speed_sp = 360)
        sleep(3)
        self.isOpen = True

    def open(self):
        if not self.isOpen:
            self.motor.run_to_rel_pos(position_sp=700, speed_sp = 360)
            sleep(3)
            self.isOpen = True

    def close(self):
        if self.isOpen:
            self.motor.run_to_rel_pos(position_sp=-700, speed_sp = 360)
            sleep(3)
            self.isOpen = False

#if __name__ == "__main__":
