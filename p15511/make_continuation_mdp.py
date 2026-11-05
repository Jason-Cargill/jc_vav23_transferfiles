import os, sys

usage = """Usage: python make_continuation_mdp.py mdpfile starttime temp 

    DESCRIPTION  

    This script will read in an input *.mdp file, and return to
    standard output a version with the following settings altered:

        continuation = yes
        init-step    = [starttime]  ; nsteps_per_WU*gen
        gen_vel      = no 
        gen-temp     = [temp]  
        gen-seed     = -1

    EXAMPLE

        $ python make_continuation_mdp.py prod.mdp 2500000 300  > new.mdp

    INPUTS

        mdpfile        - input mdpfile
        starttime      - the starttime of the new WU  
        temp           - the temperature in K
"""

if len(sys.argv) < 4:
    print(usage)
    sys.exit(1)

# get input arguments
mdpfile = sys.argv[1]
starttime = sys.argv[2]
temp = sys.argv[3]

# Read in all lines of the mdpfile
fin = open(mdpfile, 'r')
lines = fin.readlines()
fin.close()

# go line-by-line, looking for keywords to change

found_continuation = False
found_init_step = False
found_gen_temp = False
found_gen_vel = False
found_gen_seed = False

for i in range(len(lines)):

    # strip out the comments
    cleanline = lines[i].split(';')[0]

    # make this a continuation run 
    if cleanline.count('continuation') > 0:
        lines[i] = 'continuation = yes\n'
        ### print('>>> changed:', lines[i])
        found_continuation = True

    # set the initial steps to be nsteps_per_WU*gen
    if cleanline.count('init-step') > 0:
        lines[i] = 'init-step = %s\n'%starttime
        ### print('>>> changed:', lines[i])
        found_init_step = True

    # generate new velocities
    if cleanline.count('gen_vel')+cleanline.count('gen-vel') > 0:
        lines[i] = 'gen_vel = no\n'
        ### print('>>> changed:', lines[i])
        found_gen_vel = True

    # use the specified temperature
    if cleanline.count('gen_temp')+cleanline.count('gen-temp') > 0:
        lines[i] = 'gen-temp = %s\n'%temp
        ### print('>>> changed:', lines[i])
        found_gen_temp = True

    # use a random seed
    if cleanline.count('gen-seed')+cleanline.count('gen_seed') > 0:
        lines[i] = 'gen-seed = -1\n'
        ### print('>>> changed:', lines[i])
        found_gen_seed = True

# If there are missing lines, add them
if not found_continuation:
    lines.append('continuation = yes\n')
if not found_init_step:
    lines.append('init-step = %s\n'%starttime)
if not found_gen_vel:
    lines.append('gen_vel = no\n')
if not found_gen_temp:
    lines.append('gen-temp = %s\n'%temp)
if not found_gen_seed:
    lines.append('gen-seed = -1\n')

# Write the result to standard output!
print(''.join(lines))

