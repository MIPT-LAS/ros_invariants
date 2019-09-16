# import roslib; roslib.load_manifest('ros_invariants')
import rospy
import rostopic

class ConditionVariable:
    def __init__(self,name):
        self.name = name
        if name[0] != "/":
            name = "/" + name
        msg_class, real_topic, _ = rostopic.get_topic_class(name, blocking=True) #pause hz until topic is published
        self.sub = rospy.Subscriber(real_topic,msg_class,self.valuecb,queue_size=1)
        self.var = None
        self.count = 0
        self.lastcount = 0
        self.lasttime = -1.0
        self.cfreq = -1.0

    def valuecb(self,value):
        self.count += 1
        self.var = value

    def freq(self):
        if not self.var:
            return -1
        t = rospy.Time.now().to_sec()
        #print "Var %s: t %f c %d" % (self.var.getName(),t,cnt)
        if (self.lasttime < 0):
            self.lasttime = t
            self.lastcount = self.count
            return self.cfreq

        dt = t - self.lasttime
        if (dt == 0):
            return self.cfreq
        dc = self.count - self.lastcount
        if dc > 0:
            self.cfreq = dc/dt
            self.lasttime = t
            self.lastcount = self.count
        else:
            self.cfreq = 1/dt
        return self.cfreq

