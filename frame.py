import numpy as np
import cv2
import imutils

cap = cv2.VideoCapture('/home/pi/Desktop/Full_Tracking_System_Test.mp4')

while(cap.isOpened()):




        ret, frame = cap.read() # creates CV2 frame
        frame = imutils.resize(frame, width=400) # frame resolution = 400x400

        # Converting captured frame to monochrome
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Blurring the image using the GaussianBlur() method of the opencv object
        blur = cv2.GaussianBlur(gray, (9, 9), 0)

        # Using an opencv method to identify the threshold intensities and locations
        (darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)

        print "Brightest Value:", brightest_value
        # Threshold the blurred frame accordingly
        # First argument is the source image, which is the grayscale image. Second argument is the threshold value
        # which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
        # if pixel value is more than (sometimes less than) the threshold value
        out2, threshold2 = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)
        thr = threshold.copy()
        print "out value:", out2

        # Find contours in thresholded frame

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
                print "x value:", x, "y value:", final_y # printing location of spot

                cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4) # draws a circle
                cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1) # determining the size f the frame space of frame
                # Display frames and exit
                #       cv2.imshow('light', thr)
        cv2.imshow('frame', frame) # shows frame with newly imposed circle
        cv2.waitKey(4)
        key = cv2.waitKey(1)


    	cv2.imshow('frame',frame)
  	if cv2.waitKey(1) & 0xFF == ord('q'):
        	break

cap.release()
cv2.destroyAllWindows()
