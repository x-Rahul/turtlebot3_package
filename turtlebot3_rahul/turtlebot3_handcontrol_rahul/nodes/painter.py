import cv2 as cv
import handTrackingModule as htm
import numpy as np
import time
import os

# 1. Import Images
# 2. Find Hand handLandmarks
# 3. check which fingers are up
# 4. If Selection Mode - 2 finger are up
# 5. If Drawing mode - Index finger up

#----
# Variables
brushSize = 15
eraserSize = 50
#----

# Colors--
green = (0, 255, 0)
purple = (255, 0, 255)
blue = (255, 0, 0)
red =  (10, 10, 230)
orange = (15, 97, 212)
indigo = (130, 0, 75)
yello = (60, 210, 245)
cyan = (180, 180, 15)
white = (255, 255, 255)
black = (0,0,0)
drawColor = white

# Import Images--
# folderPath = 'D:\Programming\Python\Resources\Images\Painter'
folderPath = '/home/dev-r/Documents/Resources/Images/Painter' # ubuntu
campath = 'https://10.150.32.40:8080/video'
myList = os.listdir(folderPath)
print(myList)
imgList = []
for imPath in myList:
    image = cv.imread(f'{folderPath}\{imPath}')
    imgList.append(image)
#--

detector = htm.handDetector(detectionCon=0.85)
cap = cv.VideoCapture(campath)
canvas = np.zeros((720,1280,3), np.uint8)

xp, yp = 0, 0
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
            cv.circle(img, ((x1+x2)//2, (y1+y2)//2), 30, drawColor, 3)
            xp, yp = 0, 0
            if y1 < 150:
                img[0:100, 0:1280] = imgList[0]
                if 270 < x1 < 385:
                    img[0:100, 0:1280] = imgList[6]
                    canvas[0:100, 0:1280] = imgList[6]
                    drawColor = black
                if 430 < x1 < 525:
                    img[0:100, 0:1280] = imgList[5]
                    canvas[0:100, 0:1280] = imgList[5]
                    drawColor = red
                if 570 < x1 < 665:
                    img[0:100, 0:1280] = imgList[4]
                    canvas[0:100, 0:1280] = imgList[4]
                    drawColor = cyan
                if 710 < x1 < 800:
                    img[0:100, 0:1280] = imgList[3]
                    canvas[0:100, 0:1280] = imgList[3]
                    drawColor = green
                if 840 < x1 < 945:
                    img[0:100, 0:1280] = imgList[2]
                    canvas[0:100, 0:1280] = imgList[2]
                    drawColor = blue
                if 980 < x1 < 1075:
                    img[0:100, 0:1280] = imgList[1]
                    canvas[0:100, 0:1280] = imgList[1]
                    drawColor = yello
            
            
        if index and middle == False:

            print("Drawing mode")
            if y1 < 125:
                pass
            else:
                
                cv.circle(img, (x1, y1), 5, drawColor, cv.FILLED)
                cv.circle(img, (x1, y1), 15, drawColor, 2)

                if xp == 0 and yp == 0:
                    xp, yp = x1, y1
                cv.line(img, (xp, yp), (x1, y1), drawColor, brushSize)
                cv.line(canvas, (xp, yp), (x1, y1), drawColor, brushSize)


                if drawColor == black:              
                    cv.line(img, (xp, yp), (x1, y1), drawColor, eraserSize)
                    cv.line(canvas, (xp, yp), (x1, y1), drawColor, eraserSize)
                else:  
                    cv.line(img, (xp, yp), (x1, y1), drawColor, brushSize)
                    cv.line(canvas, (xp, yp), (x1, y1), drawColor, brushSize)
                xp, yp = x1, y1

            # Clear Canvas when all fingers are up
        if all (x >= 1 for x in fingers):
            canvas = np.zeros((720, 1280, 3), np.uint8)
    
    imgGray = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)
    _, imgInv = cv.threshold(imgGray, 50, 255, cv.THRESH_BINARY_INV)
    imgInv = cv.cvtColor(imgInv, cv.COLOR_GRAY2BGR)
    img = cv.bitwise_and(img, imgInv)
    img = cv.bitwise_or(img, canvas)
   
    cv.imshow("Output", img)
    cv.imshow("Canvas", canvas)
    
    if cv.waitKey(1) & 0xFF == ord('x'):
        break
cap.release()
cv.destroyAllWindows()