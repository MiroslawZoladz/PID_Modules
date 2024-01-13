from display_ssd1306_i2c import Display
from machine import Pin
import time

disp = Display(sda_pin_nr=20,scl_pin_nr=21,font_size=6)

for j in range(3):
    disp.clear()
    for i in range(10):
        disp.println(f"{j}_{i}")
    disp.show()
    time.sleep(1)        


