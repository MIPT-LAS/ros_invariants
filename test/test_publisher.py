#!/usr/bin/env python

# ====================================================================
#     Imports !
# ====================================================================  

# ROS specific imports
import roslib; 
# roslib.load_manifest('ros_invariants')
import rospy
import geometry_msgs.msg
import math



# ====================================================================
#     Definition of looping function ( BoatSimulatorLoop() )
# ====================================================================
def SimulatorLoop():

    # Initialize ROS stuff (Node, Publisher and Subscriber)
    rospy.init_node('test_publisher')

    pub1 = rospy.Publisher("topic1", geometry_msgs.msg.PointStamped,queue_size=1)
    pub2 = rospy.Publisher("topic2", geometry_msgs.msg.PointStamped,queue_size=1)
   
    rosrate = rospy.Rate(10) # in Hz

    # ----------MAIN LOOP !!!--------------------------------------------------
    while not rospy.is_shutdown():
        P1 = geometry_msgs.msg.PointStamped()
        P2 = geometry_msgs.msg.PointStamped()
        P1.header.stamp = rospy.Time.now()
        P2.header.stamp = P1.header.stamp
        tsec = P1.header.stamp.to_sec()
        P1.point.x = math.cos(tsec);
        P1.point.y = math.sin(tsec);
        P1.point.z = round(tsec/6) - math.floor(tsec/6)
        P2.point.x = -P1.point.x
        P2.point.y = -P1.point.y
        P2.point.z = 0

        pub1.publish(P1)
        if P1.point.z < 0.5:
            pub2.publish(P2)

        # sleep a little bit
        rosrate.sleep()

        
# ====================================================================
#     Main 
# ====================================================================
if __name__ == '__main__':
    try:
        SimulatorLoop()
    except rospy.ROSInterruptException: pass


