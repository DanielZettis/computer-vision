import cv2
import numpy as np
   


video = cv2.VideoCapture('golyo.mp4')
#Arr = np.array([1 , 2], dtype=np.uint8)
image = np.zeros((360,640,3),np.uint8)

while(video.isOpened()):
    opened, frame1 = video.read()
    opened, frame2 = video.read()
    
    if opened == True:
        frame1r = cv2.resize(frame1, (640, 360))
        frame2r = cv2.resize(frame2, (640, 360))
        
        diff = cv2.absdiff(frame1r, frame2r)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray ,(7,7), cv2.BORDER_DEFAULT)
        _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations = 2)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        
        cv2.imshow('diff', dilated)
        
        xpos = ypos = 0
        contours, hierarchy= cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        number = 0
        numberOfObjects= len(contours)
        for contour in contours:
            
            number += 1
            text = "object: "+ str(number)
            
            (x, y, w, h) = cv2.boundingRect(contour)
            xpos = x
            ypos = y
            #print(x, y)
            image[y,x] = [0,255,0]
            cv2.putText(image, (str(number)), (x+2, y+2), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255), 1)
            #np.append(Arr, [xpos, ypos])

            print ("Object: ", str(numberOfObjects), " X:", x, "Y:", y)
            cv2.putText(frame1r, text, (x+20, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            
            if cv2.contourArea(contour) < 2000:
                continue
            cv2.rectangle(frame1r, (x,y), (x+w, y+h), (0, 255, 0), 1)
            #cv2.circle(frame1, (x,y), 50, (0, 255, 0), 1)
            cv2.putText(frame1r, "Status: {}".format('movement'), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.putText(frame1r, "X pos: {}".format(x), (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            cv2.putText(frame1r, "X pos: {}".format(y), (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            #cv2.drawContours(frame1, contours, -1, (0, 0, 255), 2)

        cv2.imshow('Frame1', frame1r)

        if cv2.waitKey(70) & 0xFF == ord('q'):
            break
        #if cv2.waitKey(1) & 0xff == ord('a'):
            #snitch = frame1
            #cv2.imshow('snitch', snitch)
        
    else:
        print("End")
        break
#print(Arr)
cv2.imwrite("result.png",image)

video.release()
cv2.destroyAllWindows()
