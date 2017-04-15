#!/usr/bin/python2

import time
import wiringpi
import os 

# Defining class for autonomous servo control
# Utilizes the GPIO ports on the Raspberry Pi
# Making use of the wiringpi library in order to provide a stable clock 
# which is vital for making pulse width modulation possible
# Do not modify any hardcoded values for controlling the servo motor
class Servo:
	
	# Defining class constructor
	def __init__(self,y_raw):
        	self.y_raw = y_raw

	# Using GPIO naming
	wiringpi.wiringPiSetupGpio()

        # Defining pin 18 of the Raspberry Pi to be a PWM output
	wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

        # Setting the PWM mode to milliseconds
	wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

	# Dividing down clock
	wiringpi.pwmSetClock(192)
	wiringpi.pwmSetRange(2000)

        # Defining delay period (given in milliseconds)
	delay_period = 0.01

        # Defining default servo angle
        default = 0

        # Side-note 210 is 2.1 ms
        # pulse = 213 (90 degrees to the right from the reference)
        # pulse = 53 (90 degrees to the left from the reference)
        # pulse = 133 (reference)

        # one degree of movement corresponds to 0.888 ms


        # Defining a function that writes a list to a text file.
        # This function is used as a means of providing memory to keep track of the position
        # associated with the servo motor.
        def write_to_temp_file_servo(self,value):
                # Opening/creating temporary text file if it does not exist
                try:
                        with open("mem2.txt", 'w') as f:
                                f.write('%d' %int(value))
                except IOError:

                        # Letting the user know that an IO error has occurred
                        print 'Cannot open storage file for writing'
                else:

                        # Closing the opened file
                        f.close()


	# Defining a method that will be utilized to control the position of the servo motor
	def servo_control(self):

                # Checking if text file used for memory by the program exists
                if os.path.isfile('mem2.txt'):

			print "Inside if (mem2.txt) already exists"

                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')

                        except IOError:

                                print 'Cannot open storage file for reading'


			else:
				
				# Obtaining current position of the servo motor
                                current_val = [int(n) for n in fp.read().split()]

				# Calculating the angle of deviation of the brightest object from the center of the frame
				# in terms of the y-axis

			        # Vertical field of view for pi camera: 41.41 degrees +/- 0.11 degrees
        			# Converting pixel value which is the distance from the center pixel (150)
        			# Total number of pixels = 400 x 300
        			# Center = 150

				angle = int((self.y_raw - 150) * 41.41/300)

				# Defining the new angle/position for the servo motor				
				required_angle = angle + current_val[0]

				# Preventing the servo from turning more than 90 degrees from its rest position of 0 degrees
				# since the servo motor in use only has 180 degrees of freedom
				if required_angle > 90:
					required_angle = 90
				elif required_angle < -90:
					required_angle = -90
				
                                # Calculating the required pulse width corresponding to the desired
                                # servo motor angle/position
			        pulse_width = 133 + int(0.888*required_angle)

                                time.sleep(0.1)

                                # Driving the servo motor	
				wiringpi.pwmWrite(18,pulse_width)
                                time.sleep(Servo.delay_period)
				
                              # Helpful debug statements	
			      # print "Angle:",angle
			      # print "Requried angle:",required_angle
		
                                # Closing file that was opened for reading
                                fp.close()

                                # Writing new servo position to temporary storage file				
                                self.write_to_temp_file_servo(required_angle)
                else:

			# Creating a text file with the initial/default position of the servo motor
                        self.write_to_temp_file_servo(Servo.default)

                        try:
                                # Opening storage file for reading
                                fp = open("mem2.txt",'r')

                        except IOError:

                                print 'Cannot open storage file for reading'

                        else:


                                # Calculating the angle of deviation of the brightest object from the center of the frame
                                # in terms of the y-axis

                                # Vertical field of view for pi camera: 41.4 degrees
                                # Converting pixel value which is the distance from the center pixel (150)
                                # Total number of pixels = 400 x 300
                                # Center = 300
		                angle = int((self.y_raw - 150) * 41.41/300)

                                # Preventing the servo from turning more than 90 degrees from its rest position of 0 degrees
                                # since the servo motor in use only has 180 degrees of freedom
                		if angle > 90:
					angle = 90
                		elif angle < -90:
					angle = -90
			
                                # Calculating the required pulse width corresponding to the desired
                                # servo motor angle/position
				pulse_width = 133 + int(0.888*angle)

             			time.sleep(0.1)

				# Driving the servo motor	
		   		wiringpi.pwmWrite(18,pulse_width)
                		time.sleep(Servo.delay_period)

                                # Closing file that was opened for reading
                                fp.close()
			
                                # Writing new servo position to the temporary storage file
                                self.write_to_temp_file_servo(angle)



if __name__ == "__main__":
        main()


