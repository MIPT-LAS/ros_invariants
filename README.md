ros-invariants
==============

Ros tools to monitor system invariants

Run in text mode:
rosrun ros_invariants pymon.py <invariants.conf>

Start the GUI
rosrun ros_invariants pymon.py -g <invariants.conf>

Invariants are any one-line equations that can be evaluated as boolean by
python, without any affectation. Variables referring to topic names are
automatically detected and subscribed to. 

Example configuration files can be found in the test and scripts directories.
