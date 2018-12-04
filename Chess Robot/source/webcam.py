import cv2
from threading import Thread
  
class Webcam:
  
    def __init__(self):
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1]
        self.__continue = True
        
    def __del__(self):
        self.__continue = False
          
    # create thread for capturing images
    def start(self):
        self.thread = Thread(target=self._update_frame, args=()).start()
  
    def _update_frame(self):
        while(self.__continue):
            self.current_frame = self.video_capture.read()[1]
                  
    # get the current frame
    def get_current_frame(self):
        return self.current_frame
