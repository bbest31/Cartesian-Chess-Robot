import cv2
from threading import Thread
from queue import Queue

class Webcam:
  
    def __init__(self):
        self.permanent_points = []
        self.temporary_points = []
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]  
    # create thread for capturing images
    def start(self, queue):
        self.thread = Thread(target=self._update_frame, args=(queue,)).start()

    def _update_frame(self, queue):
        cv2.namedWindow("Frame")
        params = [queue]
        cv2.setMouseCallback("Frame", self._register_click, params)
        while(True):
            self.current_frame = self.video_capture.read()[1]
            for permanent_point in self.permanent_points:
                cv2.circle(self.current_frame, permanent_point, 5, (0, 0, 255), -1)
            # display image
            for temporary_point in self.temporary_points:
                cv2.circle(self.current_frame, temporary_point, 5, (0, 0, 0), -1)
            cv2.imshow('Frame', self.current_frame) 
            key = cv2.waitKey(1)
    #Draw some points permanently
    def add_permament_points(self, point):
        self.permanent_points.append(point)
    
    #Draw Temporary points
    def add_temporary_points(self, point):
        self.temporary_points.append(point)

    #Delete temporary points
    def remove_temporary_points(self):
        self.temporary_points.clear()


    def _register_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Click " + str((x,y)) )
            params[0].put((x,y))
