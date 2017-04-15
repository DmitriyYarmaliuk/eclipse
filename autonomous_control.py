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

# Defaults to using the Raspberry Pi camera
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether the PiCamera being used")
args = vars(ap.parse_args())

# Starts video capture using the Raspberry Pi camera
vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
time.sleep(2.0)

def main(argv):

	bright_values = {} # creates a dictionary which will store light intensity values as well as their corresponding positions
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
		
		# Using an opencv method to identify threshold intensities and locations
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
		    	bright_values[int(current_val[0])] = out # found the light intensity value thereby storing it 
			# into dictionary with the key being the position of the stepper motor
		
		else:
		   	bright_values[257] = out
		
		count = count + 1 # counter to happen 7 times
	
		t = Stepper(0, 0)
		t.change_position_scan() # moves stepper to scan/to the next position to ultimately span the entire 360 degree perimeter
	
	print bright_values
	i = 0
	
	for w in sorted(bright_values, key=bright_values.get, reverse=True): # sorts the 7 brightest values
		if i > 0:
			break
		print w, bright_values[w] # prints all values
		required_pos = w
		i = i + 1
	
	print "required_pos:", required_pos
    	t.return_to_bright_spot(required_pos) # returning to the required position
	
	while True:

		# Reading in a frame of video
	        frame = vs.read()
		# Resizing the frame
	        frame = imutils.resize(frame, width=400)
		
		# Converting captured frame to monochrome
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		# Blurring the image using the GaussianBlur() method of the opencv object
		blur = cv2.GaussianBlur(gray, (29, 29), 0)

		# Using an opencv method to identify the threshold intensities and locations
		(darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
		
		# Threshold the blurred frame accordingly
		# First argument is the source image, which is the grayscale image. Second argument is the threshold value
		# which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
		# if pixel value is more than (sometimes less than) the threshold value
		out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)

#		thr = threshold.copy()

		# Finding contours/edges in thresholded frame
		edged = cv2.Canny(threshold, 50, 150)
		
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
		
                # The first parameter is the image(with edges identified), second is the contour retrieval mode, and third is the contour approximation method. 
                # The function outputs the contours and hierarchy. Lightcontours is a Python list of all the contours in the image. Each individual contour
                # is a Numpy array of (x,y) coordinates of boundary points of the object.
		lightcontours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

		# Defining list that will hold light contours with a desired radius
		contour = []

		# print contour
		# print "length of lightcontours:", len(lightcontours)
		# print "length of contour:", len(contour)
		# print "Number of contours:", len(lightcontours)
		# Checking if the list of contours is greater than 0 and if any circles are detected
		# print "range(len(con)):", range(len(lightcontours))
		

		# Looping through all light contours to select the contour with the desired radius
		for i in range(len(lightcontours)):

			# Drawing a minimum enclosing circle around each light contour. 
			# Obtaining position(in terms of the x and y axis in pixels) of the center of 
			# the minimum enclosing circle associated with each light contour as well as its radius.
			(x, final_y), radius = cv2.minEnclosingCircle(lightcontours[i])
			print "First Time-----","x value:", x, "y value", final_y, "radius", radius

			# Selecting light contour with the desired radius and writing it to the contour list
			if radius > 10:
		    		contour.append(lightcontours[i])
			else:
		    		continue
		print "Length of numpy array containing all light contours:", len(lightcontours)
		print "Length of list containing contours with specified radius:",len(contour)

        	# Checking if the list of light contours with the desired radius is greater than 0.
		# If multiple light contours are outlined with the desired radius further analysis is performed.
		if (len(contour) > 0):

			# Finding the maximum contour, this is assumed to be the light beam
			maxcontour = max(contour, key=cv2.contourArea)
        	
			# Avoiding random spots of brightness by making sure the contour is reasonably sized
	                if cv2.contourArea(maxcontour):
				
				# Obtaining position (x and y) and radius of the minimum enclosing lightcontour
				# with the desired size in terms of pixels (assumed to be the brightest object in the frame)
	                        (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
	
	                        print "x value:",x,"y value:",final_y
				
				# Creating an instance of the Stepper and Servo class while passing in the position of the outlined
				# brightest object				
				t = Stepper(x,final_y)
				s = Servo(final_y)

				# Calling the corresponding methods to move the servo and stepper motors to keep the outlined 
				# brightest object in the center of the frame
				s.servo_control()
				t.change_position()
		
				# Drawing a circle around the outlined brightest object in the frame 
	                        cv2.circle(frame, (int(x), int(final_y)), int(radius+20), (0, 255, 0), 4)

				# Drawing a rectangle in the center of the outlined brightest object in the frame
	                        cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)

	        # Display frame
	        cv2.imshow('frame', frame)
	        cv2.waitKey(4)
	        key = cv2.waitKey(1)
		
		# Entering 'q' kills the program
	        if cv2.waitKey(1) & 0xFF == ord('q'):
	                break
	
	# Cleaning up and killing all windows
	cap.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main(sys.argv)
