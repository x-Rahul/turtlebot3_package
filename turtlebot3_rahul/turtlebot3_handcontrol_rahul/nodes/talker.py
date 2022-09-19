#!/usr/bin/env python3

import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('talking_topic', String, queue_size=10) # Defining the Publisher by Topic, Message type
    rospy.init_node('publisher_node', anonymous=True) # Defining the ros node - publish node
    rate = rospy.Rate(10) # hz - frequency at which the publishing occur
    rospy.loginfo("Publisher Node Started, Hi, I am Rahul (Publisher publishing messages/data...)") # To print on the terminal
    while not rospy.is_shutdown():
        msg = "Message -> Move" # TOPIC
        pub.publish(msg)
        rate.sleep()
       
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
