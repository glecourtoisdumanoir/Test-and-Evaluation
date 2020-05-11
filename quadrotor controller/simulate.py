from __future__ import print_function
from quadrotorController import controller

M = controller()
for i in xrange(100):
    input_values = {"searchTheEgg": False, "wind":2}
    print(M.move(**input_values))