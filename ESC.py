# **********************************************************************;
# * Project           : ESC@RPI
# *
# * Program name      : ESC.py
# *
# * Author            : Viacheslav Karpizin, AGTx @instructable.com
# *
# * Date created      : 
# *
# * Purpose           : 
# *
# * Revision History  :
# *
# * Date        Author      Ref    Revision (Date in YYYYMMDD format)
# * 202010    Viacheslav Karpizin      1      original version
# *
# 
#  original version: https://www.instructables.com/Driving-an-ESCBrushless-Motor-Using-Raspberry-Pi/

# Copyright (c) 2020, Viacheslav Karpizin
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# **********************************************************************





import os     #importing os library so as to communicate with the system
import time   #importing time library to make Rpi wait because its too impatient 
os.system ("sudo pigpiod") #Launching GPIO library
time.sleep(1) # As i said it is too impatient and so if this delay is removed you will get an error
import pigpio #importing GPIO library

ESC=4  #Connect the ESC in this GPIO pin 

pi = pigpio.pi();
pi.set_servo_pulsewidth(ESC, 0) 

max_value = 2000 #change this if your ESC's max value is different or leave it be
min_value = 700  #change this if your ESC's min value is different or leave it be
print "For first time launch, select calibrate"
print "Type the exact word for the function you want"
print "calibrate OR manual OR control OR arm OR stop"

def manual_drive(): #You will use this function to program your ESC if required
    print "You have selected manual option so give a value between 0 and you max value"    
    while True:
        inp = raw_input()
        if inp == "stop":
            stop()
            break
		elif inp == "control":
			control()
			break
		elif inp == "arm":
			arm()
			break	
        else:
            pi.set_servo_pulsewidth(ESC,inp)
                
def calibrate():   #This is the auto calibration procedure of a normal ESC
    pi.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        pi.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = raw_input()
        if inp == '':            
            pi.set_servo_pulsewidth(ESC, min_value)
            print "Wierd eh! Special tone"
            time.sleep(7)
            print "Wait for it ...."
            time.sleep (5)
            print "Im working on it, DONT WORRY JUST WAIT....."
            pi.set_servo_pulsewidth(ESC, 0)
            time.sleep(2)
            print "Arming ESC now..."
            pi.set_servo_pulsewidth(ESC, min_value)
            time.sleep(1)
            print "See.... uhhhhh"
            control() # You can change this to any other function you want
            
def control(): 
    print "I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'"
    time.sleep(1)
    speed = 1500    # change your speed if you want to.... it should be between 700 - 2000
    print "Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed"
    while True:
        pi.set_servo_pulsewidth(ESC, speed)
        inp = raw_input()
        
        if inp == "q":
            speed -= 100    # decrementing the speed like hell
            print "speed = %d" % speed
        elif inp == "e":    
            speed += 100    # incrementing the speed like hell
            print "speed = %d" % speed
        elif inp == "d":
            speed += 10     # incrementing the speed 
            print "speed = %d" % speed
        elif inp == "a":
            speed -= 10     # decrementing the speed
            print "speed = %d" % speed
        elif inp == "stop":
            stop()          #going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
		elif inp == "arm":
			arm()
			break	
        else:
            print "WHAT DID I SAID!! Press a,q,d or e"
            
def arm(): #This is the arming procedure of an ESC 
    print "Connect the battery and press Enter"
    inp = raw_input()    
    if inp == '':
        pi.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        pi.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control() 
        
def stop(): #This will stop every action your Pi is performing for ESC ofcourse.
    pi.set_servo_pulsewidth(ESC, 0)
    pi.stop()

#This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.    
inp = raw_input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else :
    print "Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!"
