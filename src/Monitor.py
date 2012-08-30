import roslib; roslib.load_manifest('invariants')
import rospy

from CondVariable import *
from Condition import *
from invariants.msg import *

class Monitor:
    conditions=[]
    rosvars={}
    numCond = 0

    def __init__(self,pub=None):
        self.conditions=[]
        self.rosvars=[]
        self.numCond = 0
        self.files = 0
        self.pub = pub

    def apply_dict(self,s,d):
        for v in d.keys():
            s = re.sub(v,d[v],s)
        return s


    def include(self,fname,subst={}):
        global env
        # to be protected agains infinite recursion
        self.files += 1
        if self.files > 30:
            rospy.logerr("Too many include, or recursive loop")
            return []

        # Mechanism for multiple default path
        possible_name = [ fname ]
        for f in possible_name:
            try:
                fp=open(f)
                break
            except: 
                continue


        # Read all in on shot,
        cond = fp.readlines()
        fp.close()

        # Then process line by line
        i = -1
        res = []
        comment = ""
        while (i+1 < len(cond)):
            i += 1
            # Remove any white line and apply the translation dictionary
            l = self.apply_dict(cond[i].strip(),subst)
            if (len(l) == 0):
                continue
            if (l[0]=='#') or (l[0]=='%'):
                comment = l
                continue

            # don't accept a line with a single =, we don't want to affect anything
            if (re.search('[^=><!]=[^=]',l)):
                rospy.logwarn("line '%s' rejected due to a single '='" % l)
                continue

            # identify an include and try to start a recursive call
            if (re.match('\Ainclude(.*)\Z',l)):
                try:
                    cond[i:i+1] = eval("self.%s" % l)
                    i -= 1
                    continue
                except Exception,inst:
                    rospy.logerr("Ignored %s: exception '%s'" % (l,str(inst)))
            res.append({'condition':l,'comment':comment})
            comment = ""

        return res


    def load(self,fname):
        cond = self.include(fname)
        
        vars=set()
        for l in cond:
            c = Condition(l['condition'],l['comment'])
            self.conditions.append(c)
            vars.update(c.extractVars())

        for c in self.conditions:
            c.createEvalText(vars)
            
        self.numCond = len(self.conditions)
        rospy.loginfo("Monitoring %d condition(s)" % len(self.conditions))
        for l in self.conditions:
            rospy.loginfo("\t"+str(l))
        rospy.loginfo("Found %d vars" % len(vars))

        self.rosvars={}
        for v in vars:
            try:
                self.rosvars[v] = ConditionVariable(v)
            except e:
                rospy.logerr("Could not access to variable '%s'" % v)
                raise
        
    def evaluate(self):
        lfail=[]
        lsuccess=[]
        lall=[]
        for c in self.conditions:
            cd = {'condition':c.text,'comment':c.comment}
            if c.evaluate(self.rosvars):
                lall.append({'success':True,'index':len(lsuccess)})
                lsuccess.append(cd)
            else:
                lall.append({'success':False,'index':len(lfail)})
                lfail.append(cd)
        if self.pub:
            istat = InvariantStatus()
            istat.header.stamp = rospy.Time.now()
            istat.valid = lsuccess
            istat.fail = lfail
            self.pub.publish(istat)
        d={}
        d['all'] = lall
        d['error'] = lfail
        d['success'] = lsuccess
        return d

    def numConditions(self):
        return self.numCond

    def numComments(self):
        count = 0
        for c in self.conditions:
            if len(c.comment)>0:
                count += 1
        return count

    def printEvaluation(self,fail,success):
        print "Failed conditions:"
        for c in fail:
            print "\t"+c.comment
            print "\t\t"+str(c)
        print "Successful conditions:"
        for c in success:
            print "\t"+str(c)




        
