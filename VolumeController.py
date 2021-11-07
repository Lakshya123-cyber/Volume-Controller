import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

detector = htm.handDetector(detectionCon=0.7)


# print(outputVol)

osascript.osascript("set volume output volume 50")

minVol = 0
maxVol = 100

while True:
    success, img = cap.read()

    img = detector.findHands(img)

    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # print(lmList[4], lmList[8])

        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]

        cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

        cv2.circle(img, (x1, y1), 8, (0,255,0), cv2.FILLED)
        cv2.circle(img, (x2, y2), 8, (0,255,0), cv2.FILLED)

        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)
        # print(length)

        # Hand range -> 20 - 200
        # Volume range -> 0 - 100

        vol = np.interp(length, [20, 200], [minVol, maxVol])
        # print(vol)
        result = osascript.osascript('get volume settings')
        volInfo = result[1].split(',')
        outputVol = volInfo[0].replace('output volume:', '')

        if length <= 50:
            cv2.circle(img, (cx, cy), 5, (0, 255,0), cv2.FILLED)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)