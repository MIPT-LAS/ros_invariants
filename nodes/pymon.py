#!/usr/bin/python
#import roslib; 
# roslib.load_manifest('ros_invariants')
import rospy

import sys
import re
import time
import getopt
from math import *

from ros_invariants.Monitor import *

###### Option parsing ###################

def printhelp():
    print "Usage: %s [-h] [-p] [-g] <condition file>" % sys.argv[0]
    print "-p,--protect: load file outside an exception block (debug)"
    print "-g,--gui    : load the gui"
    print "-r,--reorder: reorder statements to show fail on top"
    print "-h,--help   : print this message"
    print "Alternatively, all the arguments can be set through ROS params"
    sys.exit(1)

# if (len(sys.argv) < 2):
#     printhelp()

opts,args=getopt.getopt(sys.argv[1:],"pgrh",["protect","gui","reorder","help"])

# if (len(args) != 1):
#     printhelp()

textonly=True
protect=True
reorder=False
#print opts
for o,a in opts:
    if o == "-g":
        textonly = False
    if o == "-r":
        reorder = True
    if o == "-p":
        protect = False
    if o == "-h":
        printhelp()


#######################################################3333###

rospy.init_node("invariants")
textonly = rospy.get_param("~textonly",textonly)
reorder = rospy.get_param("~reorder",reorder)
protect = rospy.get_param("~protect",protect)
condfile = rospy.get_param("~conditions","")

if len(condfile)>0:
    args=[condfile]

if len(args) != 1:
    rospy.logerr("Error: config file not defined")
    printhelp()


pub = rospy.Publisher("~status",InvariantStatus,queue_size=1)
monitor = Monitor(pub)
if protect:
    try:
        monitor.load(args[0])
    except Exception,inst:
        rospy.logerr("Error opening config file '%s': %s" % (str(args),str(inst)))
        sys.exit(1)
else:
    monitor.load(args[0])

time.sleep(1)
R=monitor.evaluate()


################## Main loop #################

if textonly:
    try:
        while not rospy.is_shutdown():
            R=monitor.evaluate()
            #monitor.printEvaluation(R[0],R[1])
            if (len(R['error']) > 0):
                if (len(R['error']) > 1):
                    rospy.logwarn("Warning these conditions are not verified:")
                else:
                    rospy.logwarn("Warning this condition is not verified:")
                for s in R['error']:
                    if len(s['comment'])>0:
                        rospy.logwarn("\t" + s['condition'] + "\n\t(" + s['comment'] + ")")
                    else:
                        rospy.logwarn("\t" + s['condition'])
            time.sleep(0.5)
    except Exception,inst:
        rospy.loginfo("Monitor interrupted: " + str(inst))
else:
    from ros_invariants.CondMonitorGUI import *
    #print "starting GUI"
    MonitorGUI = MonitorGUIMain(monitor,reorder,0)
    MonitorGUI.MainLoop()





