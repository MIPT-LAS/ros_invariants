
import roslib; roslib.load_manifest('ros_invariants')
import rospy

from math import *
import re

class Condition:
    text=""
    etext=""

    def __init__(self,line,comment):
        self.comment=comment
        self.text=line
        self.etext=""

    def __str__(self):
        return self.text

    def extractVars(self):
        predef = set(['freq','and','or'])
        vars = set()
        # this matches a word starting by a letter, not preceded by a letter,
        # a dot or a square bracket, and followed by letter or number
        potvar = re.findall('(?<![.\]a-zA-Z0-9_])[a-zA-Z][a-zA-Z0-9_]*',self.text)
        #print "predef: " + str(predef)
        #print "potvar: " + str(potvar)
        for v in potvar:
            if v in predef:
                continue
            try:
                t=eval("type(%s)" % v)
            except:
                vars.add(v)
        return vars

    def createEvalText(self,vars):
        self.etext = self.text
        for v in vars:
            self.etext = re.sub("(?<![.\]a-zA-Z0-9_])%s"%v,"rosvar['%s'].var"%v,self.etext)
            self.etext = re.sub("(freq\(rosvar\['[A-Za-z0-9_]*'\]).var\)",r"\1)",self.etext)

    def evaluate(self,rosvar):
        #print "Evaluating " + self.etext
        def freq(cv):
            try:
                f = cv.freq()
                #print "Var %s: freq %f" % (v.getName(),f)
                return f
            except Exception,inst:
                rospy.logerr("freq exception: " + str(inst))
                return -1
        try:
            return bool(eval(self.etext))
        except Exception,inst:
            if not re.search("'NoneType' object",str(inst)):
                rospy.logwarn("eval exception: " + str(inst))
            return False







