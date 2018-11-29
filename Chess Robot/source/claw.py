from ev3dev2.motor import *
from time import sleep

class Claw(MediumMotor):
    def __init__(self, port = OUTPUT_B):
        MediumMotor.__init__(self,port)
        self.reset()
        #Close the gripper completely
        convergence_counter = 0
        time_delta = 0.01
        tachometer_reading = self.motor.position
        while convergence_counter < 3:
            self.on(speed_sp=-24)
            sleep(time_delta)
            if tachometer_reading == self.position:
                convergence_counter = convergence_counter + 1
            tachometer_reading = self.position
        self.stop()
        #Gripper is closed at this point
        
        #self.motor.run_to_rel_pos(position_sp=700, speed_sp = 360)
        self.on_for_degrees(24,700);
        sleep(3)
        self.isOpen = True

    def open(self):
        if not self.isOpen:
            #self.motor.run_to_rel_pos(position_sp=700, speed_sp = 360)
            self.on_for_degrees(24,700);
            sleep(3)
            self.isOpen = True

    def close(self):
        if self.isOpen:
            #self.motor.run_to_rel_pos(position_sp=-700, speed_sp = 360)
            self.on_for_degrees
            sleep(3)
            self.isOpen = False

#if __name__ == "__main__":
