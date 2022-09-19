import cv2 as cv
import handTrackingModule as htm
import numpy as np
import time
import os

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
cap = cv.VideoCapture(0)

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
            print("Selection mode")
            cv.circle(img, ((x1+x2)//2, (y1+y2)//2), 30, (255, 0, 0), 3)

            if ( y1 < 200) and (x1 < 830 and x1 > 450):
                print("print forward")
            if (y1 > 510) and (x1 < 830 and x1 > 450):
                print("print backward")
            if (y1 > 200 and y1 < 510) and (x1 < 370):
                print("print Left")
            if (y1 > 200 and y1 < 510) and (x1 > 900):
                print("print Right")
            
            
        if index and middle == False:
            print("Move")
        
        # stop when all fingers are up
        if all (x >= 1 for x in fingers):
            print("command to stop")

    cv.imshow("Output", img)
    if cv.waitKey(1) & 0xFF == ord('x'):
        break
cap.release()
cv.destroyAllWindows()