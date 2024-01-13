from machine import Pin
import onewire, ds18x20, time

ds_pin = Pin(28)
ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
roms = ds_sensor.scan()

print("SN:temp")
for rom in roms:        
    _ = 0;
    for r in rom:
        _ <<= 8
        _ += int(r)            
    ds_sensor.convert_temp()
    time.sleep_ms(750)
    temp = ds_sensor.read_temp(rom)
    print(f'{_:016x}',':', round(temp,1) )#        
print()




    
