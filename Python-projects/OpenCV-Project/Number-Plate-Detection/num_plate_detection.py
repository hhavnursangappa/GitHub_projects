# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# This project demonstrates a number plate scanner using OpenCV and haar cascade files
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

import cv2

cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
numPlateCascade = cv2.CascadeClassifier("E:\\Python_Programming\\GitHub_projects\\Python-projects\\OpenCV-Project\\Resource\\Haarcascades\\haarcascade_russian_plate_number.xml")
textColor = (0, 255, 0)
count = 0

while True:
    res, frame = cam.read()
    frameGray = cv2.cvtColor(frame, code=cv2.COLOR_BGR2GRAY)
    numPlates = numPlateCascade.detectMultiScale(frameGray, 1.1, 10)

    for (x, y, w, h) in numPlates:
        area = w*h
        if area > 500:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            cv2.putText(frame, "Number Plate", (x, y-5), cv2.FONT_HERSHEY_COMPLEX, 1, textColor, 2)
            frameROI = frame[y:y+h, x:x+w]
            cv2.imshow("Number plate", frameROI)

    cv2.imshow("Original", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('s'):
        cv2.rectangle(frame, (0, 200), (640, 300), (0, 0, 0), cv2.FILLED)
        cv2.putText(frame, "Scan saved", (150, 265), cv2.FONT_HERSHEY_COMPLEX, 2, (0, 0, 255), 2)
        cv2.imwrite("E:\\Python_Programming\\GitHub_projects\\Python-projects\\OpenCV-Project\\Resource\\Scanned\\number_plate_" + str(count) + ".jpg", frameROI)
        cv2.imshow("Original", frame)
        cv2.waitKey(500)
        count += 1

    elif key == ord('q') or key == 27:
        break
