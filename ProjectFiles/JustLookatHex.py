# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Just Look at Hex
--------------------------------------------------------------------------
License:   
Copyright 2019 - Jorge F Tito

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
The most important thing from this code is the hex display function and its use
of libraries

--------------------------------------------------------------------------
Background:
  - https://adafruit-beaglebone-io-python.readthedocs.io/en/latest/ADC.html
  - https://learn.adafruit.com/controlling-a-servo-with-a-beaglebone-black/writing-a-program

"""
import threading    #To make everything work smoothly

import time         #  A library

"For the first thread:"
import Adafruit_BBIO.ADC as ADC   #For the potentiometer
import Adafruit_BBIO.PWM as PWM   #For Motor control
import LetterWrciterThingy as LetterWriterThingy   #Importing the hex control library

"For the second thread:"
import board
import busio
import adafruit_tcs34725 as colorer


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

ANALOG_INPUT = "P1_19"                      # AIN0 from potentiometer
MOTOR_OUTPUT = "P1_36"                      # PWM0 A To the motor

RED     = "P2_1"                            # Where the red PWM output is
GREEN   = "P2_3"                            # Where the green PWM output is
BLUE    = "P1_33"                           # Where the blue PWM output is




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

def ADCsetup():                     #Used to initiate thread
    #global sensor
    ADC.setup()
    #LetterWriterThingy.display_setup()
    #LetterWriterThingy.update_display(0)
    
def PWMcleanup():                   #Used somewhere in the end
    """Set up the hardware components."""
    PWM.cleanup()


"Class Initialization"    
class Motor(threading.Thread):
    # Motor Variables
    motor_duty_min          = 0                      # Numbers that just have to get figured out
    motor_duty_max          = 100                     # Numbers that just have to get figured out
    motor_pwm_frequency     = 100                    # Frequency in Hz   From the datasheet
    motor_update_time       = 1                    # Time in seconds
    

    adcPin   = None    #arg1: adcpin, where the potentiometer is located
    motorPin = None  #arg2: motor Pin
    #import Adafruit_BBIO.ADC as ADC   #For the potentiometer
    
    def __init__(self, adcPin, motorPin):
        """Class initialization method"""
        threading.Thread.__init__(self)
        self.adcPin     = adcPin
        self.motorPin   = motorPin
        return
    
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
            LetterWriterThingy.display_setup()
            LetterWriterThingy.ada_setup()
            
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
    #Define arguments
    i2c = None
    sensor = None
    RED = None
    GREEN = None
    BLUE = None
    
    def __init__(self, RED, GREEN, BLUE):
        """Class initialization method"""
        threading.Thread.__init__(self)
        
        self.RED = RED
        self.GREEN = GREEN
        self.BLUE = BLUE
        
        # self.i2c = busio.I2C(board.SCL, board.SDA)
        # self.sensor = colorer.TCS34725(self.i2c)
        return
    
    def read_Color_In(self):
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.sensor = colorer.TCS34725(self.i2c)
        
        red, green, blue = self.sensor.color_rgb_bytes
        Colors = [red,green,blue]      #Vectorized to use in for loops

        PWM.set_duty_cycle(self.RED, 100-Colors[0])   # Red
        PWM.set_duty_cycle(self.GREEN, 100-Colors[1])   # Green
        PWM.set_duty_cycle(self.BLUE, 100-Colors[2])   # Blue
        print("REd, GrEeN, BlUe")
        
    def sing_Fool(self):
        print("I'm Singing")
        
    def cleanup(self):
        """Set up the hardware components."""
        i2c.deinit()
            
    def run(self):
        
        PWM.start(self.RED, 0, 100)
        PWM.start(self.BLUE, 0, 100)
        PWM.start(self.GREEN, 0, 100)
            
        while True:
            try:
                time.sleep(1)
                self.read_Color_In()
                self.sing_Fool()
                
            except Exception as e:
                print(e)
            
        PWM.stop(self.RED)
        PWM.stop(self.BLUE)
        PWM.stop(self.GREEN)

# end def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':

    ADCsetup()
    LetterWriterThingy.ada_setup()

    t1 = Motor(adcPin = ANALOG_INPUT, motorPin= MOTOR_OUTPUT)
    t2 = Color_Sensor_Class(RED = RED, GREEN = GREEN, BLUE = BLUE)

    """
    Issues with starting both notes at the same time
    """
    
    # t1.start()   #Function call so open and close those parentheses
    t2.start()
    
    try:
        main_thread = threading.currentThread()
        for t in threading.enumerate():
            if t is not main_thread:
                t.join()   #Wait for thread to finish
                
    except KeyboardInterrupt:
        PWM.stop(MOTOR_OUTPUT)
        PWM.stop(RED)
        PWM.stop(BLUE)
        PWM.stop(GREEN)
        
        
    LetterWriterThingy.ada_cleanup()
    t2.cleanup()
    PWMcleanup()



