# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
LetterWriterThingy I2C Library
--------------------------------------------------------------------------
License:   
Copyright 2019 Jorge Tito

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

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
Software API:

  * update_display(value)
      - Update the value on the display.  Value is based on the words for tempo:
        lento, Andante, Allegro, and Presto
  * 
  
--------------------------------------------------------------------------
Background Information: 
 
  * Using seven-segment digit LED display for Adafruit's HT16K33 I2C backpack:
    * http://adafruit.com/products/878
    * https://learn.adafruit.com/assets/36420
    * https://cdn-shop.adafruit.com/datasheets/ht16K33v110.pdf
    
    * Base code (adapted below):
        * https://github.com/emcconville/HT16K33/blob/master/FourDigit.py
        * https://github.com/emcconville/HT16K33/blob/master/_HT16K33.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/HT16K33.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/Adafruit_LED_Backpack/SevenSegment.py
        * https://github.com/adafruit/Adafruit_Python_LED_Backpack/blob/master/examples/sevensegment_test.py
    Special thanks to Eric Welsh

"""
import os
import Adafruit_BBIO.ADC as ADC   #For the potentiometer


# ------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------

# HT16K33 values
DISPLAY_I2C_BUS              = 2                 # I2C 1  
DISPLAY_I2C_ADDR             = 0x70
DISPLAY_CMD                  = "/usr/sbin/i2cset -y 2 0x70"         

ANALOG_INPUT = "P1_19"                      # AIN0 from potentiometer

# ------------------------------------------------------------------------
# Display Library
# ------------------------------------------------------------------------
HEX_DIGITS                  = [0x3f, 0x06, 0x5b, 0x4f,    # 0, 1, 2, 3
                               0x66, 0x6d, 0x7d, 0x07,    # 4, 5, 6, 7
                               0x7f, 0x6f, 0x77, 0x7c,    # 8, 9, A, b
                               0x39, 0x5e, 0x79, 0x71]    # C, d, E, F
                               
LETTERS_USED                = [0x77, 0x5E, 0x79, 0x38,    # A, d, E, L
                               0x54, 0x73, 0x50, 0x6D,    # n, p, r, s
                               0x78]                      # t

CLEAR_DIGIT                 = 0x7F
POINT_VALUE                 = 0x80

DIGIT_ADDR                  = [0x00, 0x02, 0x06, 0x08]
COLON_ADDR                  = 0x04
                      
HT16K33_BLINK_CMD           = 0x80
HT16K33_BLINK_DISPLAYON     = 0x01
HT16K33_BLINK_OFF           = 0x00
HT16K33_BLINK_2HZ           = 0x02
HT16K33_BLINK_1HZ           = 0x04
HT16K33_BLINK_HALFHZ        = 0x06

HT16K33_SYSTEM_SETUP        = 0x20
HT16K33_OSCILLATOR          = 0x01

HT16K33_BRIGHTNESS_CMD      = 0xE0
HT16K33_BRIGHTNESS_HIGHEST  = 0x0F
HT16K33_BRIGHTNESS_DARKEST  = 0x00



def display_setup():
    """Setup display"""
    # i2cset -y 0 0x70 0x21
    os.system("{0} {1}".format(DISPLAY_CMD, (HT16K33_SYSTEM_SETUP | HT16K33_OSCILLATOR)))
    # i2cset -y 0 0x70 0x81
    os.system("{0} {1}".format(DISPLAY_CMD, (HT16K33_BLINK_CMD | HT16K33_BLINK_OFF | HT16K33_BLINK_DISPLAYON)))
    # i2cset -y 0 0x70 0xEF
    os.system("{0} {1}".format(DISPLAY_CMD, (HT16K33_BRIGHTNESS_CMD | HT16K33_BRIGHTNESS_HIGHEST)))
#end def

def ada_setup():
    #global sensor
    ADC.setup()

def ada_cleanup(self):
    """Set up the hardware components."""
    i2c.deinit()

def display_clear():
    """Clear the display to read '0000'"""
    # i2cset -y 0 0x70 0x00 0x3F
    os.system("{0} {1} {2}".format(DISPLAY_CMD, DIGIT_ADDR[0], HEX_DIGITS[0]))
    # i2cset -y 0 0x70 0x02 0x3F
    os.system("{0} {1} {2}".format(DISPLAY_CMD, DIGIT_ADDR[1], HEX_DIGITS[0]))
    # i2cset -y 0 0x70 0x06 0x3F
    os.system("{0} {1} {2}".format(DISPLAY_CMD, DIGIT_ADDR[2], HEX_DIGITS[0]))
    # i2cset -y 0 0x70 0x08 0x3F
    os.system("{0} {1} {2}".format(DISPLAY_CMD, DIGIT_ADDR[3], HEX_DIGITS[0]))
    
    os.system("{0} {1} {2}".format(DISPLAY_CMD, COLON_ADDR, 0x0))
    
#End def


def display_encode(data, double_point=False):
    """Encode data to TM1637 format.
    
    This function will convert the data from decimal to the TM1637 data fromt
    
    :param value: Value must be between 0 and 15
    
    Will throw a ValueError if number is not between 0 and 15.
    """
    ret_val = 0
    
    try:
        if (data != CLEAR_DIGIT):
            if double_point:
                ret_val = LETTERS_USED[data] + POINT_VALUE
            else:
                ret_val = LETTERS_USED[data]
    except:
        raise ValueError("Digit value must be between 0 and 15.")

    return ret_val

#End def


def display_set(data):
    """Display the data.
    
    data is a list containing 4 values
    """
    for i in range(0,3):
        display_set_digit(i, data[i])
    
#End def


def display_set_digit(digit_number, data, double_point=False):
    """Update the given digit of the display."""
    os.system("{0} {1} {2}".format(DISPLAY_CMD, DIGIT_ADDR[digit_number], display_encode(data, double_point)))    

#End def


def update_display(value):
    """Update the value on the display.  
    
    This function will clear the display and then set the appropriate digits
    
    :param value: Value must be between 0 and 9999.
    
    Will throw a ValueError if number is not between 0 and 9999.
    
    """    
    #dog1 = value  %  10     #Last digit
    #dog2 = (value // 10) % 10    #second to last one
    #dog3 = (value // 100) % 10   #third to last
    #dog4 = (value // 1000) % 10  #first digit
    
    display_set_digit(3, value[3], double_point=False)
    display_set_digit(2, value[2], double_point=False)
    display_set_digit(1, value[1], double_point=False)
    display_set_digit(0, value[0], double_point=False)
    #raise ValueError("Function not implemented.")

#End def



# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    import time

    delay = 1
    
    print("Test HT16K33 Display:")

    display_setup()
    
    Lento   = [3,2,4,8]
    Andante = [0,4,1,0]
    Allegro = [0,3,3,2]
    Presto  = [5,6,2,7]
    #update_display(Lento)
    #time.sleep(delay)
    #update_display(Andante)
    #time.sleep(delay)
    #update_display(Allegro)
    #time.sleep(delay)
    #update_display(Presto)
    #time.sleep(delay)
    
    ada_setup()
    
    
    while True:
        angle  = ADC.read(ANALOG_INPUT) * 100
        if angle < 25:
            value = Lento
        elif (angle>25) and (angle<50):
            value = Andante
        elif (angle>50) and (angle<75):
            value = Allegro
        else:
            value = Presto
        print (value)
        update_display(value)
        time.sleep(delay)
        
    

    

    display_clear()    
    print("Test Finished.")