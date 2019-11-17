# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Servo Control using a Potentiometer
--------------------------------------------------------------------------
License:   
Copyright 2019 - <NAME>

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, 
this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
Control a servo using a potentiometer

  - Potentiometer connected to AIN0 (P1_19)
  - Servo Connected to PWM (P1_36)

When potentiometer is changed, this will change the corresponding servo location

--------------------------------------------------------------------------
Background:
  - https://adafruit-beaglebone-io-python.readthedocs.io/en/latest/ADC.html
  - https://learn.adafruit.com/controlling-a-servo-with-a-beaglebone-black/writing-a-program

"""
import threading    #To make everything work smoothly

import time         #  A library

import Adafruit_BBIO.ADC as ADC   #For the potentiometer
import Adafruit_BBIO.PWM as PWM   #For Motor control and RGB Control

import LetterWriterThingy as LetterWriterThingy   #Importing the Code
#For the color sensor
#import board
#import busio
#import adafruit_tcs34725

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

ANALOG_INPUT = "P1_19"                      # AIN0 from potentiometer
MOTOR_OUTPUT = "P1_36"                      # PWM0 A To the motor




# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
debug                   = True    #to turn on and off print statements



#Color Sensor Variables
#sensor = None      #Blank, give us a debuggable error
#i2c = None


# ------------------------------------------------------------------------
# Functions/Objects
# ------------------------------------------------------------------------
#def setup():
#    """Set up the hardware components."""
 #   #global sensor, i2c   #Use global variable for sensor Use what is already previously defined by others
  #  
   # global sensor
    #
    #ADC.setup()
    #For Color Sensor
    #i2c = busio.I2C(board.SCL, board.SDA)
    #sensor = adafruit_tcs34725.TCS34725(i2c)
    
# end def

#"This is the motor class"
#"Contains: set_motor_speed, hexDisplay

def setup():
    #global sensor
    ADC.setup()
    #LetterWriterThingy.display_setup()
    #LetterWriterThingy.update_display(0)
    
def cleanup():
    """Set up the hardware components."""
    PWM.cleanup()


"Class Initialization"    
class Motor(threading.Thread):
    adcPin   = None    #arg1: adcpin, where the potentiometer is located
    motorPin = None  #arg2: motor Pin
    #import Adafruit_BBIO.ADC as ADC   #For the potentiometer
    
    def __init__(self, adcPin, motorPin):
        """Class initialization method"""
        threading.Thread.__init__(self)
        self.adcPin     = adcPin
        self.motorPin   = motorPin
        return
    
    #sensor = None
    
    # Motor Variables
    
    motor_duty_min          = 0                      # Numbers that just have to get figured out
    motor_duty_max          = 100                     # Numbers that just have to get figured out
    motor_pwm_frequency     = 100                    # Frequency in Hz   From the datasheet
    motor_update_time       = 1                    # Time in seconds
    
    #Sets up the ADC sensor :)
    
    
    
    def set_motor_speed(self):
        motor_duty_span = self.motor_duty_max - self.motor_duty_min   #Max value minus min value
        angle           = float(ADC.read(self.adcPin))      #Value between 0 and 1 from the potentiometer, instead of 0-4095
        duty            = ((angle * motor_duty_span) + self.motor_duty_min)
        print(angle)
        PWM.set_duty_cycle(self.motorPin, duty)   #Outputs stuff to the motor
        #print("Run Run as fast as you can you")
        
    def hexDisplay(self):
        Lento   = [3,2,4,8]
        Andante = [0,4,1,0]
        Allegro = [0,3,3,2]
        Presto  = [5,6,2,7]
        angle           = ADC.read(self.adcPin) * 100
        if angle < 25:
            value = Lento
        elif (angle>25) and (angle<50):
	        value = Andante
        elif (angle>50) and (angle<75):
            value = Allegro
        else:
            value = Presto
            
        LetterWriterThingy.update_display(value)
        print("double double toil and trouble")
        

    
    #What this thread is supposed to do
    def run(self):
        
        try:
            PWM.start(self.motorPin, (100 - self.motor_duty_min), self.motor_pwm_frequency)
            while True:
                #self.set_motor_speed()
                time.sleep(self.motor_update_time)
                self.hexDisplay()
        except KeyboardInterrupt:       #Control c to end the program
            PWM.stop(self.motorPin)
        return
        


"This is the color sensor class"
"Contains:"
class Color_Sensor_Class(threading.Thread):
    def __init__(self):
        """Class initialization method"""
        threading.Thread.__init__(self)
        #self.arg   = arg
        return
    def read_Color_In(self):
        print("REd, GrEeN, BlUe")
        
    def sing_Fool(self):
        print("I'm Singing")
        
    def show_Colors(self):
        print("Purdyyyyy")
        
    def cleanup(self):
        """Set up the hardware components."""
        i2c.deinit()
            
    def run(self):
        print("something")
        self.read_Color_In()
        self.sing_Fool()
        self.show_Colors()



# end def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    setup()
    LetterWriterThingy.ada_setup
    t1 = Motor(adcPin = ANALOG_INPUT, motorPin= MOTOR_OUTPUT)
    t2 = Color_Sensor_Class()
    t1.start()   #Function call so open and close those parentheses
    t2.start()
    
    try:
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()   #Wait for thread to finish
    except KeyboardInterrupt:
        PWM.stop(MOTOR_OUTPUT)
    LetterWriterThingy.ada_cleanup
        
    
    
    
    print("Servo Control Program Finished")
    cleanup()



