import cv2
import numpy as np

from euclideanTracker import *
tracker = Tracker()

def callBack(x):
    pass

def findContours(frame):
    
    diff = MOG.apply(frame)
    blur = cv2.GaussianBlur(diff, (blurKernel, blurKernel), 0)
    _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.imshow("diff", diff)
    #cv2.imshow("blur", blur)
    cv2.imshow("thresh", thresh)
    return contours

videoPath = 'videok/traffic1.mp4'
windowName = "Tracker"

color = np.random.randint(0,255,(1500,3))

video = cv2.VideoCapture(videoPath)
cv2.namedWindow(windowName, flags=cv2.WINDOW_AUTOSIZE)

MOG = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=70)

cv2.createTrackbar("Threshold", windowName, 20, 100, callBack)
cv2.createTrackbar("BlurKernel", windowName, 60, 100, callBack)
cv2.createTrackbar("MinArea", windowName, 400, 10000, callBack)
cv2.createTrackbar("pDistance", windowName, 40, 500, callBack)
cv2.createTrackbar("Speed", windowName, 450, 499, callBack)

while(video.isOpened()):
    
    opened,frame=video.read()

    
    threshold = cv2.getTrackbarPos("Threshold", windowName)

    blurKernel = cv2.getTrackbarPos("BlurKernel", windowName)
    if blurKernel % 2 == 0 or blurKernel == 0:
        blurKernel += 1
        
    minArea = cv2.getTrackbarPos("MinArea", windowName)
    distanceOfPoints = cv2.getTrackbarPos("pDistance", windowName)
    speed = cv2.getTrackbarPos("Speed", windowName)
        
    #végtelenített lejátszás
    if not opened:
        video = cv2.VideoCapture(videoPath)
        tracker.idCount = 0
        tracker.centerPoints = {}
        continue
        
    frame = cv2.resize(frame, (800, 600))
    
    contours = findContours(frame)
    centers=[]
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > minArea:
            cv2.drawContours(frame,[contour],-1,(255,255,255),1)
            x,y,w,h = cv2.boundingRect(contour)
            cv2.circle(frame, ((x + x + w) // 2, (y + y + h) // 2), int(distanceOfPoints), (255, 0, 0), 1)
            centers.append([x,y,w,h])
            
    centerSort = tracker.Euclidean(centers, distanceOfPoints)
    
    for i in centerSort:
        x,y,w,h,id = i
        cv2.rectangle(frame,(x,y),(x+w,y+h),color[id].tolist(),2)
        cv2.putText(frame,str(id),(x,y -1),cv2.FONT_HERSHEY_COMPLEX,0.6,(255,255,0),1)
    
    cv2.putText(frame,str('Q to Quit'),(5,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,255),4)
    if cv2.waitKey(500-speed) & 0xFF == ord('q'):
        break
    cv2.imshow(windowName, frame)
video.release()
cv2.destroyAllWindows()
