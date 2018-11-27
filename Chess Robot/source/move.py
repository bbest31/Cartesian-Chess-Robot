
from ev3dev.ev3 import *
import socket
from threading import Event, Thread
from time import sleep
from claw import *

#yMotor = LargeMotor(OUTPUT_A)
#xMotor = LargeMotor(OUTPUT_C)
#zMotor = LargeMotor(OUTPUT_D)
#gripperMotor = MediumMotor(OUTPUT_B)


#Y
#yMotor.run_to_rel_pos(position_sp=720, speed_sp = 230)
#sleep(3)
#yMotor.stop()
#X
#xMotor.run_to_rel_pos(position_sp=960, speed_sp = 230)
#sleep(3)
#xMotor.stop()
#Gripper
#gripperMotor.run_to_rel_pos(position_sp=500, speed_sp = 360)
#sleep(3)
#gripperMotor.stop()

#Gripper
#gripperMotor.run_to_rel_pos(position_sp=-500, speed_sp = 360)
#sleep(3)
#gripperMotor.stop()

#Z
#Upwards
#zMotor.run_to_rel_pos(position_sp=-120, speed_sp = 100, stop_action="hold")
##sleep(3)
zMotor.stop()


#Downwards




#gripperMotor.run_to_rel_pos(position_sp=-2000, speed_sp = 360)
#sleep(6)
#gripperMotor.stop()


#zMotor.run_to_rel_pos(position_sp=-120, speed_sp = 100, stop_action="hold")
#sleep(3)
#zMotor.stop()

#xMotor.run_to_rel_pos(position_sp=-960, speed_sp = 230)
#sleep(3)
#xMotor.stop()

#yMotor.run_to_rel_pos(position_sp=-420, speed_sp = 230)
#sleep(3)
#yMotor.stop()

#zMotor.run_to_rel_pos(position_sp=120, speed_sp = 100, stop_action="coast")
#sleep(3)
#zMotor.stop()


#gripperMotor.run_to_rel_pos(position_sp=700, speed_sp = 360)
#sleep(4)
#gripperMotor.stop()

zMotor.run_to_rel_pos(position_sp=-120, speed_sp = 100, stop_action="hold")
sleep(3)
zMotor.stop()


claw = Claw(OUTPUT_B)

zMotor.run_to_rel_pos(position_sp=120, speed_sp = 100, stop_action="coast")
sleep(3)
zMotor.stop()

claw.close()


zMotor.run_to_rel_pos(position_sp=-120, speed_sp = 100, stop_action="hold")
sleep(3)
zMotor.stop()

yMotor.run_to_rel_pos(position_sp=-420, speed_sp = 230)
sleep(3)
yMotor.stop()

zMotor.run_to_rel_pos(position_sp=120, speed_sp = 100, stop_action="coast")
sleep(3)
zMotor.stop()

claw.open()
#zMotor.reset()