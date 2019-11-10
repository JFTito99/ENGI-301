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

import time   #  A library

#For potentiometer
import Adafruit_BBIO.ADC as ADC   #

#For Motor control and RGB Control
import Adafruit_BBIO.PWM as PWM

#For the color sensor
import board
import busio
import adafruit_tcs34725

# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------
ANALOG_INPUT = "P1_19"                      # AIN0

SERVO_OUTPUT = "P1_36"                      # PWM0 A


# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------
debug                   = True    #to turn on and off print statements

# Motor Variables
servo_duty_min          = 0                      # Numbers that just have to get figured out
servo_duty_max          = 100                     # Numbers that just have to get figured out
servo_pwm_frequency     = 100                    # Frequency in Hz   From the datasheet
servo_update_time       = 1                    # Time in seconds

#Color Sensor Variables
sensor = None      #Blank, give us a debuggable error
i2c = None


# ------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------
def setup():
    """Set up the hardware components."""
    global sensor, i2c   #Use global variable for sensor Use what is already previously defined by others
    
    ADC.setup()
    #For Color Sensor
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = adafruit_tcs34725.TCS34725(i2c)
    
# end def


def set_servo_angle(adc_pin, servo_pin):
    """ Set the position of the servo using the ADC input value.
    
    ADC input value of 0 should result in the servo at 0 degrees while
    an ADC input value of 1 should result in the servo at 180 degrees.

    This function will only set the servo angle.  The servo must be
    properly initialized and cleaned up outside this function.    
    """
    servo_duty_span = servo_duty_max-servo_duty_min   #Max value minus min value
    angle           = float(ADC.read(adc_pin))      #Value between 0 and 1 from the potentiometer, instead of 0-4095
    duty            = ((angle * servo_duty_span) + servo_duty_min) 
    
    if (debug):         # Just a way to check when things go wrong
        print("angle = {0}; duty = {1}".format(angle, duty))

    PWM.set_duty_cycle(servo_pin, duty)

# End def


def cleanup():
    """Set up the hardware components."""
    PWM.cleanup()
    i2c.deinit()
# end def


# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    setup()
    print("Servo Control Program Start")
    try:
        while True:
            try:
                PWM.start(SERVO_OUTPUT, (100 - servo_duty_min), servo_pwm_frequency)
        
                while True:
                    set_servo_angle(ANALOG_INPUT, SERVO_OUTPUT)
                    print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes))
                    print('Temperature: {0}K'.format(sensor.color_temperature))
                    print('Lux: {0}'.format(sensor.lux))
                    time.sleep(servo_update_time)
                    
                
            except Exception as e:   #timeout errors for light sensor
                print(e)
                
    except KeyboardInterrupt:       #Control c to end the program
        PWM.stop(SERVO_OUTPUT)
        
    cleanup()
    print("Servo Control Program Finished")



