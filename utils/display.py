import cv2
            
def draw_points(frame, point_sets, type = 'box'):

    for point_set in point_sets:
        bounding_box = point_set['box']
        
        if type == 'box':
            cv2.rectangle(frame,
              (bounding_box[0], bounding_box[1]),
              (bounding_box[0]+bounding_box[2], bounding_box[1] + bounding_box[3]),
              (0,155,255),
              2)
        elif type == 'face':
            keypoints = point_set['keypoints']
            cv2.circle(frame,(keypoints['left_eye']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['right_eye']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['nose']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['mouth_left']), 2, (0,155,255), 2)
            cv2.circle(frame,(keypoints['mouth_right']), 2, (0,155,255), 2)
            #cv2.rectangle(frame, (keypoints['mouth_left']),(keypoints['mouth_right']), (0, 155, 255), 2)
        else:
            raise Exception("no drawing type")
        
    return frame