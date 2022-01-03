import cv2
import numpy as np
from collections import deque



class CostBasedTracker:
    """
    Tracks an object over several frames.
    Generates cost between a history of a tracked object and current
    proposals. The lowest cost proposal is assumed to be the object 
    and added to the history.
    
    """
    def __init__(self, loc_history_len):
        """
        New object tracker
        :param loc_history_len: Maximum length of the track history
        """
        self.location_history = deque(maxlen=loc_history_len)
    def location_prediction(self, lost_track_frames):
        """
        Predicts the location of the tracked object by taking the 
        derivative over the history and projecting into future.
        :param lost_track_frames: number of frames the object has not 
        been seen
        """
        delta_y = 0
        delta_x = 0
        delta_w = 0
        delta_h = 0
        hist_len = len(self.location_history)
        if hist_len > 1:
            norm = 0
            pred_x, pred_y, pred_w, pred_h = self.location_history[0]
            for i in range(1,hist_len,1):
                delta_x += (self.location_history[i-1][0] - self.location_history[i][0])*(hist_len-i+1)
                delta_y += (self.location_history[i-1][1] - self.location_history[i][1])*(hist_len-i+1)
                delta_w += (self.location_history[i-1][2] - self.location_history[i][2])*(hist_len-i+1)
                delta_h += (self.location_history[i-1][3] - self.location_history[i][3])*(hist_len-i+1)
                norm += (hist_len-i+1)
            pred_x = self.location_history[0][0] + delta_x / max(1, norm) * (1 + lost_track_frames)
            pred_y = self.location_history[0][1] + delta_y / max(1, norm) * (1 + lost_track_frames)
            pred_w = self.location_history[0][2] + delta_w / max(1, norm) * (1 + lost_track_frames)
            pred_h = self.location_history[0][3] + delta_h / max(1, norm) * (1 + lost_track_frames)
        return (pred_x, pred_y), pred_w, pred_h
        
    def iou_cost(self, point_sets, lost_track_frames):
        """
        Calculates the intersection over union cost. Proposal with the 
        most overlap with bounding box prediction from location 
        prediction.
        :param point_sets: bounding box coords of all proposals
        :param lost_track_frames: number of frames the object has not 
        been seen
        """
        #a,b for upper left corner, c,d for lower right corner
        pred_x, pred_y, pred_w, pred_h = self.location_prediction(lost_track_frames)
        a = pred_x
        b = pred_y
        c = pred_x + pred_w
        d = pred_y + pred_h
        pred_area = pred_w * pred_h
        
        bb_costs = []
        for point_set in point_sets:
            (x, y, w, h) = point_set['box']
            a_2 = x 
            b_2 = y
            c_2 = x + w
            d_2 = y + h
            intersection = max(0 , (min(c, c_2) - max(a, a_2))) * max(0, (min(d, d_2) - max(b, b_2)))
            union = pred_area + (w * h) - intersection
            
            bb_costs.append(1 - intersection/union)
            
        return bb_costs


    def location_cost(self, point_sets, lost_track_frames):
        """
        Calculates cost between all proposals and history based on 
        location prediction. The poposal closest to the predicted 
        location will have the lowest cost.
        :param point_sets: bounding box coords of all proposals
        :param lost_track_frames: number of frames the object has not 
        been seen
        """
            
            
        (pred_x, pred_y), pred_w, pred_h = self.location_prediction(lost_track_frames)
        bb_costs = []
        for point_set in point_sets:
            (x, y, w, h) = point_set['box']
            bb_costs.append((abs(pred_x - x) + abs(pred_y - y) + abs(pred_h - h) +abs(pred_w - w)))
            
        return bb_costs
    def xy_error(self, bounding_box, x, y):
        """
        Calculates xy error between two bounding boxes
        :param bounding_box: bounding box coords
        :param x: x coord to compare to bounding box
        :param y: y coord to compare to bounding box        
        """
        (x, y, w, h) = bounding_box
        return (abs(x - x) + abs(y - y))

    def find_track(self, point_sets, x, y):
        """
        Finds nearest detected object to x,y coord
        :param point_sets: bounding box coords of all detections
        :param x: x coord to compare to bounding boxes
        :param y: y coord to compare to bounding boxes
        """
        if len(point_sets) > 0:
            closest_track = point_sets[0]['box'] 
            smallest_error = self.xy_error(point_sets[0]['box'], x, y)
            for point_set in point_sets:
                box = point_set['box']
                if self.xy_error(box, x, y) < smallest_error:
                    closest_track = box
                    smallest_error = self.xy_error(box, x, y)
            x, y, w, h = closest_track
            self.location_history.clear()
            self.location_history.appendleft((x, y, w, h))
            self.location_history.appendleft((x, y, w, h))

            return True
        
        else:
            useless = y + x
            return False
    def drop_track(self):
        self.location_history.clear()
    def update_track(self, x, y, w, h):
        self.location_history.appendleft((x, y, w, h))
        

      