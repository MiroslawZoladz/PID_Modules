from machine import Pin
from display import Display
import onewire, ds18x20, time

# Display
sda=machine.Pin(20,pull=Pin.PULL_UP)
scl=machine.Pin(21,pull=Pin.PULL_UP)
i2c=machine.I2C(0, sda=sda, scl=scl, freq=100000)
display = Display(i2c)
display.rows_l(('R0','R1','R2','R3'))


# Temp Sensor
ds_pin = Pin(28)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()        
# print('Found DS devices: ', roms)
ID_l = (0x28aba78a0d00000a,0x28dc5a95f0013cbb,0x2865ca95f0013c9d,0x28d3f395f0013c5f)

# Relay
relay=machine.Pin(0,Pin.OUT)
relay.on()

while True:
    ds_sensor.convert_temp()
    time.sleep_ms(750)
 
#     # service
#     for rom in roms:
#         _ = 0;
#         for r in rom:
#             _ <<= 8
#             _ += int(r)        
#         print(f'{_:016x}', ds_sensor.read_temp(rom))#
#     print()

# normal
    T_sl = list()
    for id_ in ID_l:
        rom = (id_).to_bytes(8, 'big')
        T = ds_sensor.read_temp(rom)
        T_sl.append(f'{T:0.1f}')
    display.rows_l(T_sl)
    for s in T_sl:
        print(s,' ',end='')
    print()
    

##### MAPOWANIE ########
# pozycja od wejscia: pozycja na liscie: ID
# 0:0:28aba78a0d00000a
# 1:3:28dc5a95f0013cbb
# 2:2:2865ca95f0013c9d
# 3:1:28d3f395f0013c5f
