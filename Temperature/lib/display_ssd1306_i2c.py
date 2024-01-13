import machine
from machine import Pin, SoftI2C

from ssd1306 import SSD1306_I2C
import writer

class Display:
        
    def __init__(self, sda_pin_nr,scl_pin_nr,font_size):
        sda=machine.Pin(sda_pin_nr)
        scl=machine.Pin(scl_pin_nr)
        i2c=SoftI2C(sda=sda, scl=scl, freq=1000000)        
        self._oled = SSD1306_I2C(128, 64, i2c)
        
        self._font_writer = writer.Writer(self._oled,self._get_font(font_size))
                
        self.clear()
    
    def _get_font(self,font_size):
        if font_size == 6:
            import font6 as font
        elif font_size == 10:
            import font10 as font
        elif font_size == 24:
            import freesans24 as font
        elif font_size == 28:
            import freesans28 as font
        elif font_size == 46:
            import freesans46 as font
        else:
            assert False, f"font size {font_size} not found"
        return font
    
    def clear(self):
        self._oled.fill(0)
        self._font_writer.set_textpos(0,0)
        self.nl_flag=False
    
    def println(self,line):
        
        nl = '\n' if self.nl_flag else ''
        self._font_writer.printstring(f"{nl}{line}")
        self.nl_flag = True
        
    def show(self):
        self._oled.show()
        
    def print_list(self,l):    
        self.clear()
        for s in l:
            self.println(s)
        self.show()        