import machine
from machine import Pin, SoftI2C

sda=machine.Pin(20)
scl=machine.Pin(21)
i2c=SoftI2C(sda=sda, scl=scl, freq=1000000)

_ = i2c.scan()
print(_)


