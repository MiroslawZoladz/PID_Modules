from machine import Pin
from display_ssd1306_i2c import Display
import onewire, ds18x20, time

SET_TEMP = 25 

ID_l = 0x2826a795f0013c4c,0x2817d395f0013ce4,0x28fb0f8a0d000029

# INITIAALIZAATION

disp = Display(sda_pin_nr=20,scl_pin_nr=21,font_size=10)

# Temp Sensor
ds_pin = Pin(28)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

# Relay
relay=machine.Pin(0,Pin.OUT)
 
# MAIN LOOP

# # Temp service
# roms = ds_sensor.scan()        
# # print('Found DS devices: ', roms)
# while True:
#     for rom in roms:        
#         _ = 0;
#         for r in rom:
#             _ <<= 8
#             _ += int(r)            
#         ds_sensor.convert_temp()
#         time.sleep_ms(750)
#         temp = ds_sensor.read_temp(rom)
#         print(f'{_:016x}',temp )#        
#     print()

#temp Normaal
hardbeet = False

while True:
    
    # te,mperature measurement
    try:
        ds_sensor.convert_temp()    

        T_l = list()
        for id_ in ID_l:
            rom = (id_).to_bytes(8, 'big')
            T_l.append(ds_sensor.read_temp(rom))
    except:
        print('err')
    
    else:
        if T_l[0] > SET_TEMP:
            relay.on()
            rel_state='ON'
        else:
            relay.off()
            rel_state='OFF'
            
        Ts_l = list(map(lambda i:f'{i:0.1f}',T_l))                
            
        print(' '.join(Ts_l),rel_state)            
        
        hardbeet = not hardbeet
        _ = [' |' if hardbeet else '--',]+Ts_l
        disp.print_list(_)
        
        time.sleep_ms(900)

#         time.sleep_ms(250)
#         relay.on()
#         time.sleep_ms(250)
#         relay.off()



    
