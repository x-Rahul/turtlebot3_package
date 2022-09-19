#!/usr/bin/env python3

import rospy
from std_msgs.msg import String


def Callback(data):
    rospy.loginfo(rospy.get_caller_id() + f"Subscriberer Node Started, now Recieving messages/data... {data.data}") # To print on the terminal
    
def listener():
    rospy.init_node('subscirber_node', anonymous=True) # Defining the ros node - publish node
    sub = rospy.Subscriber('talking_topic', String, Callback) # Defining the Publisher by Topic, Message type
    rospy.spin() # python file runs infinitely


if __name__ == '__main__':
    try:
        listener()
    except rospy.ROSInterruptException:
        pass

