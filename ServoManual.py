#!/usr/bin/python2

import time
import wiringpi
import os 

class ServoManual:

	def __init__(self,y_raw):
        	self.y_raw = y_raw
        

        # use 'GPIO naming'
	wiringpi.wiringPiSetupGpio()

	# set #18 to be a PWM output
	wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

	# set the PWM mode to milliseconds stype
	wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

	# divide down clock
	wiringpi.pwmSetClock(192)
	wiringpi.pwmSetRange(2000)

	delay_period = 0.01

	angle = 10

	# Side-note 210 is 2.1 ms
	# pulse = 213 (90 degrees to the right from the reference)
	# pulse = 53 (90 degrees to the left from the reference)	
	# pulse = 133 (reference)

	# one degree of movement corresponds to 0.888 ms



	# Function that writes a list to a text file.
        # This function is used as a means of providing memory to keep track of the position of the stepper.
        def write_to_temp_file_servo(self,value):
                # Opening/creating temporary text file if it does not exist
                try:
                        with open("mem2.txt", 'w') as f:
                                f.write('%d' %int(value))
                except IOError:

                        # Letting the user know that an IO error has occured
                        print 'Cannot open storage file for writing'
                else:

                        # Closing the opened file
                        f.close()



	def write_to_temp(value,value2):

        	# Opening/creating temporary text file if it does not exist
        	try:
                	with open("mem2.txt", 'w') as f:
                        	f.write('%d' %int(value))
                        	f.write(" ")
                        	f.write('%d'%int(value2))
        	except IOError:
                	# Letting the user know that an IO error has occured
                	print 'Cannot open storage file for writing'
        	else:

                	# Closing the opened file
                	f.close()
	
	def read_temp():


        	write_to_temp(23,45)
        	with open("mem2.txt", 'r') as fp:
                	current_val = [int(n) for n in fp.read().split()]
        	print "current_val[0]", current_val[0]
        	print "current_val[1]", current_val[1]



	def servo_control_up(self):

                # Checking if text file used for memory by the program exists
                if os.path.isfile('mem2.txt'):

			print "Inside if (mem2.txt) already exists"

                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')

                        except IOError:

                                print 'Cannot open storage file for reading'


			else:

                                current_val = [int(n) for n in fp.read().split()]

#				angle = int((self.y_raw - 150) * 41.4/300)

                                # Pulse width given in millisecond

				required_angle = ServoManual.angle + current_val[0]

				if required_angle > 90:
					required_angle = 90
				      	
			        pulse_width = 133 + int(0.888*required_angle)

                                time.sleep(0.1)
				wiringpi.pwmWrite(18,pulse_width)
                                time.sleep(ServoManual.delay_period)
				print "Angle:",ServoManual.angle
				print "Requried angle:",required_angle
                                fp.close()
                                self.write_to_temp_file_servo(required_angle)
                else:

                        # Creating a text file with the initial/default position of the stepper motor
			print "Inside else"
			self.write_to_temp_file_servo(0)
                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')
                        except IOError:

                                print 'Cannot open storage file for reading'

                        else:
			
				pulse_width = 133 + int(0.888*ServoManual.angle)

             			time.sleep(0.1)
		   		wiringpi.pwmWrite(18,pulse_width)
                		time.sleep(ServoManual.delay_period)


                                # Closing file that was opened for reading
                                fp.close()
                                self.write_to_temp_file_servo(ServoManual.angle)

	def servo_control_down(self):

                # Checking if text file used for memory by the program exists
                if os.path.isfile('mem2.txt'):

			print "Inside if (mem2.txt) already exists"

                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')

                        except IOError:

                                print 'Cannot open storage file for reading'


			else:

                                current_val = [int(n) for n in fp.read().split()]

#				angle = int((self.y_raw - 150) * 41.4/300)

                                # Pulse width given in millisecond

				required_angle = current_val[0] - ServoManual.angle 

				if required_angle < -90:
					required_angle = -90
				      	
			        pulse_width = 133 + int(0.888*required_angle)

                                time.sleep(0.1)
				wiringpi.pwmWrite(18,pulse_width)
                                time.sleep(ServoManual.delay_period)
				print "Angle:",ServoManual.angle
				print "Requried angle:",required_angle
                                fp.close()
                                self.write_to_temp_file_servo(required_angle)
                else:

                        # Creating a text file with the initial/default position of the stepper motor
			print "Inside else"
			self.write_to_temp_file_servo(0)
                        try:
                                 # Opening storage file for reading
                                fp = open("mem2.txt",'r')
                        except IOError:

                                print 'Cannot open storage file for reading'

                        else:
			
				pulse_width = 133 + int(0.888*-ServoManual.angle)

             			time.sleep(0.1)
		   		wiringpi.pwmWrite(18,pulse_width)
                		time.sleep(ServoManual.delay_period)


                                # Closing file that was opened for reading
                                fp.close()
                                self.write_to_temp_file_servo(-ServoManual.angle)


	def move_servo(self):

		print "Y_Poisition", self.y_raw
		
                if self.y_raw >= 150:
			angle = int((self.y_raw - 150) * 41.4/300)
                	# Pulse width given in millisecond
			print "Inside 1st if angle = ",angle
                	pulse_width = 133 + int(0.888*angle)
                        wiringpi.pwmWrite(18,pulse_width)
                        time.sleep(Servo.delay_period)
                elif self.y_raw <= 150:
                        angle = int((self.y_raw - 150) * 41.4/300)
                	# Pulse width given in milliseconds
			print "Inside 2nd if angle = ",angle
                	pulse_width = 133 + int(0.888*angle)
			wiringpi.pwmWrite(18,pulse_width)
                        time.sleep(Servo.delay_period)




if __name__ == "__main__":
        main()


