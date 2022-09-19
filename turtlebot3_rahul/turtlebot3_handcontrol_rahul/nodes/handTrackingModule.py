import cv2 as cv
import mediapipe as mp
import time


class handDetector():

    def __init__(self, mode = False, maxHands = 2, modelComplexity=1, detectionCon = 0.5, trackCon = 0.5): 
        self.mode = mode
        self.maxHands = maxHands
        self.modelComplexity = modelComplexity
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplexity, self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]

    def findHands(self, img, draw = True):
        imgRGB = cv.cvtColor((img), cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            if draw:
                for handlmrk in self.results.multi_hand_landmarks:
                    self.mpDraw.draw_landmarks(img, handlmrk, self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo = 0, draw = True):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id,lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv.circle(img,(cx,cy), 5 , (0,0,150), cv.FILLED) 
        return self.lmList

    def fingersUp(self):
        # If Image is flipped then results will change accordingly
        fingers = []
        for id in range(0, 5):
            if id == 0:
                if(self.lmList[self.tipIds[id]][1] < self.lmList[self.tipIds[id] - 1][1]):
                    fingers.append(1)
                else :
                    fingers.append(0)
            else:
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else :
                    fingers.append(0)

        return fingers


#----------------------------------------------------------------------------------------------------------


def main():
    # Dummy Code
    pTime = 0
    cTime = 0
    cap = cv.VideoCapture(0)
    detector = handDetector() # module.handDetector
    while True:
        isTrue, frame = cap.read()
        img = cv.resize(frame, (640,480))

        img = detector.findHands(img, True)
        lmList = detector.findPosition(img)

        if len(lmList) != 0:
            print(lmList[8])
        
        #FPS
        # cTime = time.time()
        # fps = 1/(cTime-pTime)
        # pTime = cTime
        # cv.putText(img, str(int(fps)), (5, 20), cv.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

        cv.imshow("webCam", img)
        if cv.waitKey(1) & 0xFF == ord('x'):
            break
        
    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()