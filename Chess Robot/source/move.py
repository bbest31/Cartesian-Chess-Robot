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


# robot = Robot()

# robot.xMotor.run_to_rel_pos(position_sp=-360,speed_sp=230)