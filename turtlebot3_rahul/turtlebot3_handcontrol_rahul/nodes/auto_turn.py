#!/usr/bin/env python3

from shutil import move
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


dist_obs = 1

def Callback(msg):
    
    rospy.loginfo(rospy.get_caller_id() + f"Obstacle distance : {msg.ranges[300]}")

    # Condition : If the distance to obstacle is less than 1m then move forward
    if msg.ranges[300] > dist_obs:
        print("In")
        twist.linear.x = 0.5
        twist.linear.z = 0.0
    
    if msg.ranges[300] <= dist_obs:
        print("Out")
        twist.linear.x = 0
        twist.angular.z = 0.5

    pub.publish(twist)
    

rospy.init_node('autoturn') # Defining the ros node - publisher node
sub = rospy.Subscriber('/scan', LaserScan, Callback) # Subscribe to Laser Topic
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=2) # Defining the Publisher by Topic, Message type
rate = rospy.Rate(2)
twist = Twist()

rospy.spin()


