from machine import Pin, UART
import time

uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5),timeout = 5000, timeout_char = 5000) # 2 dni

while True:
    input()
    print('reading SN')
    uart.write("s\n")
    r = uart.readline()
    print(r)



