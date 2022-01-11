# PTZ_PID
This project implements a object detector, object tracker, and PID controller for PTZOptics cameras. It is loosely based on work done at Houghton College Summer Research Institute 2021.

## Detectors
There are 4 detectors currently implemented: a simple color-based detector using OpenCV <a href = "https://www.pyimagesearch.com/2021/04/28/opencv-thresholding-cv2-threshold/"> thresholding and contours</a>, a HAAR-cascade face and landmark detector using <a href = "https://github.com/opencv/opencv/tree/master/data/haarcascades">Intel HAAR cascades</a> with OpenCV, a face detector based on OpenCV <a href = "https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html">DNN Module</a>, and a face and landmark detector using <a href = "https://pypi.org/project/mtcnn/"> MTCNN</a>.

The detectors are wrapped to take parameters height and width and include a detect function that returns a list of bounding boxes. See <a href = "https://github.com/bendostie/PTZ_PID/blob/main/utils/detectors.py">detectors.py</a> for details. New detectors can easily be added.

## Tracker

A simple cost-based, single-object tracker is used to track a given object over time. Multi-object capabilities can easily be added by minimizing the tracking cost accross multiple detections with the Hungarian algorithm or similar. See this <a href = "https://ieeexplore.ieee.org/document/8782450"> paper</a> for inspiration.

## Controller
A PID controller is used to move a camera. The current controller is implementation specific to the PTZOptics camera using VISCA over IP. See <a href = "https://ptzoptics.com/wp-content/uploads/2021/01/PT30X-SDI-xx-G2-User-Manual-v1_6-rev-8-20.pdf">manual</a> for details on VISCA over IP. 

As expected the controller uses the difference in the target and current position to calculate the proportional error to follow an object, the integral of the error for steady state error, and the derivative of the error for smooth movement. It also uses thresholding to limit unnecessary movement. There are multiple adjustable parameters that will be described after further updates.
