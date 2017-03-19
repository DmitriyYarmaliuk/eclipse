# import libs
import cv2
#import numpy as np
import time

# begin streaming
# Creating a VideoCapture object while also specifying which camera will be used for the purpose
# of capturing the video using hte input parameter 0.
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    _, frame = cap.read()

    # Converting captured frame to monochrome
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("gray",gray)
    # Blurring the image using the GaussianBlur() method of the opencv object
    blur = cv2.GaussianBlur(gray, (59, 59), 0)
    cv2.imshow("blur", blur)
    copy =  frame.copy()
    # Using an opencv method to identify the threshold intensities and locations
    (darkest_value, brightest_value, darkest_loc, brightest_loc) = cv2.minMaxLoc(blur)
    #print "brightest Value:", brightest_value-200

    # Threshold the blurred frame accordingly
    # First argument is the source image, which is the grayscale image. Second argument is the threshold value
    # which is used to classify the pixel values. Third argument is the maxVal which represents the value to be given
    # if pixel value is more than (sometimes less than) the threshold value
    cv2.imshow('blur',blur)
    out2, threshold2 = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    out, threshold = cv2.threshold(blur, brightest_value - 10, 230, cv2.THRESH_BINARY)
 #   print "Threshold:", out2
    thr = threshold.copy()
    # Resize frame for ease
    # cv2.resize(thr, (300, 300))
    # Find contours in thresholded frame
    edged = cv2.Canny(threshold, 50, 150)
    cv2.imshow('theshold', threshold)
    cv2.imshow('edged', edged)

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
        if radius < 60:
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
        if cv2.contourArea(maxcontour) :
            (x, final_y), radius = cv2.minEnclosingCircle(maxcontour)
            print "Second Time-----","x:", x, "final value", final_y, "radius", radius
            cv2.circle(frame, (int(x), int(final_y)), int(radius), (0, 255, 0), 4)
            cv2.rectangle(frame, (int(x) - 5, int(final_y) - 5), (int(x) + 5, int(final_y) + 5), (0, 128, 255), -1)
            # Display frames and exit
    cv2.imshow('light', thr)
    cv2.imshow('frame', frame)
    cv2.waitKey(1)
    key = cv2.waitKey(1)


cap.release()
cv2.destroyAllWindows()



