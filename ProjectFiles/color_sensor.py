"""
This code was found from the color sensor website
https://learn.adafruit.com/adafruit-color-sensors/downloads

"""
"""
--------------------------------------------------------------------------
Just a color sensor
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

--------------------------------------------------------------------------
Background Information: 
 
  * Using seven-segment digit LED display for Adafruit's HT16K33 I2C backpack:
    * http://adafruit.com/products/878
    * https://learn.adafruit.com/assets/36420
    * https://cdn-shop.adafruit.com/datasheets/ht16K33v110.pdf
    
    * Base code (adapted below):
        * https://learn.adafruit.com/adafruit-color-sensors/downloads
    Special thanks to Eric Welsh

"""
import time
import board
import busio
import adafruit_tcs34725 as colorer
import Adafruit_BBIO.PWM as PWM   #To control the RGB LED

RED     = "P2_1"
GREEN   = "P2_3"
BLUE    = "P1_33"

PWM.start(RED, 0)
PWM.start(BLUE, 0)
PWM.start(GREEN, 0)
# ------------------------------------------------------------------------
# Functions/Objects
# ------------------------------------------------------------------------

def colorSensorReader(RED,GREEN,BLUE):
    i2c = busio.I2C(board.SCL, board.SDA)
    sensor = colorer.TCS34725(i2c)

    dog = sensor.color_rgb_bytes   #dog is a tuple, so the information has to be unpacked
    red,green,blue = dog
    Colors = [red,green,blue]      #Vectorized to use in for loops

    PWM.set_duty_cycle(RED, 100-Colors[0])   # Red      Important to make these opposite, as the light emits what the sensor does not pick up
    PWM.set_duty_cycle(GREEN, 100-Colors[1])   # Green
    PWM.set_duty_cycle(BLUE, 100-Colors[2])   # Blue

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    try:
        while True:
            colorSensorReader(RED,GREEN,BLUE)
            time.sleep(1)
    except KeyboardInterrupt:
        PWM.stop(RED)
        PWM.stop(GREEN)
        PWM.stop(BLUE)
    

#print('Color: ({0}, {1}, {2})'.format(*sensor.color_rgb_bytes)) #Red, Green, and Blue
#print('Temperature: {0}K'.format(sensor.color_temperature))
#print('Lux: {0}'.format(sensor.lux))

