#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
# from turtlebot3_handcontrol_rahul.msg import Position


import cv2 as cv
import handTrackingModule as htm
import time

def talk_to_me():
    pub = rospy.Publisher('talking_topic', String, queue_size=10) # Defining the Publisher by Topic, Message type
    rospy.init_node('publisher_node', anonymous=True) # Defining the ros node - publish node
    rate = rospy.Rate(1) #1 hz - frequency at which the publishing occur
    rospy.loginfo("Publisher Node Started, now publishing messages...") # To print on the terminal
    while not rospy.is_shutdown():

        pTime = 0
        cTime = 0
        campath = 'https://10.150.32.40:8080/video'
        path = '/home/dev-r/Documents/ROS/vision_ws/src/tutorial/vision/Resources/Videos/cat.mp4'
        cap = cv.VideoCapture(campath)
        detector = htm.handDetector()
        while True:
            isTrue, frame = cap.read()
            img = cv.resize(frame, (640,480))

            img = detector.findHands(img, True)
            lmList = detector.findPosition(img)

            if len(lmList) != 0:
                print(lmList[8])
       
                msg = "Index finger Tip : "
                msg.x = lmList[8][1]
                msg.y = lmList[8][2]
                pub.publish(msg) # MAIN PUBLISHING
                rate.sleep()

            
            #FPS
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv.putText(img, str(int(fps)), (5, 20), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

            cv.imshow("webCam", img)
            if cv.waitKey(1) & 0xFF == ord('x'):
                break
            
        cap.release()
        cv.destroyAllWindows()
    
if __name__ == '__main__':
    try:
        talk_to_me()
    except rospy.ROSInterruptException:
        pass
