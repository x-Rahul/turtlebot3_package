#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist

rospy.init_node('handtrack_node') # Defining the ros node - publisher node
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10) # Defining the Publisher by Topic, Message type


twist = Twist()
twist.linear.x = 0.5 # velocity
twist.angular.z = 0.5

while not rospy.is_shutdown():
    pub.publish(twist)
    rospy.Rate(2).sleep()
