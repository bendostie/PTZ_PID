import cv2
import numpy as np
from collections import deque

from numpy.lib.utils import byte_bounds



class ColorDetector:
    """
    Detect a bounding box around a thresholded HSV selection 
    """
    def __init__(self, height, width, threshold = 50) -> None:
        """
        New instance of color based detector

        :param width: width of frames
        :param height: height of frames
        :param threshold: minimum size of pixel group
        """

        self.lower_bound_1 = 0
        self.upper_bound_1 = 0
        self.lower_bound_2 = 0
        self.upper_bound_2 = 0
        self.DISPLAY_HEIGHT = height
        self.DISPLAY_WIDTH = width
        self.THRESHOLD = threshold

        cv2.namedWindow('Trackbars')
        cv2.moveWindow('Trackbars', self.DISPLAY_WIDTH * 2, self.DISPLAY_HEIGHT + 20)
        cv2.createTrackbar('HueLow', 'Trackbars', 150, 179, self.nothing)
        cv2.createTrackbar('HueHigh', 'Trackbars', 179, 179, self.nothing)

        cv2.createTrackbar('HueLow2', 'Trackbars', 0, 179, self.nothing)
        cv2.createTrackbar('HueHigh2', 'Trackbars', 30, 179, self.nothing)

        cv2.createTrackbar('SatLow', 'Trackbars', 125, 255, self.nothing)
        cv2.createTrackbar('SatHigh', 'Trackbars', 255, 255, self.nothing)
        cv2.createTrackbar('ValLow', 'Trackbars', 103, 255, self.nothing)
        cv2.createTrackbar('ValHigh', 'Trackbars', 255, 255, self.nothing)

    def nothing(self, x):
        pass

    def update_trackbars(self):
        """
        Polls trackbars for updates and sets new bounds
        """
        hue_lower_1 = cv2.getTrackbarPos('HueLow', 'Trackbars')
        hue_upper_1 = cv2.getTrackbarPos('HueHigh', 'Trackbars')
        hue_lower_2 = cv2.getTrackbarPos('HueLow2', 'Trackbars')
        hue_upper_2 = cv2.getTrackbarPos('HueHigh2', 'Trackbars')
        saturation_lower = cv2.getTrackbarPos('SatLow', 'Trackbars')
        saturation_upper = cv2.getTrackbarPos('SatHigh', 'Trackbars')    
        value_lower = cv2.getTrackbarPos('ValLow', 'Trackbars')
        value_upper = cv2.getTrackbarPos('ValHigh', 'Trackbars')

        self.lower_bound_1 = np.array([hue_lower_1,saturation_lower,value_lower])
        self.upper_bound_1 = np.array([hue_upper_1,saturation_upper ,value_upper])
        self.lower_bound_2 = np.array([hue_lower_2,saturation_lower,value_lower])
        self.upper_bound_2 = np.array([hue_upper_2,saturation_upper ,value_upper])
        
    def detect(self, frame, display = True):
        """
        Creates bounding boxes around groups of pixels that fall within the color threshold
        :param frame: camera frame or image
        :param display: If true it shows each frame in a cv2 window with bounding boxes overlaid
        :return: returns list of bounding boxes in center, w, h format
        """
        self.update_trackbars()
        hsv=cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
        foreground_mask_1 = cv2.inRange(hsv,self.lower_bound_1, self.upper_bound_1)
        foreground_mask_2= cv2.inRange(hsv,self.lower_bound_2, self.upper_bound_2)
        #white on black
        foreground_mask_composition = cv2.add(foreground_mask_1, foreground_mask_2) 
        

        if display == True:
            #color on black
            foreground = cv2.bitwise_and(frame, frame, mask = foreground_mask_composition) 
            #black on white
            background_mask = cv2.bitwise_not(foreground_mask_composition)
            background = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)
            #color on white
            final = cv2.add(foreground, background)

            cv2.imshow('foreground_mask', foreground_mask_composition)
            cv2.moveWindow('foreground_mask', 0, self.DISPLAY_HEIGHT + 20)
            cv2.imshow('foreground', foreground)
            cv2.moveWindow('foreground', self.DISPLAY_WIDTH, 0)
            cv2.imshow('background_mask', background_mask)
            cv2.moveWindow('background_mask', self.DISPLAY_WIDTH, self.DISPLAY_HEIGHT + 20)
            cv2.imshow('final', final)
            cv2.moveWindow('final', self.DISPLAY_WIDTH * 2, 0)

        contours, _ = cv2.findContours(foreground_mask_composition, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key=lambda x:cv2.contourArea(x), reverse = True)
        bounding_boxes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= self.THRESHOLD:

                (x,y,w,h) = cv2.boundingRect(contour)
                
                center = (x+w/2, y+h/2)
                
                bounding_boxes.append((center, w, h))
            
        return bounding_boxes
    def assign_detection(self, frame, x, y):
        #target_color = frame[y, x]
        pass



class FaceCascadeDetector:
    """
    Detects faces using cv2/intel haar cascades
    """
    def __init__(self, width, height) -> None:
        """
        New instance of haar cascade face detector
        :param width: width of frames
        :param height: height of frames
        """
        self.face_det = CascadeDetector('cascades/haarcascade_frontalface_default.xml')
        self.r_eye_det = CascadeDetector('cascades/haarcascade_righteye_2splits.xml')
        self.l_eye_det = CascadeDetector('cascades/haarcascade_lefteye_2splits.xml')
        #self.nose_det = CascadeDetector('haarcascade_frontalface_default.xml')
        self.mouth_det = CascadeDetector('cascades/haarcascade_smile.xml')


    def detect(self, frame):

        faces = self.face_det.detect(frame)
        bounding_boxes = []
        for (x,y,w,h) in faces:
            sub_frame = frame[y:y + h, x:x + w]
            r_eyes = self.r_eye_det.detect(sub_frame)
            
            if len(r_eyes) > 0:
                r_eye_sub_x, r_eye_sub_y, r_eye_w, r_eye_h = r_eyes[0]
                r_eye_x = r_eye_sub_x + x + r_eye_w/2
                r_eye_y = r_eye_sub_y + y + r_eye_h/2
            else:
                r_eye_x = r_eye_y = 0

            l_eyes = self.l_eye_det.detect(sub_frame)
            if len(l_eyes) > 0:
                
                l_eye_sub_x, l_eye_sub_y, l_eye_w, l_eye_h = l_eyes[0]
                l_eye_x = l_eye_sub_x + x + l_eye_w/2
                l_eye_y = l_eye_sub_y + y + l_eye_h/2
            else:
                l_eye_x = l_eye_y = 0

            #noses = self.nose_det.detect(sub_frame)
            if False:
                nose_sub_x, nose_sub_y, nose_w, nose_h = noses[0]
                nose_x = nose_sub_x + x + nose_w/2
                nose_y = nose_sub_y + y + nose_h/2
            else:
                nose_y = nose_x = 0

            mouths = self.mouth_det.detect(sub_frame)
            
            if len(mouths) > 0:
                mouth_sub_x, mouth_sub_y, mouth_w, mouth_h = mouths[0]
                l_mouth_x = mouth_sub_x + x 
                l_mouth_y = r_mouth_y = mouth_sub_y + y + mouth_h/2
                r_mouth_x = mouth_sub_x + x + mouth_w
            else:
                l_mouth_x = l_mouth_y = r_mouth_y = r_mouth_x = 0
            
            bounding_boxes.append({
                    'box': [x, y, w, h],
                    'confidence': 1,
                    'keypoints': {
                        'left_eye': (int(l_eye_x), int(l_eye_y)),
                        'right_eye': (int(r_eye_x), int(r_eye_y)),
                        'nose': (int(nose_x), int(nose_y)),
                        'mouth_left': (int(l_mouth_x), int(l_mouth_y)),
                        'mouth_right': (int(r_mouth_x), int(r_mouth_y)),
                    }
                })
        return bounding_boxes
    def assign_detection(self, frame, x, y):
        pass

class CascadeDetector:
    def __init__(self, cascade_path) -> None:
        self.cascade = cv2.CascadeClassifier(cascade_path)
    def detect(self, frame, display = True):
        grayscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        bounding_boxes = self.cascade.detectMultiScale(grayscale_frame, 1.3, 5)
        
        
            
        return bounding_boxes
    def assign_detection(self, frame, x, y):
        pass

class OpenCVDNNDetector:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.model_file = "models/res10_300x300_ssd_iter_140000.caffemodel"
        self.config_file =  "models/deploy.prototxt.txt"
        self.model = cv2.dnn.readNetFromCaffe(self.config_file, self.model_file)
    def detect(self, frame):
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
                            (300, 300), (104.0, 117.0, 123.0))
        self.model.setInput(blob)
        faces = self.model.forward()
        bounding_boxes = []
        for i in range(faces.shape[2]):
            confidence = faces[0, 0, i, 2]
            if confidence > 0.5:
                box = faces[0, 0, i, 3:7] * np.array([self.width, self.height, self.width, self.height])
                (x, y, x1, y1) = box.astype("int")
                w = x1 - x
                h = y1 - y
                bounding_boxes.append({
                    'box': [x, y, w, h],
                    'confidence': confidence
                })
        return bounding_boxes
    def assign_detection(self, frame, x, y):
        pass