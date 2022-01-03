from adafruit_servokit import ServoKit





class SimpleServoControl:
    """ proportional controller for adafruit servo kit"""
    def __init__(self, width, height):
        """
        New proportional controller 
        :param width: width of camera frames
        :param height: height of camera frames
        :return: none
        """
        self.kit = ServoKit(channels=16)
        self.pan = 90
        self.tilt = 90
        self.kit.servo[0].angle = self.tilt
        self.kit.servo[1].angle = self.pan
        self.WIDTH = width
        self.HEIGHT = height
    def follow(self, box):
        """
        Moves camera to indicated pixel coordinates
        :param box: bounding box to follow in x,y,h,w format
        :return: none
        """
        x, y, w, h = box
        center_x = x + w/2
        center_y = y + h/2
        pan_error = center_x - self.WIDTH/2
        tilt_error = center_y - self.HEIGHT/2

        if abs(pan_error) > 15:
            self.pan -= pan_error/25
        if abs(tilt_error) > 15:
            self.tilt -= pan_error/25


        #range check
        if self.pan > 180:
            self.pan = 180
        if self.pan < 0:
            self.pan = 0
        if self.tilt> 180:
            self.tilt = 180
        if self.tilt < 0:
            self.tilt = 0
        
        #apply
        self.kit.servo[1].angle = self.pan
        self.kit.servo[0].angle = self.tilt
        