from queue import Queue
from server import *

#Thread-safe queue to get data from threads
queue = Queue()
server = Server(9999)

server.sendDistances(-76,-138, queue)
server.sendLowerClaw()
server.sendCloseClaw()
server.sendRaiseClaw()
server.sendDistances(0,-38,queue)
server.sendLowerClaw()
server.sendOpenClaw()
server.sendRaiseClaw()



#yMotor = LargeMotor(OUTPUT_A)
#xMotor = LargeMotor(OUTPUT_C)
#zMotor = LargeMotor(OUTPUT_D)
#gripperMotor = MediumMotor(OUTPUT_B)