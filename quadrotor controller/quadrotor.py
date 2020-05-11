from tulip import transys
from tulip import spec
from tulip import synth
from tulip import dumpsmach
import logging
# 
# The system is modeled as a discrete transition system in which the
# quadrotor is firstly located on a segway. The quadrotor can be located anyplace on a 4x2 grid of cells. 
# Quadrotor can be recharged at the Segway.
# The quadrotor is allowed to transition between any two adjacent cells;
# diagonal motions are not allowed. The quadrotor should continuously revisit the Egg cells X7, X3 and X6.
# The environment consists of a single state called 'searchTheEgg' that
# indicates that the quadrotor should move to cells  X7/X6/X3.
#    --------------
#    -- X0 -- X4 --     Segway: X0 
#    -- X1 -- X5 --     Egg: X7 || X3 || X6
#    -- X2 -- X6 --     Wind: X2
#    -- X3 -- X7 --
#    --------------
#
# The system specification in its simplest form is given by
#  []<>searchTheEgg -> []<>X7 && []<>X3 &&[]<>X6 && [](!searchTheEgg -> <>X0) 

# We must convert this specification into GR(1) form:
#  env_init && []env_safe && []<>env_prog_1 && ... && []<>env_prog_m ->
#      sys_init && []sys_safe && []<>sys_prog_1 && ... && []<>sys_prog_n

# Environment specification
# The environment can issue a searchTheEgg signal that the robot must respond
# to by moving to the lower right corner of the physicalGrid.  We assume that
# the searchTheEgg signal is turned on infinitely often.
env_vars = {}
env_vars['searchTheEgg'] = 'boolean'
env_vars['wind'] = (1, 7)
env_init = set()  
env_prog = {'searchTheEgg'} #[]<>
env_safe = {'X wind = wind'} #static wind

# System dynamics
# The system dynamics describes how the system is allowed to move
# and what the system is required to do in response to an environmental
# action.
sys_vars = {}
sys_vars['quadrotorLocation'] = (0, 7)
sys_vars['eggCoordinatesSent'] = 'boolean'
sys_vars['eggLocationVisited'] = (0, 7) #does not work with [0, 3, 6, 7, 36, 37, 67, 367]
sys_vars['X7reach'] = 'boolean'
sys_vars['X6reach'] = 'boolean'
sys_vars['X3reach'] = 'boolean'
# [0, 3, 6, 7, 36, 37, 67, 367] is equivalent to ...
# [0, 1, 2, 3,  4,  5,  6,   7]

#, 6, 7, 36, 37, 67, 367
sys_vars['batteryLevel'] = (0, 15)
sys_safe = {
            '(quadrotorLocation = 0) -> X (quadrotorLocation = 0 || quadrotorLocation = 4 || quadrotorLocation = 1)',
            '(quadrotorLocation = 1) -> X (quadrotorLocation = 1 || quadrotorLocation = 0 || quadrotorLocation = 5 || quadrotorLocation = 2)',
            '(quadrotorLocation = 2) -> X (quadrotorLocation = 2 || quadrotorLocation = 1 || quadrotorLocation = 6 || quadrotorLocation = 3)',
            '(quadrotorLocation = 3) -> X (quadrotorLocation = 3 || quadrotorLocation = 2 || quadrotorLocation = 7)',
            '(quadrotorLocation = 4) -> X (quadrotorLocation = 4 || quadrotorLocation = 0 || quadrotorLocation = 5)',
            '(quadrotorLocation = 5) -> X (quadrotorLocation = 5 || quadrotorLocation = 4 || quadrotorLocation = 1 || quadrotorLocation = 6)',
            '(quadrotorLocation = 6) -> X (quadrotorLocation = 6 || quadrotorLocation = 5 || quadrotorLocation = 2 || quadrotorLocation = 7)',
            '(quadrotorLocation = 7) -> X (quadrotorLocation = 7 || quadrotorLocation = 6 || quadrotorLocation = 3)',
                       
            '(eggLocationVisited = 0 && quadrotorLocation != 7 && quadrotorLocation != 6 && quadrotorLocation != 3) -> X (eggLocationVisited = 0)',
            '(quadrotorLocation = 0 -> X eggLocationVisited = 0)',
            '(eggLocationVisited = 0 && quadrotorLocation = 3) -> X (eggLocationVisited = 1)', 
            '(eggLocationVisited = 0 && quadrotorLocation = 6) -> X (eggLocationVisited = 2)',
            '(eggLocationVisited = 0 && quadrotorLocation = 7)-> X (eggLocationVisited = 3)',
            '(eggLocationVisited = 1 && quadrotorLocation = 6) -> X (eggLocationVisited = 4)', 
            '(eggLocationVisited = 1 && quadrotorLocation = 7) -> X (eggLocationVisited = 5)',
            '(eggLocationVisited = 1 && quadrotorLocation != 7 && quadrotorLocation != 6 && quadrotorLocation != 0) -> X (eggLocationVisited = 1)',
            '(eggLocationVisited = 2 && quadrotorLocation = 3) -> X (eggLocationVisited = 4)',
            '(eggLocationVisited = 2 && quadrotorLocation = 7) -> X (eggLocationVisited = 6)',
            '(eggLocationVisited = 2 && quadrotorLocation != 7 && quadrotorLocation != 3 && quadrotorLocation != 0) -> X (eggLocationVisited = 2)',
            '(eggLocationVisited = 3 && quadrotorLocation = 3) -> X (eggLocationVisited = 5)',
            '(eggLocationVisited = 3 && quadrotorLocation = 6) -> X (eggLocationVisited = 4)',
            '(eggLocationVisited = 3 && quadrotorLocation != 6 && quadrotorLocation != 3 && quadrotorLocation != 0) -> X (eggLocationVisited = 3)',
            '(eggLocationVisited = 4 && quadrotorLocation = 7) -> X (eggLocationVisited = 7)',
            '(eggLocationVisited = 4 && quadrotorLocation != 7 && quadrotorLocation != 0) -> X (eggLocationVisited = 4)',
            '(eggLocationVisited = 5 && quadrotorLocation = 6) -> X (eggLocationVisited = 7)',
            '(eggLocationVisited = 5 && quadrotorLocation != 6) -> X (eggLocationVisited = 5)',
            '(eggLocationVisited = 6 && quadrotorLocation = 3) -> X (eggLocationVisited = 7)',
            '(eggLocationVisited = 6 && quadrotorLocation != 3 && quadrotorLocation != 0) -> X (eggLocationVisited = 6)',           
            '(eggLocationVisited = 7 && quadrotorLocation != 0) -> X (eggLocationVisited = 7)', 
            
            '(quadrotorLocation = 0 && eggLocationVisited = 7) <-> X (eggCoordinatesSent)',

            'batteryLevel > 0',
            '!(quadrotorLocation = 0 && X quadrotorLocation = 0) <-> (X batteryLevel = batteryLevel -1)',
            '(quadrotorLocation = 0 && X quadrotorLocation = 0) <-> (X batteryLevel = batteryLevel +1)', 
            
            'wind=2 -> !(quadrotorLocation=2)', 
            }
sys_prog = set()               

# System specification
#
# The system specification is that the quadrotor should repeatedly revisit
# the upper left corner of the grid while at the same time responding
# to the searchTheEgg signal by visiting the lower right corner.  The LTL
# specification is given by
#
#     []<> X0 && [](searchTheEgg -> <>X7 && <>X3 && <>X6) && [](!searchTheEgg -> <>X0)
#
# Since this specification is not in GR(1) form, we introduce three
# environment variables X7reach X6reach X3 reach that are initialized to True and the specification :
#     1. [](searchTheEgg -> <>X7 && <>X3 && <>X6)
# becomes :
#     1.1 [](X (X7reach) <-> (X7)) || (X7reach && !searchTheEgg), 
#     1.2 [](X (X6reach) <-> (X6)) || (X6reach && !searchTheEgg),
#     1.3 [](X (X3reach) <-> (X3)) || (X3reach && !searchTheEgg),
#
# Augment the system description to make it GR(1)
sys_init = {'X7reach', 'X6reach', 'X3reach', 'batteryLevel = 1', 'quadrotorLocation = 0', 'eggLocationVisited = 0', '!eggCoordinatesSent'} #does not work with 2x sys_init ={...}
sys_safe |= {
            '(X (X7reach) <-> (quadrotorLocation=7)) || (X7reach && !searchTheEgg)', 
            '(X (X6reach) <-> (quadrotorLocation=6)) || (X6reach && !searchTheEgg)', 
            '(X (X3reach) <-> (quadrotorLocation=3)) || (X3reach && !searchTheEgg)',
            }
sys_prog |= {'eggCoordinatesSent'} #send coordinates to the Segway

# Create a GR(1) specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)

specs.moore = True
specs.qinit = '\E \A'

# Controller synthesis
ctrl = synth.synthesize('omega', specs)
assert ctrl is not None, 'unrealizable'

dumpsmach.write_python_case("quadrotorController.py", ctrl, classname="controller")