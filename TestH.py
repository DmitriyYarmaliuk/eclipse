import cv2
import imutils 

cap = cv2.VideoCapture("/home/pi/Desktop/Test_5_fps_2.h264")
cap.set(cv2.cv.CV_CAP_PROP_FPS,10)

while not cap.isOpened():
    cap = cv2.VideoCapture("/home/pi/Desktop/Test_5_fps_2.h264")
    cv2.waitKey(10)
    print "Wait for the header"

pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
frame_count = 0
while True:
#    flag = cap.grab()	
    flag = cap.grab()
#    _, frame = cap.read()
#   frame = imutils.resize(frame, width=400)
   # flag, frame = cap.read()

    if flag:
	frame_count + frame_count + 1
	print "frame_count:", frame_count 
	if frame_count % 25 == 0:
		print "Inside if"
		_, frame = cap.read()
		frame = imutils.resize(frame, width=400)

        	# The frame is ready and already captured
        	cv2.imshow('video', frame)
        	pos_frame = cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
        print str(pos_frame)+" frames"
    else:
        # The next frame is not ready, so we try to read it again
        cap.set(cv2.cv.CV_CAP_PROP_POS_FRAMES, pos_frame-1)
        print "frame is not ready"
        # It is better to wait for a while for the next frame to be ready
        cv2.waitKey(1000)
	break

    if cv2.waitKey(10) == 27:
        break
    if cap.get(cv2.cv.CV_CAP_PROP_POS_FRAMES) == cap.get(cv2.cv.CV_CAP_PROP_FRAME_COUNT):
        # If the number of captured frames is equal to the total number of frames,
        # we stop
        break
