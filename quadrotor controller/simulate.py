from __future__ import print_function
from quadrotorController import controller

M = controller()
for i in xrange(100):
    input_values = {"searchTheEgg": False, "comEmiterOperational": False}
    #input_values = {"searchTheEgg": False, "cameraOperational": False, "enoughBrightness": False, "lightsOperational": False, "comEmiterOperational": False}
    print(M.move(**input_values))