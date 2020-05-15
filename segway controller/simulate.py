from __future__ import print_function
from segwayController import controller

M = controller()
for i in xrange(100):
    input_values = {"moveToTheEgg": False, "turtleRobotLocation":2}
    print(M.move(**input_values))

