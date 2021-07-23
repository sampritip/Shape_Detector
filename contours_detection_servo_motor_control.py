import cv2
import numpy as np
from pyfirmata import Arduino, util
import time

board = Arduino('COM5')
servo = board.get_pin('d:10:s') #digital:setting pin 10:mode
servo.write(90.0)

frameWidth = 200
frameHeight = 200
cap = cv2.VideoCapture(1)
cap.set(3,frameWidth)
cap.set(4,frameHeight)

def empty(a):
    pass

cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters",300,300)
cv2.createTrackbar("Threshold1","Parameters",30,255,empty)
cv2.createTrackbar("Threshold2","Parameters",34,255,empty)
cv2.createTrackbar("Area","Parameters",5000,30000,empty)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour):
    contours, hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("Area","Parameters")
        if area > areaMin:
            cv2.drawContours(imgContour,cnt,-1,(255,0,255),7)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            edges = int(len(approx))
            if edges == 4:
                servo.write(20)
                time.sleep(0.3)
                # n=5
                # while n>0:
                #     board.digital[13].write(1)
                #     time.sleep(1)
                #     board.digital[13].write(0)
                #     time.sleep(1)
                #     n=n-1
            elif edges == 5:
                servo.write(130)
                time.sleep(0.3)
                # board.digital[13].write(1)
                

            x,y,w,h = cv2.boundingRect(approx)
            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),5)


            cv2.putText(imgContour,"Points: " + str(len(approx)),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)
            #cv2.putText(imgContour,"Area: "+str(int(area)),(x+w+20,y+45),cv2.FONT_HERSHEY_COMPLEX,.7,(0,255,0),2)





while True:
    success, img = cap.read()
    #img = cv2.imread(r"C:\Users\Shampoo\Pictures\Screenshots\square.png")
    # if img is not None:
    #     cv2.imshow("Img",img)
    # else:
    #     print("None")
    imgContour = img.copy()
    imgBlur = cv2.GaussianBlur(img,(7,7),1)
    imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1","Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2","Parameters")


    imCanny = cv2.Canny(imgGray,threshold1,threshold2)
    kernel = np.ones((5,5))
    imgDil = cv2.dilate(imCanny, kernel, iterations=1)

    getContours(imgDil,imgContour)
    #possible output: imgGray,imgBlur,imgDil,imgContour,img,imCanny
    #imgStack = stackImages(0.8,[imgDil,imgBlur,imgContour])

    #cv2.imshow("Img",imgStack)
    cv2.imshow("Img",imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break