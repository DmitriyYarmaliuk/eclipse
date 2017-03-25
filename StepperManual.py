# /usr/bin/python2

import RPi.GPIO as GPIO  # GPIO stepper library
import time
import sys
import os


# This class is used to run the stepper motor
# Utilizes the GPIO ports on the Raspberry Pi
# Extra hardware includes a motor driver
# Basic setup and usage of stepper motor
# Do not motify any hardcoded values for controlling the stepper motor
class StepperManual:
    def __init__(self, x_raw, y_raw):
        self.x_raw = x_raw
        self.y_raw = y_raw

    # This delay value is in milliseconds
    delay = 4 / 1000.0
    # Initial value corresponding to 180 degree point
    initial_val = 257
	
    steps = 25

    # Setting up the pins
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
    # Inputs = function, milliseconds to delay, # of steps to take

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
    # Inputs = function, milliseconds to delay, # of steps to take
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

    # function definition for clearing/stopping stepper
    def clear(self):
        self.setStep(0, 0, 0, 0)

    # Command line function for running stepper motor
    def run(self):
        while True:
            # User input for number of steps forward
            self.forward(int(StepperManual.delay) / 1000.0, int(StepperManual.steps)) # calls function to move forward specified number
            self.clear()

    # Function that writes a list to a text file.
    # This function is used as a means of providing memory to keep track of the position of the stepper.
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

    def change_position_forward(self):

		
        if os.path.isfile('mem.txt'):

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')

            except IOError:

                print 'Cannot open storage file for reading'

            else:  # File exists

                current_val = [int(n) for n in fp.read().split()] # reads the current position of the stepper from the file
                required_pos = StepperManual.steps + current_val[0] # calculates new required position
#               print "steps:", StepperManual.steps, "current_val[0]", current_val[0], "required_pos:", required_pos # prints to console


                if required_pos > 514: # moves backwards because to the right of the current position
#                   print "Inside Positive routine"
                    # step_val = 514 - abs(StepperManual.steps)  # Setting the step_val in this manner will cause slight deviation from the reference position (257)
                    #		However, it also adds stability to the operation in that the device will be less prone to rotate back and forth repeatedly
                    #					step_val = 514
		    step_val = current_val[0] - (required_pos - 514)
#                   print "Currenet_val:", current_val[0]
#                   print "requried_pos", required_pos
#		    print "Step value backwards:",step_val
                    self.backwards(StepperManual.delay, abs(step_val))
                    self.clear()
                    fp.close()
#                   print "step_val", step_val
                    new_curr_value = current_val[0] - (current_val[0] - (required_pos - 514))
                    self.write_to_temp_file(new_curr_value)
#                   print "step_val written to text file"

                else: # still at correct position
                    self.forward(StepperManual.delay, StepperManual.steps)
                    self.clear()
                    val = int(current_val[0]) + int(StepperManual.steps)
 #                   print "current val:",current
                    # Closing file that was opened for reading
                    fp.close()
                    self.write_to_temp_file(val)

        else: # text file doesn't exist

            self.forward(StepperManual.delay, StepperManual.steps)
            self.clear()

            # Creating a text file with the initial/default position of the stepper motor
            self.write_to_temp_file(StepperManual.initial_val)

            try: # IO Errors
                # Opening storage file for reading
                fp = open("mem.txt", 'r')
            except IOError:

                print 'Cannot open storage file for reading'

            else: # finds the current position and writes the value to the file

                current_val = [int(n) for n in fp.read().split()]
                val = int(current_val[0]) + int(StepperManual.steps)
#		print "First Initial Value:",val 
                # Closing file that was opened for reading
                fp.close()
                self.write_to_temp_file(val)



    def change_position_backward(self):

		
        if os.path.isfile('mem.txt'):

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')

            except IOError:

                print 'Cannot open storage file for reading'

            else:  # File exists

                current_val = [int(n) for n in fp.read().split()] # reads the current position of the stepper from the file
                required_pos = current_val[0] - StepperManual.steps # calculates new required position
#               print "steps:", StepperManual.steps, "current_val[0]", current_val[0], "required_pos:", required_pos # prints to console

                # Routine to determine which direction it must move
                if required_pos < 0: # moves forward because it is to the left of the current position
#                   print "Inside Negative routine"
                    step_val = 514 - (abs(required_pos) + current_val[0])
#                   print "Currenet_val:", current_val[0]
#                   print "requried_pos", required_pos
#		    print "Step value backwards:",step_val
                    self.forward(StepperManual.delay, abs(step_val))
                    self.clear()
                    fp.close()
#                   print "about to write new current value"
                    new_curr_val = 514 - abs(required_pos)
#                   print "new_curr_value:",new_curr_val
                    self.write_to_temp_file(new_curr_val)
#                   print "finished writing current value:",new_curr_val,"to temporary file"
#                   print "step_val", step_val
    

                else: # still at correct position
                    
                    self.backwards(StepperManual.delay, StepperManual.steps)
                    self.clear()
                    val = int(current_val[0]) - int(StepperManual.steps)
#                   print "val", val
                    # Closing file that was opened for reading
                    fp.close()
                    self.write_to_temp_file(val)

        else: # text file doesn't exist

            self.backwards(StepperManual.delay, StepperManual.steps)
            self.clear()
            # Creating a text file with the initial/default position of the stepper motor
            self.write_to_temp_file(StepperManual.initial_val)

            try: # IO Errors
                # Opening storage file for reading
                fp = open("mem.txt", 'r')
            except IOError:

                print 'Cannot open storage file for reading'

            else: # finds the current position and writes the value to the file

                current_val = [int(n) for n in fp.read().split()]
                val = int(current_val[0]) - int(StepperManual.steps)
#		print "steps:", StepperManual.steps, "current_val[0]", current_val[0]
                # Closing file that was opened for reading
                fp.close()
                self.write_to_temp_file(val)



    def change_position_scan(self):  # scanning algorithm for changing the position

        steps = int(73) # number of steps to scan based on the field of view

        # Negative -- left -- backwards
        if steps < 0:
            self.backwards(int(Stepper.delay) / 1000.0, abs(steps))
            self.clear()

        # Positive -- right -- forward
        elif steps > 0:
            self.forward(int(Stepper.delay) / 1000.0, abs(steps))
            self.clear()

        # Checking if text file used for memory by the program exists
        if os.path.isfile('mem.txt'):

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')

            except IOError:

                print 'Cannot open storage file for reading'

            else:  # found file

                current_val = [int(n) for n in fp.read().split()]
                required_pos = steps + current_val[0] # calculates the next position
                print "steps:", steps, "current_val[0]", current_val[0], "required_pos:", required_pos
                if required_pos < 0: # moves to the left because currently positioned to the right of center
                    print "Inside Negative routine"
                    step_val = 514 # scans entire length of frame
                    self.forward(int(Stepper.delay) / 1000.0, abs(step_val))
                    self.clear()
                    fp.close()
                    print "step_val", step_val
                    self.write_to_temp_file(step_val)
                    print "step_val written to text file"

                elif required_pos > 514: # moves to the right because currently positioned left of center
                    print "Inside Positive routine"
                    step_val = 514
                    #	step_val = required_pos - abs(steps)
                    self.backwards(int(Stepper.delay) / 1000.0, abs(step_val))
                    self.clear()
                    fp.close()
                    print "step_val", step_val
                    new_curr_value = required_pos - 514 # scans entire width
                    self.write_to_temp_file(new_curr_value)
                    print "step_val written to text file"

                else:
                    val = int(current_val[0]) + int(steps)
                    print "val", val
                    # Closing file that was opened for reading
                    fp.close()
                    self.write_to_temp_file(val)

        else:

            # Creating a text file with the initial/default position of the stepper motor
            self.write_to_temp_file(Stepper.initial_val)

            try:
                # Opening storage file for reading
                fp = open("mem.txt", 'r')
            except IOError:

                print 'Cannot open storage file for reading'

            else:

                current_val = [int(n) for n in fp.read().split()]
                val = int(current_val[0]) + int(steps)

                # Closing file that was opened for reading
                fp.close()
                self.write_to_temp_file(val)


    # found the brightest spot and writing to text file
    def return_to_bright_spot(self, position):

        try:
            # Opening storage file for reading
            fp = open("mem.txt", 'r')

        except IOError:

            print 'Cannot open storage file for reading'
        else:
            current_val = [int(n) for n in fp.read().split()]
            val = int(current_val[0])
            steps = abs(int(val) - position) # found the number of steps in reference to the frame
            # Closing file that was opened for reading
            self.write_to_temp_file(position) # writes position to fil
            fp.close()
            if position < val: # moves towards spot
                self.backwards(int(Stepper.delay) / 1000.0, abs(steps))
                self.clear()

            elif position > val: # moves toward spot
                self.forward(int(Stepper.delay) / 1000.0, abs(steps))
                self.clear()

