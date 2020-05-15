from tulip import transys
from tulip import spec
from tulip import synth
from tulip import dumpsmach
import logging
# 
# The system is modeled as a discrete transition system.
# The Segway can be located anyplace on a 4x2 grid of cells. 
# Segway can be recharged at X0.
# The Segway is allowed to transition between any two adjacent cells;
# diagonal motions are not allowed. The Segway should continuously revisit the Egg cell X7.
# The environment consists of a single state called 'moveToTheEgg' that
# indicates that the quadrotor should move to cell X7.
#    --------------
#    -- X0 -- X4 --     Segway: X0 
#    -- X1 -- X5 --     Egg: X7
#    -- X2 -- X6 --     1 turtle robot (moving obstacle): X1-X2
#    -- X3 -- X7 --
#    --------------

# We must convert this specification into GR(1) form:
#  env_init && []env_safe && []<>env_prog_1 && ... && []<>env_prog_m ->
#      sys_init && []sys_safe && []<>sys_prog_1 && ... && []<>sys_prog_n

# Environment specification
# The environment can issue a searchTheEgg signal that the robot must respond
# to by moving to the lower right corner of the physicalGrid.  We assume that
# the searchTheEgg signal is turned on infinitely often.
env_vars = {}
env_vars['moveToTheEgg'] = 'boolean' #corresponds to the quadrotor is landed on the segway and eggCoordinates has been received
env_vars['turtleRobotLocation'] = (1, 2)
env_init = set() #env_vars initialized in the simulate.py document
env_prog = {'moveToTheEgg'} #[]<>
env_safe = set()
env_safe = {
            '(turtleRobotLocation = 1) -> X (turtleRobotLocation = 2 || turtleRobotLocation = 1)',
            '(turtleRobotLocation = 2) -> X (turtleRobotLocation = 2 || turtleRobotLocation = 1)',
           } 

# System dynamics
# The system dynamics describes how the system is allowed to move
# and what the system is required to do in response to an environmental
# action.
sys_vars = {}
sys_vars['segwayLocation'] = (0, 7)
sys_vars['X7reach'] = 'boolean'
sys_vars['batteryLevel'] = (0, 15)
sys_safe = {
            '(segwayLocation = 0) -> X (segwayLocation = 0 || segwayLocation = 4 || segwayLocation = 1)',
            '(segwayLocation = 1) -> X (segwayLocation = 1 || segwayLocation = 0 || segwayLocation = 5 || segwayLocation = 2)',
            '(segwayLocation = 2) -> X (segwayLocation = 2 || segwayLocation = 1 || segwayLocation = 6 || segwayLocation = 3)',
            '(segwayLocation = 3) -> X (segwayLocation = 3 || segwayLocation = 2 || segwayLocation = 7)',
            '(segwayLocation = 4) -> X (segwayLocation = 4 || segwayLocation = 0 || segwayLocation = 5)',
            '(segwayLocation = 5) -> X (segwayLocation = 5 || segwayLocation = 4 || segwayLocation = 1 || segwayLocation = 6)',
            '(segwayLocation = 6) -> X (segwayLocation = 6 || segwayLocation = 5 || segwayLocation = 2 || segwayLocation = 7)',
            '(segwayLocation = 7) -> X (segwayLocation = 7 || segwayLocation = 6 || segwayLocation = 3)',
                       
            'batteryLevel > 0',
            '!(segwayLocation = 0 && X segwayLocation = 0) <-> (X batteryLevel = batteryLevel -1)',
            '(segwayLocation = 0 && X segwayLocation = 0) <-> (X batteryLevel = batteryLevel +1)', 
            
            '(turtleRobotLocation = 1) -> !(segwayLocation=1)', 
            '(turtleRobotLocation = 2) -> !(segwayLocation=2)',
            }
sys_prog = set()               

# System specification
#
# The system specification is that the segway should repeatedly revisit
# the upper left corner of the grid while at the same time responding
# to the moveToTheEgg signal by visiting the lower right corner.  The LTL
# specification is given by
#
#     []<> X0 && [](moveToTheEgg -> <>X7) && [](!moveToTheEgg -> <>X0)
#
# Since this specification is not in GR(1) form, we introduce three
# environment variables X7reach X6reach X3 reach that are initialized to True and the specification :
#      [](moveToTheEgg -> <>X7)
# becomes :
#      [](X (X7reach) <-> (X7)) || (X7reach && !moveToTheEgg), 
#    
# Augment the system description to make it GR(1)
sys_init = {'X7reach', 'batteryLevel = 15', 'segwayLocation = 0'} #does not work with 2x sys_init ={...}
sys_safe |= {
            '(X (X7reach) <-> (segwayLocation=7)) || (X7reach && !moveToTheEgg)',
            }
sys_prog |= {'X7reach', 'segwayLocation = 0'}

# Create a GR(1) specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init, env_safe, sys_safe, env_prog, sys_prog)

specs.moore = True
specs.qinit = '\E \A'

# Controller synthesis
ctrl = synth.synthesize('omega', specs)
assert ctrl is not None, 'unrealizable'

dumpsmach.write_python_case("segwayController.py", ctrl, classname="controller")