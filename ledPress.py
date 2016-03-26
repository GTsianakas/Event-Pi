#This software was created by George Tsianakas giorgostsianakas@hotmail.com and is under GPL v3 licence

#verson 0.1

#thing to be fixed and added soon
#when holding if you press another key the holding stops and you need to press it again to restart
#multiple simultainous inputs of various types

#future
#add support for servos and motors 

import time
import curses
import RPi.GPIO as GPIO

#init curses 
screen = curses.initscr() #get screen
curses.noecho()           #remove echo respond
curses.cbreak()           #real time input (no terminal processing)
screen.keypad(1)          #enable special characters e.g ctrl-c
screen.nodelay(1)         #no enter required for input capture

#fucntions

currentMills = lambda: int(round(time.time()*1000)) # Get current time in miliseconds

#Switches values between true and false for a given pin
def pressEvent(PIN,flag):
    GPIO.output(PIN,not(flag))
    return not(flag)

#should be modified to be used with the milliseconds to remove them from main
def holdEvent(PIN,flag):
    if flag:
        GPIO.output(PIN,True)
    if not(flag):
        GPIO.output(PIN,False)
    
#main loop
def main():

    #set pin mode
    GPIO.setmode(GPIO.BCM)

    #choose pin names
    REDLED = 17
    YELLED = 27

    #set pin input/output mode
    GPIO.setup(REDLED,GPIO.OUT)
    GPIO.setup(YELLED,GPIO.OUT)

    #init variables
    redFlag = False
    yelFlag = False

    # this helps calculate teh release delay because curses doesn't have any release events
    # a more optimal solution should be found or tranfer this to the holdevent function
    startTime = 0
    releaseDelay = 240 #optimal for my situation you might want to change it to get better accuracy but more jittering
    
    while(1):
        try:
            time.sleep(0.01)
            
            # handle input events
            input = screen.getch()

            #example of press event

            if input == ord('r'):
                redFlag = pressEvent(REDLED,redFlag)
        

            #example of hold event
            
            if input == ord('y'):
                yelFlag = True
                startTime = currentMills()
            elif not(input == ord('y')) and (currentMills() - startTime) > releaseDelay:
                yelFlag = False
            holdEvent(YELLED,yelFlag)

            
            #exit
            if input == ord('e'):
                break
        
        except(KeyboardInterrupt): #exit succesfully on keyboard interrupts
            break
        
#exit sequence powers down pins and returns terminal to normal state
def cexit():
    GPIO.cleanup()
    curses.nocbreak()
    screen.keypad(0)
    curses.echo()
    curses.endwin()

#program starts here
main()
cexit()
