#!/usr/bin/env python3

import cv2 as cv
import handTrackingModule as htm
import numpy as np
import time
import os


import rospy
from geometry_msgs.msg import Twist
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios

BURGER_MAX_LIN_VEL = 0.22
BURGER_MAX_ANG_VEL = 2.84

WAFFLE_MAX_LIN_VEL = 0.26
WAFFLE_MAX_ANG_VEL = 1.82

LIN_VEL_STEP_SIZE = 0.01
ANG_VEL_STEP_SIZE = 0.1

msg = """
Control Your TurtleBot3!
---------------------------
Moving around:
        w
   a    s    d
        x

w/x : increase/decrease linear velocity (Burger : ~ 0.22, Waffle and Waffle Pi : ~ 0.26)
a/d : increase/decrease angular velocity (Burger : ~ 2.84, Waffle and Waffle Pi : ~ 1.82)

space key, s : force stop

CTRL-C to quit
"""

e = """
Communications Failed
"""

def getKey():
    if os.name == 'nt':
        timeout = 0.1
        startTime = time.time()
        while(1):
            if msvcrt.kbhit():
                if sys.version_info[0] >= 3:
                    return msvcrt.getch().decode()
                else:
                    return msvcrt.getch()
            elif time.time() - startTime > timeout:
                return ''

    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def vels(target_linear_vel, target_angular_vel):
    return "currently:\tlinear vel %s\t angular vel %s " % (target_linear_vel,target_angular_vel)

def makeSimpleProfile(output, input, slop):
    if input > output:
        output = min( input, output + slop )
    elif input < output:
        output = max( input, output - slop )
    else:
        output = input

    return output

def constrain(input, low, high):
    if input < low:
      input = low
    elif input > high:
      input = high
    else:
      input = input

    return input

def checkLinearLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_LIN_VEL, WAFFLE_MAX_LIN_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_LIN_VEL, BURGER_MAX_LIN_VEL)

    return vel

def checkAngularLimitVelocity(vel):
    if turtlebot3_model == "burger":
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)
    elif turtlebot3_model == "waffle" or turtlebot3_model == "waffle_pi":
      vel = constrain(vel, -WAFFLE_MAX_ANG_VEL, WAFFLE_MAX_ANG_VEL)
    else:
      vel = constrain(vel, -BURGER_MAX_ANG_VEL, BURGER_MAX_ANG_VEL)

    return vel

if __name__=="__main__":
    if os.name != 'nt':
        settings = termios.tcgetattr(sys.stdin)

    rospy.init_node('turtlebot3_teleop')
    pub = rospy.Publisher('cmd_vel', Twist, queue_size=10)

    turtlebot3_model = rospy.get_param("model", "burger")

    status = 0
    target_linear_vel   = 0.0
    target_angular_vel  = 0.0
    control_linear_vel  = 0.0
    control_angular_vel = 0.0

    try:
        print(msg)
        while not rospy.is_shutdown():

            # # Import Images--
            # folderPath = 'D:\Programming\Python\Resources\Images\Painter'
            # myList = os.listdir(folderPath)
            # print(myList)
            # imgList = []
            # for imPath in myList:
            #     image = cv.imread(f'{folderPath}\{imPath}')
            #     imgList.append(image)
            # #--

            detector = htm.handDetector(detectionCon=0.85)
            path = '/home/dev-r/myTurtlebot_ws/src/turtlebot3_rahul/turtlebot3_handcontrol_rahul/Resources/Videos'
            camlink = 'https://172.16.137.2:8080/video'
            cap = cv.VideoCapture(camlink)

            while True:
                isTrue, img = cap.read()
                img = cv.flip(img, 1)
                img = cv.resize(img, (1280,720))
                # Find Landmark
                detector.findHands(img, draw = False)
                lmList =  detector.findPosition(img, draw=False)
                if len(lmList) != 0:
                    x1,y1 = lmList[8][1:]
                    x2,y2 = lmList[12][1:]
                    # Getting up fingers
                    fingers = detector.fingersUp()
                    thumb, index, middle, ring, pinky = fingers[0:5]

                    if index and middle and thumb == 0 and pinky == 0 and ring == 0:
                        # print("Selection mode")
                        cv.circle(img, ((x1+x2)//2, (y1+y2)//2), 30, (255, 0, 0), 3)

                        if ( y1 < 200) and (x1 < 830 and x1 > 450):
                            print("print forward")
                            #-----main
                            target_linear_vel = checkLinearLimitVelocity(target_linear_vel + LIN_VEL_STEP_SIZE)
                            status = status + 1
                            print(vels(target_linear_vel,target_angular_vel))
                            #------

                        if (y1 > 510) and (x1 < 830 and x1 > 450):
                            print("print backward")
                            target_linear_vel = checkLinearLimitVelocity(target_linear_vel - LIN_VEL_STEP_SIZE)
                            status = status + 1
                            print(vels(target_linear_vel,target_angular_vel))
                            

                        if (y1 > 200 and y1 < 510) and (x1 < 370):
                            print("print Left")
                            target_angular_vel = checkAngularLimitVelocity(target_angular_vel + ANG_VEL_STEP_SIZE)
                            status = status + 1
                            print(vels(target_linear_vel,target_angular_vel))
                        if (y1 > 200 and y1 < 510) and (x1 > 900):
                            print("print Right")
                            target_angular_vel = checkAngularLimitVelocity(target_angular_vel - ANG_VEL_STEP_SIZE)
                            status = status + 1
                            print(vels(target_linear_vel,target_angular_vel))
                                    
                        
                    if index and middle == False:
                        print("Move")
                    
                    # stop when all fingers are up
                    if all (x >= 1 for x in fingers):
                        print("command to stop")

                        target_linear_vel   = 0.0
                        control_linear_vel  = 0.0
                        target_angular_vel  = 0.0
                        control_angular_vel = 0.0
                        print(vels(target_linear_vel, target_angular_vel))

                    if status == 20 :
                        print(msg)
                        status = 0

                    twist = Twist()

                    control_linear_vel = makeSimpleProfile(control_linear_vel, target_linear_vel, (LIN_VEL_STEP_SIZE/2.0))
                    twist.linear.x = control_linear_vel; twist.linear.y = 0.0; twist.linear.z = 0.0

                    control_angular_vel = makeSimpleProfile(control_angular_vel, target_angular_vel, (ANG_VEL_STEP_SIZE/2.0))
                    twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = control_angular_vel

                    pub.publish(twist)

                cv.imshow("Output", img)
                if cv.waitKey(1) & 0xFF == ord('x'):
                    break
            cap.release()
            cv.destroyAllWindows()


    except:
        print(e)

    finally:
        twist = Twist()
        twist.linear.x = 0.0; twist.linear.y = 0.0; twist.linear.z = 0.0
        twist.angular.x = 0.0; twist.angular.y = 0.0; twist.angular.z = 0.0
        pub.publish(twist)

    if os.name != 'nt':
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
