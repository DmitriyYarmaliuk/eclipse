#!/usr/bin/python2
import curses
from StepperManual import StepperManual
from ServoManual import ServoManual


def main():

    # Obtaining the curser screen window
    screen = curses.initscr()

    # Input echoing turned off
    curses.noecho()

    # Setting response to a key press to be immediate 
    # No need to wait/check for enter key
    curses.cbreak()

    # Mapping arrow keys to their corresponding values 
    screen.keypad(True)

    try:
        while True:

            # Obtaining user input 
            char = screen.getch()
            
            # Creating an instance of the StepperManual class which is then used to 
            # control the stepper motor 
            stepper = StepperManual()

            # Creating an instance of the ServorManual class which is then used to 
            # control the servo motor 
            servo = ServoManual()

            # Checking for the 'q' character which signals the program to break out
            # of the while loop and thereby terminate
            if char == ord('q'):
                break

            # Checking if the user pressed the right arrow key
            elif char == curses.KEY_RIGHT:
                
                # Displaying that the right arrow key was pressed 	
                screen.addstr(0, 0, 'right')
              
                # Calling a stepper class method to move the stepper forward
                stepper.change_position_forward()

            # Checking if the user pressed the left arrow key
            elif char == curses.KEY_LEFT:
            
                # Displaying that the left arrow key was pressed
                screen.addstr(0, 0, 'left ')
                
                # Calling a stepper class method to move the stepper backward  		
                stepper.change_position_backward()

            # Checking if the user pressed the up arrow key
            elif char == curses.KEY_UP:

                # Displaying that the up arrow key was pressed	
                screen.addstr(0, 0, 'up   ')
              
                # Calling a servo class method to move the servo upward
                servo.servo_control_up()

            # Checking if the user pressed the down arrow key
            elif char == curses.KEY_DOWN:

                # Displaying that the down arrow key was pressed	
                screen.addstr(0, 0, 'down ')

                # Calling a servo class method to move the servo downward
                servo.servo_control_down()
    finally:

        # Shutting down cleanly
         curses.nocbreak(); screen.keypad(0); curses.echo()
         curses.endwin()

if __name__ == "__main__":
        main()

