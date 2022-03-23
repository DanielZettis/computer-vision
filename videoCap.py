import cv2
import numpy as np

cap = cv2.VideoCapture('traffic1.mp4')
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 50, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations = 6)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(frame1, contours, -1, (0, 0, 255), 2)
    
    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()
     
    if cv2.waitKey(1) == ord('q'):
        break

cv2.destroyAllWindows()
cap.release()
