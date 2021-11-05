import cv2
import numpy as np
from trackers import CostBasedTracker
from detectors import OpenCVDNNDetector
from display import draw_points
from numpy.core.fromnumeric import argmin

#detection bounding box size threshold
SIZE_THRESHOLD = 50
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
cam = cv2.VideoCapture(0)
cam.set(3, DISPLAY_WIDTH)
cam.set(4, DISPLAY_HEIGHT)



detector = OpenCVDNNDetector(DISPLAY_WIDTH, DISPLAY_HEIGHT)
tracker = CostBasedTracker(5)
lost_track_frames = 0
tracking = False


def click(event, x, y, flags, params):
    global tracking
    
 
    
    
    if event == cv2.EVENT_LBUTTONDOWN:
        _, frame = cam.read()
        bounding_boxes = detector.detect(frame)
        tracking = tracker.find_track(bounding_boxes, x, y)

    if event == cv2.EVENT_RBUTTONDOWN:
        _, frame = cam.read()
        detector.assign_detection(frame, x, y)
        
        
cv2.namedWindow('web_cam')
cv2.setMouseCallback('web_cam', click)



while True:
    #camera
    _, frame = cam.read()
    
 

    point_sets = detector.detect(frame)
    
    
    
    
            
    if tracking == True:
        bb_costs = tracker.location_cost(point_sets, lost_track_frames)
       
        if len(bb_costs) > 0: 
            
            track_box = point_sets[argmin(bb_costs)]['box']
            #controller.follow(track_box)
            x,y,w,h = track_box
            tracker.update_track(x, y, w, h) 
            frame = draw_points(frame, [point_sets[argmin(bb_costs)]], type = 'box')
            
 
    else:
        frame = draw_points(frame, point_sets, 'box')
            
        
                
    
         
        


    #cv2.drawContours(frame, contours, 0,(255,0,0), 3)
    cv2.imshow('web_cam', frame)
    cv2.moveWindow('web_cam',0,0)
    
    key = cv2.waitKey(1)
    if key == ord('q'):
        break
    elif key == ord('c'):
        tracking = False
        tracker.drop_track()

cam.release
cv2.destroyAllWindows