#!/usr/bin/python2
import RPi.GPIO as GPIO 
import time
import sys
import os

# Definign class used to run the stepper motor
class StepperManual:
    def __init__(self):
	pass
    # Defining delay value in between each bit pattern used 
    # to drive the stepper 
    delay = 4 / 1000.0

    # Defining initial value corresponding to 180 degree point
    initial_val = 257
	
    # Setting up the number of steps made by the stepper motor with each 
    # key press of the right of left arrow keys on the keyboard	
    steps = 25

    # Setting up the Raspberry Pi pins 
    coil_A_1_pin = 31
    coil_A_2_pin = 33
    coil_B_1_pin = 35
    coil_B_2_pin = 37

    # Standard GPIO error codes
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    # Raspberry Pi setup for GPIO pins
    # Pins set as output
    GPIO.setup(coil_A_1_pin, GPIO.OUT)
    GPIO.setup(coil_A_2_pin, GPIO.OUT)
    GPIO.setup(coil_B_1_pin, GPIO.OUT)
    GPIO.setup(coil_B_2_pin, GPIO.OUT)

    # Sets order for steps and activating coils
    def setStep(self, w1, w2, w3, w4):
        GPIO.output(StepperManual.coil_A_1_pin, w1)
        GPIO.output(StepperManual.coil_A_2_pin, w2)
        GPIO.output(StepperManual.coil_B_1_pin, w3)
        GPIO.output(StepperManual.coil_B_2_pin, w4)

    # Forward function definition
    # Inputs to the function include delay value in milliseconds 
    # and the # of steps the stepper motor should take
    def forward(self, delay, steps):
        for i in range(0, steps):
            # moves in sequence specified by activation of coils
            # equivalent to clockwise rotation
            self.setStep(1, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 1)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    # Backwards function definition
    # Inputs to the function include delay value in milliseconds 
    # and the # of steps the stepper motor should take	
    def backwards(self, delay, steps):
        for i in range(0, steps):
            # moves in sequence specified by activation of coils
            # equivalent to counterclockwise rotation
            self.setStep(0, 0, 1, 1)
            time.sleep(delay)
            self.setStep(0, 1, 1, 0)
            time.sleep(delay)
            self.setStep(1, 1, 0, 0)
            time.sleep(delay)
            self.setStep(1, 0, 0, 1)
            time.sleep(delay)

    # Defining function for clearing/stopping stepper
    def clear(self):
        self.setStep(0, 0, 0, 0)


    # Function that writes a list to a text file.
    # This function is used as a means of providing memory to keep 
    # track of the position of the stepper.
    def write_to_temp_file(self, value):
        # Opening/creating temporary text file if it does not exist
        try:
            with open("mem.txt", 'w') as f:
                f.write('%d' % int(value))
        except IOError:

            # Letting the user know that an IO error has occured
            print 'Cannot open storage file for writing'
        else:

            # Closing the opened file
            f.close()


    # Defining function used to change the position of the stepper
    # motor in the forward direction
    def change_position_forward(self):

	# Checking if temporary storage file used to keep track of the 
	# stepper motor position exists 		
        if os.path.isfile('mem.txt'):

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')

            except IOError:

                print 'Cannot open storage file for reading'

            else:
		
		# Obtaining current stepper position 
                current_val = [int(n) for n in fp.read().split()]
		
		# Calculating the new required stepper motor position thereby obtaining the number 
		# of steps that should be taken after a right arrow key press
                required_pos = StepperManual.steps + current_val[0]
		
		# If the next required position causes the stepper motor to spin more than 180 degrees from 
		# the rest/default position (which means required_pos > 514) the stepper motor is turned 
		# backwards thereby pointing to the required position from the opposite side 
                if required_pos > 514: 
		    
                    # Obtaining the number of steps necessary to spin the stepper motor to the required
		    # position from the opposite side
		    step_val = current_val[0] - (required_pos - 514)

		    # Driving the stepper motor	
                    self.backwards(StepperManual.delay, abs(step_val))
                    self.clear()

		    # Closing the temporary storage file that was opened for reading
                    fp.close()

	 	    # Calculating the new current position of the stepper motor after it spinned back 
		    # on itself (position in terms of steps)	
                    new_curr_value = current_val[0] - (current_val[0] - (required_pos - 514))

	            # Writing new stepper position to the temporary storage file
                    self.write_to_temp_file(new_curr_value)

                else:
		    
                    # Driving stepper motor by the specified amount (determined by user input)
                    self.forward(StepperManual.delay, StepperManual.steps)
                    self.clear()
		    
                    # Defining new current position of the stepper motor	
                    val = int(current_val[0]) + int(StepperManual.steps)

                    # Closing the file that was opened for reading
                    fp.close()

		    # Writing new stepper motor position to the temporary storage file
                    self.write_to_temp_file(val)

        else: 
		
	    # Driving stepper motor by the specified amount (determined by user input)
	    # In this case the file storing the current position of the stepper motor
            # does not exit yet	
            self.forward(StepperManual.delay, StepperManual.steps)
            self.clear()

            # Creating a text file with the initial/default position of the stepper motor
            self.write_to_temp_file(StepperManual.initial_val)

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')
            except IOError:

                print 'Cannot open storage file for reading'

            else: 
		
		# Obtaining current stepper posisiton (which in this case is the defualt value)
                current_val = [int(n) for n in fp.read().split()]

		# Defining new current value after the stepper motor has moved from the 
                # the defualt position for the first time 
                val = int(current_val[0]) + int(StepperManual.steps)

                # Closing file that was opened for reading
                fp.close()
		
		# Writing new current value to the temporary storage file
                self.write_to_temp_file(val)


    # Defining function used to change the position of the stepper
    # motor in the backward direction    
    def change_position_backward(self):

	# Checking if temporary storage file used to keep track of the 
	# stepper motor position exists 				
        if os.path.isfile('mem.txt'):

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')

            except IOError:

                print 'Cannot open storage file for reading'

            else: 
		
		# Obtaining current stepper position 
                current_val = [int(n) for n in fp.read().split()] 
               
		# Calculating the new required stepper motor position thereby obtaining the number 
		# of steps that should be taken after a left arrow key press
       	        required_pos = current_val[0] - StepperManual.steps 

		# If the next required position causes the stepper motor to spin more than 180 degrees from 
		# the rest/default position (which means required_pos < 0) the stepper motor is turned 
		# forwards thereby pointing to the required position from the opposite side 
                if required_pos < 0:
		
		    # Obtaining the number of steps necessary to spin the stepper motor to the required
		    # position from the opposite side
                    step_val = 514 - (abs(required_pos) + current_val[0])

		    # Driving the stepper motor	
                    self.forward(StepperManual.delay, abs(step_val))
                    self.clear()

		    # Closing the temporary storage file that was opened for reading
                    fp.close()
	
	    	    # Calculating the new current position of the stepper motor after it spinned forward
		    # on itself (position in terms of steps)		
                    new_curr_val = 514 - abs(required_pos)

		    # Writing new stepper position to the temporary storage file
                    self.write_to_temp_file(new_curr_val)
    

                else:
                    
		    # Driving stepper motor by the specified amount (determined by user input)
                    self.backwards(StepperManual.delay, StepperManual.steps)
                    self.clear()

		    # Defining new current position of the stepper motor	
                    val = int(current_val[0]) - int(StepperManual.steps)

                    # Closing the file that was opened for reading
                    fp.close()

		    # Writing new stepper motor position to the temporary storage file
                    self.write_to_temp_file(val)

        else: 
		
            # Driving stepper motor by the specified amount (determined by user input)
	    # In this case the file storing the current position of the stepper motor
            # does not exit yet	  
            self.backwards(StepperManual.delay, StepperManual.steps)
            self.clear()

            # Creating a text file with the initial/default position of the stepper motor
            self.write_to_temp_file(StepperManual.initial_val)

            try: 
                # Opening storage file for reading
                fp = open("mem.txt", 'r')
            except IOError:

                print 'Cannot open storage file for reading'

            else: 

		# Obtaining current stepper posisiton (which in this case is the defualt value)
                current_val = [int(n) for n in fp.read().split()]

		# Defining new current value after the stepper motor has moved from the 
                # the defualt position for the first time 
                val = int(current_val[0]) - int(StepperManual.steps)

                # Closing the file that was opened for reading
                fp.close()

		# Writing new current value to the temporary storage file
                self.write_to_temp_file(val)



if __name__ == "__main__":
	main()
