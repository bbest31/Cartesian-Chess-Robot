import cv2
from threading import Thread
from threading import Lock
from queue import Queue

'''
This class in in charge of abstracting camera image capture as well as image frame
functionality (display images, capture clicks, draw points).
The purpose of this abstranction is to be able to easily run the camera as well as the frame
in a separate frame so that the image never freezes with minimal boilerplate code.
This class also has the capability to perform distortion correction.
'''

class Webcam:
  
    def __init__(self):
        #Points that will be permanently draw in the frame (i.e the four corners of the chess board)
        self.permanent_points = []
        #Points that are meant for temporary display only (i.e the two points that the player has to specify in order to perform a movement)
        self.temporary_points = []
        self.video_capture = cv2.VideoCapture(0)
        self.current_frame = self.video_capture.read()[1] 
        #Create lock for thread synchronization
        self.lock = Lock() 
        #We disabled image distortion correction since distortion was
        #found to be negligible
        self.undistort_image = False
    # create thread for capturing images
    # we pass a reference to a queue so that we can get click coordinate data back from the
    # update_frame thread
    def start(self, queue):
        self.thread = Thread(target=self._update_frame, args=(queue,)).start()
    #Update the frame by getting images from the camera
    def _update_frame(self, queue):
        cv2.namedWindow("Frame")
        #Queue to send the coordinates of the registered clicks back to the main thread
        params = [queue]
        cv2.setMouseCallback("Frame", self._register_click, params)
        #If image distortion correction is enabled, load the campera parameters and distortion coefficients
        #Compute new camera matrix based on this and initialize maps for distortion correction
        if (self.undistort_image):
            mtx = np.loadtxt('camera_matrix.out')
            dist = np.loadtxt('distortion_coeffs.out')
            newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
            mapx,mapy = cv2.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)

        while(True):
            self.current_frame = self.video_capture.read()[1]
            #if distortion correction is enabled then remap the pixels of the current frame
            #to correct the distortion
            if (self.undistort_image):
                self.current_frame = cv2.remap(self.current_frame,mapx,mapy,cv2.INTER_LINEAR)
            #Draw the permanent points in the permanent_points array
            for permanent_point in self.permanent_points:
                cv2.circle(self.current_frame, permanent_point, 5, (0, 0, 255), -1)
            #Since the temporary_points array can be cleared by the main thread at any moment,
            #to guarantee thread safety, we acquire a lock while we are drawing the points inside
            #the temporary list
            self.lock.acquire()
            try:
                for temporary_point in self.temporary_points:
                    cv2.circle(self.current_frame, temporary_point, 5, (0, 0, 0), -1)
            finally:
                self.lock.release()
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
        self.lock.acquire()
        try:
            self.temporary_points.clear()
        finally:
            self.lock.release()        

    #Register a click. Since this function is actually executed in the update_frame thread we pass a queue
    #in the params array params=[queue] so that the registered clicks can be sent back to the main thread
    def _register_click(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            print("Click " + str((x,y)) )
            #If a click is registed, put it in the queue
            params[0].put((x,y))
