import Adafruit_BBIO.PWM as PWM
import time
 
red     = "P2_1"
green   = "P2_3"
blue    = "P1_33"
 
PWM.start(red, 0)
PWM.start(blue, 0)
PWM.start(green, 0)

 
def fade(colorA, colorB, ignore_color):
    PWM.set_duty_cycle(ignore_color, 100)
    for i in range(0, 100):
	    PWM.set_duty_cycle(colorA, i)
	    PWM.set_duty_cycle(colorB, 100-i)
	    time.sleep(0.05)
	
while True:
    try:
        fade(red, green, blue)   #Somewhere between red and green
        fade(green, blue, red)   #Somewhere between green and blue
        fade(blue, red, green)   #Somewhere between blue and red
    except KeyboardInterrupt:
        PWM.stop(red, 0)
        PWM.stop(blue, 0)
        PWM.stop(green, 0)