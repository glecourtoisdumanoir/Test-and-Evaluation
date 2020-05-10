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
# diagonal motions are not allowed. The quadrotor should continuously revisit the Egg cell X7.
# The environment consists of a single state called 'searchTheEgg' that
# indicates that the quadrotor should move to cell X7.
#    --------------
#    -- X0 -- X4 --     Segway: X0, Egg: X7 || X3 || X6
#    -- X1 -- X5 --
#    -- X2 -- X6 --
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
# the searchTheEgg signal is turned off infinitely often.
env_vars = {}
env_vars['searchTheEgg'] = 'boolean'
#env_vars['comEmiterOperational'] = 'boolean'
env_init = set()
env_prog = {'searchTheEgg'} #[]<>
env_safe = set()

# System dynamics
# The system dynamics describes how the system is allowed to move
# and what the system is required to do in response to an environmental
# action.
sys_vars = {}
sys_vars['quadrotorLocation'] = (0, 7)
sys_vars['batteryLevel'] = (0, 10)
#sys_vars['X7visited'] = 'boolean'
#sys_vars['X6visited'] = 'boolean'
#sys_vars['X3visited'] = 'boolean'
sys_init = {'quadrotorLocation=0', 'batteryLevel=1'}
#sys_init = {"X7visited":False, "X6visited":False, "X3visited":False}

sys_safe = {
            '(quadrotorLocation = 0) -> X (quadrotorLocation = 0 || quadrotorLocation = 4 || quadrotorLocation = 1)',
            '(quadrotorLocation = 1) -> X (quadrotorLocation = 0 || quadrotorLocation = 5 || quadrotorLocation = 2)',
            '(quadrotorLocation = 2) -> X (quadrotorLocation = 1 || quadrotorLocation = 6 || quadrotorLocation = 3)',
            '(quadrotorLocation = 3) -> X (quadrotorLocation = 2 || quadrotorLocation = 7)',
            '(quadrotorLocation = 4) -> X (quadrotorLocation = 0 || quadrotorLocation = 5)',
            '(quadrotorLocation = 5) -> X (quadrotorLocation = 4 || quadrotorLocation = 1 || quadrotorLocation = 6)',
            '(quadrotorLocation = 6) -> X (quadrotorLocation = 5 || quadrotorLocation = 2 || quadrotorLocation = 7)',
            '(quadrotorLocation = 7) -> X (quadrotorLocation = 6 || quadrotorLocation = 3)',
            'batteryLevel > 0',
            '!(quadrotorLocation = 0 && X quadrotorLocation = 0) <-> (X batteryLevel = batteryLevel -1)',
            '(quadrotorLocation = 0 && X quadrotorLocation = 0) <-> (X batteryLevel = batteryLevel +1)',
            #'X X7reach <-> eggFound = eggFound +1,
            #'X X6reach <-> X X X6visited',
            #'X X3reach <-> X X X3visited',
            #'comEmiterOperational = True',
            }
sys_prog = set()                # empty set

# System specification
#
# The system specification is that the quadrotor should repeatedly revisit
# the upper left corner of the grid while at the same time responding
# to the searchTheEgg signal by visiting the lower right corner.  The LTL
# specification is given by
#
#     []<> X0 && [](searchTheEgg -> <>X7 && <>X3 && <>X6) && [](searchTheEgg -> <>X0)
#boolean
# Since this specification is not in GR(1) form, we introduce an
# environment variable X7reach that is initialized to True and the
# specification [](searchTheEgg -> <>X7 && <>X3 && <>X6) becomes
#
#     [](X (X7reach) <-> X7 || (X7reach && !searchTheEgg)), []((X0reach && !searchTheEgg) || X (X0reach) <-> X0))
#
# Augment the system description to make it GR(1)
#sys_vars['EggReach'] = 'boolean'
sys_vars['X7reach'] = 'boolean'
sys_vars['X6reach'] = 'boolean'
sys_vars['X3reach'] = 'boolean'
sys_init = {'X7reach', 'X6reach', 'X3reach'}
sys_safe |= {
            '(X (X7reach) <-> (quadrotorLocation=7)) || (X7reach && !searchTheEgg)', 
            '(X (X6reach) <-> (quadrotorLocation=6)) || (X6reach && !searchTheEgg)', 
            '(X (X3reach) <-> (quadrotorLocation=3)) || (X3reach && !searchTheEgg)',
            }
sys_prog |= {'X7reach', 'X6reach', 'X3reach', 'quadrotorLocation = 0'}

# Create a GR(1) specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)

specs.moore = True
specs.qinit = '\E \A'

# Controller synthesis
ctrl = synth.synthesize('omega', specs)
assert ctrl is not None, 'unrealizable'

dumpsmach.write_python_case("quadrotorController.py", ctrl, classname="controller")