import cv2
import numpy as np

cam = cv2.VideoCapture(0)

myColor =  [[0, 122, 167, 179, 255, 255],
            [116, 110, 138, 179, 243, 255]]  # Add HSV values of teh colors you wish to detect [hmin, smin, vmin, hmax, smax, vmax]
myColorValues = [[10, 133, 255],
                 [8, 8, 163]]                # Add the color you wish to draw on screen [B, G, R]
myPoints= []


def getContours(mask, colorIdx):
    """ Find the contour in the mask and draw it on the actual frame """

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cont in contours:
        area = cv2.contourArea(cont)
        if area > 50:
            cv2.drawContours(frameContour, cont, -1, (0, 255, 255), 2)
            peri = cv2.arcLength(cont, True)
            apprx = cv2.approxPolyDP(cont, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(apprx)
            cv2.circle(frame, ((x + w // 2), y), 10, myColorValues[colorIdx], cv2.FILLED)  # Draw the circle at the center of the rectangle
            point = [(x + w // 2), y, colorIdx]  # Get the center of the rectangle
            myPoints.append(point)


def drawOnCanvas(pointArray, imgFrame):
    """ Draw circles at every point in the point array """
    for pt in pointArray:
        cv2.circle(imgFrame, (pt[0], pt[1]), 10, myColorValues[pt[-1]], cv2.FILLED)


while True:
    res, frame = cam.read()
    frameContour = frame.copy()
    frameHSV = cv2.cvtColor(frame, code=cv2.COLOR_BGR2HSV)
    mask = np.zeros_like(frame)

    for colorIdx, color in enumerate(myColor):
        lower = np.array([color[0:3]])
        upper = np.array([color[3:]])
        mask = cv2.inRange(frameHSV, lower, upper)
        getContours(mask, colorIdx)
    drawOnCanvas(myPoints, frame)

    cv2.imshow("Mask", mask)
    cv2.imshow("Video", frame)

    if (cv2.waitKey(1) == 27) or (cv2.waitKey(1) == ord('q')):
        break