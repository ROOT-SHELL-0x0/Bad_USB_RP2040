import busio
import adafruit_ssd1306
import board
import digitalio as io
import thisbutton as tb
import os
import System 

from SillyOled.sillyoled import SillyOled
from time import sleep



power_pin=io.DigitalInOut(board.GP12)
power_pin.direction=io.Direction.OUTPUT
power_pin.value=True




power_pin_display=io.DigitalInOut(board.GP4)
power_pin_display.direction=io.Direction.OUTPUT
power_pin_display.value=True

gnd_pin=io.DigitalInOut(board.GP5)
gnd_pin.direction=io.Direction.OUTPUT
gnd_pin.value=False

sleep(0.3)



i2c = busio.I2C(board.GP3, board.GP2) # инициализация шины I2C
oled = SillyOled(i2c,128, 64) # инициализация дисплея


#exec(load_gif())

system=System.System(oled)
system.run()





        
        
    





