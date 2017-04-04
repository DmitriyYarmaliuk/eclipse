import os
import sys
import cv2
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from WebcamVideoStream import WebcamVideoStream
from VideoStream import VideoStream
import imutils
from threading import Thread
import cv2
from imutils.video import VideoStream
import datetime
import argparse
from Stepper import Stepper
from Servo import Servo

#ap = argparse.ArgumentParser()
#ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether the PiCamera being used")
#args = vars(ap.parse_args())

#vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
#vs = cv2.VideoCapture("/home/pi/Desktop/Full_Tracking_System_Test.mp4")

#vs = cv2.VideoCapture("/home/pi/Downloads/April_03_17_Manual_and_Stream_Test_2.h264")
#time.sleep(2)
vs = cv2.VideoCapture("/home/pi/Desktop/Test.h264")

#vs.set(cv2.cv.CV_CAP_PROP_FPS, 25)
#time.sleep(2.0)

def main(argv):
	

	while True:
	
	        frame = vs.grab()
		_, frame = vs.read()
	        frame = imutils.resize(frame, width=400)
		
	        # Converting captured frame to monochrome
	        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	        # Blurring the image using the GaussianBlur() method of the opencv object
	        blur = cv2.GaussianBlur(gray, (9, 9), 0)
	
	        # Using an opencv method to identify the threshold intensities and locations
	        (darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
		print "Brightest Value:",brightest_value
	        # Threshold the blurred frame accordingly
	        # First argument is the source image, which is the grayscale image. Second argument is the threshold value
	        # which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
	        # if pixel value is more than (sometimes less than) the threshold value
	        out2, threshold2 = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
		out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)
	        thr = threshold.copy()
	        print "out value:",out2
	        # Resize frame for ease
	        # cv2.resize(thr, (300, 300))
	        # Find contours in thresholded frame
	        edged = cv2.Canny(threshold, 50, 150)
	
	        # First one is source image, second is contour retrieval mode, third is contour approximation method. And it outputs
	        # the contours and hierarchy. Contours is a Python list of all the contours in the image. Each individual contour
	        # is a Numpy array of (x,y) coordinates of boundary points of the object.
	        lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	
	
	        # Checking if the list of contours is greater than 0 and if any circles are detected
	        if (len(lightcontours)):
	                # Finding the maxmimum contour, this is assumed to be the light beam
	                maxcontour = max(lightcontours, key=cv2.contourArea)
	                # Avoiding random spots of brightness by making sure the contour is reasonably sized
	                if cv2.contourArea(maxcontour):
	                        (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
	
	                        print "x value:",x,"y value:",final_y
	
				t=Stepper(x,final_y)
				s = Servo(final_y)
#				s.servo_control()
#				t.change_position()
		
	                        cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
	                        cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)
	                        # Display frames and exit
	#       cv2.imshow('light', thr)
	        cv2.imshow('frame', frame)
	        cv2.waitKey(4)
	        key = cv2.waitKey(1)
	
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	                break
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv) 
