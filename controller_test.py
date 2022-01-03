"""
File for testing PID controller and setting parameters
Creates a fake bounding box for the camera to track
Bounding box is adjustable through trackbars
Benjamin Dostie 2022
"""

import cv2
from utils.VISCA_controller import controller


SIZE_THRESHOLD = 50
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
cam = cv2.VideoCapture(1)

# trackbars for moving test bounding box
def nothing(x):
    pass
cv2.namedWindow('web_cam')
cv2.createTrackbar('xVal' , 'web_cam', 200, 1920, nothing)
cv2.createTrackbar('yVal' , 'web_cam', 200, 1080, nothing)
cv2.createTrackbar('hVal' , 'web_cam', 100, 500, nothing)
cv2.createTrackbar('wVal' , 'web_cam', 100, 500, nothing)

test_controller = controller(DISPLAY_WIDTH, DISPLAY_HEIGHT)


while True:
    _, frame = cam.read()
    frame = cv2.resize(frame, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    
    posX = cv2.getTrackbarPos('xVal', 'web_cam')
    posY = cv2.getTrackbarPos('yVal', 'web_cam')
    boxH= cv2.getTrackbarPos('hVal', 'web_cam')
    boxW = cv2.getTrackbarPos('wVal', 'web_cam')

    frame = cv2.rectangle(frame, (posX, posY), (posX + boxW, posY + boxH),(2,100,0), -1)
    
    test_controller.follow((posX, posY, boxW, boxH))
 
        
                
    
         
        


    #cv2.drawContours(frame, contours, 0,(255,0,0), 3)
    cv2.imshow('web_cam', frame)
    cv2.moveWindow('web_cam',0,0)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    

cam.release
cv2.destroyAllWindows