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

ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether the PiCamera being used")
args = vars(ap.parse_args())

vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

def main(argv):

	bright_values = {} # creates an array of the brightest values
	count = 0
	
	while True:
		if count == 7: # looks for 7 different spots
		    break
		
		frame = vs.read() # reads the frame from the OpenCV object
		frame = imutils.resize(frame, width=400) # resizing the frame in case frame was changed previously
		
		# Converting captured frame to monochrome
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Blurring the image using the GaussianBlur() method of the opencv object
		blur = cv2.GaussianBlur(gray, (9, 9), 0)
		
		# Using an opencv method to identify the threshold intensities and locations
		(darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
		# Threshold the blurred frame accordingly
		# First argument is the source image, which is the grayscale image. Second argument is the threshold value
		# which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
		# if pixel value is more than (sometimes less than) the threshold value
		out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
		
		time.sleep(1)
		
		if os.path.isfile('mem.txt'): # finds txt file
			fp = open("mem.txt", 'r')
		    	current_val = [int(n) for n in fp.read().split()] # reads current position
		    	print "current_val", current_val[0], "out", out
		    	bright_values[int(current_val[0])] = out # found the brightest value and storing
		
		else:
		   	bright_values[257] = out
		
		count = count + 1 # counter to happen 7 times
	
		t = Stepper(0, 0)
		t.change_position_scan() # moves stepper to scan
	
	print bright_values
	i = 0
	
	for w in sorted(bright_values, key=bright_values.get, reverse=True): # sorts the 7 brightest values
		if i > 0:
			break
		print w, bright_values[w] # prints all values
		required_pos = w
		i = i + 1
	
	print "required_pos", required_pos
    	t.return_to_bright_spot(required_pos) # found required spot
	

	while True:
	
	        frame = vs.read()
	        frame = imutils.resize(frame, width=400)
		
		# Converting captured frame to monochrome
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		# Blurring the image using the GaussianBlur() method of the opencv object
		blur = cv2.GaussianBlur(gray, (39, 39), 0)
		cv2.imshow("blur", blur)
#		copy =  frame.copy()
		# Using an opencv method to identify the threshold intensities and locations
		(darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
		#print "brightest Value:", brightest_value-200
		
		# Threshold the blurred frame accordingly
		# First argument is the source image, which is the grayscale image. Second argument is the threshold value
		# which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
		# if pixel value is more than (sometimes less than) the threshold value
		out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)
		#   print "Threshold:", out2
		thr = threshold.copy()
		# Resize frame for ease
		# cv2.resize(thr, (300, 300))
		# Find contours in thresholded frame
		edged = cv2.Canny(threshold, 50, 150)
		
		# First one is source image, second is contour retrieval mode, third is contour approximation method. And it outputs
		# the contours and hierarchy. contours is a Python list of all the contours in the image. Each individual contour
		# is a Numpy array of (x,y) coordinates of boundary points of the object.
		
		
		# Possible second parameter options
		# RETR_EXTERNAL
		# retrieves only the extreme outer contours. It sets hierarchy[i][2]=hierarchy[i][3]=-1 for all the contours.
		# RETR_LIST
		# retrieves all of the contours without establishing any hierarchical relationships.
		# RETR_CCOMP
		# retrieves all of the contours and organizes them into a two-level hierarchy. At the top level, there are external boundaries of the components. At the second level, there are boundaries of the holes. If there is another contour inside a hole of a connected component, it is still put at the top level.
		# RETR_TREE
		# retrieves all of the contours and reconstructs a full hierarchy of nested contours.
		# RETR_FLOODFILL
		
		
		
		# Possible 3 parameter options
		#  CHAIN_APPROX_NONE
		# stores absolutely all the contour points. That is, any 2 subsequent points (x1,y1) and (x2,y2) of the contour will be either horizontal, vertical or diagonal neighbors, that is, max(abs(x1-x2),abs(y2-y1))==1.
		# CHAIN_APPROX_SIMPLE
		# compresses horizontal, vertical, and diagonal segments and leaves only their end points. For example, an up-right rectangular contour is encoded with 4 points.
		# CHAIN_APPROX_TC89_L1
		# applies one of the flavors of the Teh-Chin chain approximation algorithm [151]
		# CHAIN_APPROX_TC89_KCOS
		# applies one of the flavors of the Teh-Chin chain approximation algorithm [151]
		
		lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		contour = []
		# print contour
		# print "length of lightcontours:", len(lightcontours)
		# print "length of contour:", len(contour)
		# print "Number of contours:", len(lightcontours)
		# # Checking if the list of contours is greater than 0 and if any circles are detected
		# print "range(len(con)):", range(len(lightcontours))
		
		for i in range(len(lightcontours)):
			(x, final_y), radius = cv2.minEnclosingCircle(lightcontours[i])
			print "First Time-----","x value:", x, "y value", final_y, "radius", radius
			if radius < 20:
		    		print "Inside special if statement"
		    		contour.append(lightcontours[i])
			else:
		    		continue
		print "Length of numpy array containing all light contours:", len(lightcontours)
		print "Length of list containing contours with specified radius:",len(contour)
		print contour
		if (len(contour) > 0):
		# Finding the maxmimum contour, this is assumed to be the light beam
			maxcontour = max(contour, key=cv2.contourArea)
        	# Avoiding random spots of brightness by making sure the contour is reasonably sized
	                if cv2.contourArea(maxcontour):
	                        (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
	
	                        print "x value:",x,"y value:",final_y
	
				t=Stepper(x,final_y)
				s = Servo(final_y)
				s.servo_control()
#				t.change_position()
		
	                        cv2.circle(frame, (int(x), int(final_y)), int(radius+20), (0, 255, 0), 4)
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
