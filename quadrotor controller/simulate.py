from __future__ import print_function
from quadrotorController import controller

M = controller()
for i in xrange(50):
    input_values = {"searchTheEgg": False}
    print(M.move(**input_values))