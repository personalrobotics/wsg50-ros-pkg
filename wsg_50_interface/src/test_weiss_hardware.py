#!/usr/bin/env python

import rospy
from sensor_msgs.msg import JointState
from std_msgs.msg import Float64MultiArray, MultiArrayDimension

OPEN_WIDTH = -0.05
CLOSE_WIDTH = -0.01
LEFT_JOINT_IDX = 0

class TestWeissHardware:
  
  def __init__(self):
    self.cmd_pub = rospy.Publisher("/hand/joint_position_controller/command", Float64MultiArray, queue_size=1)
    self.joint_sub = rospy.Subscriber("joint_states", JointState, self.joint_cb, queue_size=1)
    
    self.cmd_pub.publish(self.gen_msg(OPEN_WIDTH))    
    
  def joint_cb(self, msg):
    width = msg.position[LEFT_JOINT_IDX]
    if width < 0.95*OPEN_WIDTH:
      self.cmd_pub.publish(self.gen_msg(CLOSE_WIDTH))  
    elif width > 1.05*CLOSE_WIDTH:
      self.cmd_pub.publish(self.gen_msg(OPEN_WIDTH))     
      
  def gen_msg(self, val):
    fa = Float64MultiArray()
    mad = MultiArrayDimension()
    mad.label = 'commands'
    mad.size = 2
    mad.stride = 2
    fa.layout.dim = [mad]
    fa.layout.data_offset = 0
    fa.data = [val, val]
    return fa
   
    
  
    
if __name__ == '__main__':
  rospy.init_node("test_weiss_hardware")
  
  print 'Waiting for hand to start up'
  rospy.sleep(5.0)
  
  print 'Going to start test'
  twh = TestWeissHardware()
  
  rospy.spin()
  

