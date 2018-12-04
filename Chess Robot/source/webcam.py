import cv2
from threading import Thread
from queue import Queue

class Webcam:
  
    def __init__(self, queue):
        self.queue = queue
        self.permanent_points = []
        self.temporary_points = []
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]
        cv2.namedWindow("Frame")
        cv2.setMouseCallback("Frame", self._register_click)  
    # create thread for capturing images
    def start(self):
        self.thread = Thread(target=self._update_frame, args=()).start()

    def _update_frame(self):
        while(True):
            self.current_frame = self.video_capture.read()[1]
            for permanent_point in permanent_points:
                cv2.circle(self.current_frame, permanent_point, 5, (0, 0, 255), -1)
            # display image
            for temporary_point in temporary_points:
                cv2.circle(self.current_frame, temporary_point, 5, (0, 0, 0), -1)
            cv2.imshow('Frame', self.current_frame) 
            key = cv2.waitKey(1)
    #Draw some points permanently
    def add_permament_points(self, point):
        self.corners.append(point)
    
    #Draw Temporary points
    def add_temporary_points(self, point):
        self.points.append(point)

    #Delete temporary points
    def remove_temporary_points(self):
        self.points.clear()


   def _register_click(event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.queue.put((x,y))
