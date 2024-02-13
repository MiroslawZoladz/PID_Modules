from machine import Pin, UART
from display_ssd1306_i2c import Display
import onewire, ds18x20 

from time import sleep
import _thread

set_temp_l = 25
temp_str_l = None

try: 
    with open('set-temp.txt','r') as f:
        set_temp_l = float(f.read())
except:
       set_temp_l = 25

def temp_stab_thread():
    global lock, temp_str_l, set_temp_l
    hardbeet = False

    # Temp Sensor
    # 8-chip:  0x2826a795f0013c4c, 0x2817d395f0013ce4, 0x28fb0f8a0d000029
    # 32-chip: 0x28aba78a0d00000a,0x28dc5a95f0013cbb,0x2865ca95f0013c9d,0x28d3f395f0013c5f
    ID_l = 0x2826a795f0013c4c, 0x2817d395f0013ce4, 0x28fb0f8a0d000029
    ds_pin = Pin(28)
    ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))

    # Relay
    relay=machine.Pin(0,Pin.OUT)
    
    # Display
    disp = Display(sda_pin_nr=20,scl_pin_nr=21,font_size=10)
    
    # read set_temp

        
    while True:
        
        try:
            ds_sensor.convert_temp()    

            T_l = list()
            for id_ in ID_l:
                rom = (id_).to_bytes(8, 'big')
                T_l.append(ds_sensor.read_temp(rom))
        except:
            lock.acquire()
            temp_str_l = 'error'
            lock.release()
        
        else:
            lock.acquire()
            t = set_temp_l
            lock.release()            
            if T_l[0] > t:
                relay.on()
                rel_state='ON'
            else:
                relay.off()
                rel_state='OFF'
            
            Ts_l = list(map(lambda i:f'{i:0.1f}',T_l))                            
            _t  = 'MSR: '+' '.join(Ts_l)
            _r  = f"REL:{rel_state}"
            _st = f"SET:{set_temp_l}"
            lock.acquire()
            temp_str_l = f'{_st}, {_t}, {_r}'
            lock.release()
            
            hardbeet = not hardbeet
            _ = [f'set: {set_temp_l}', '--'.join(Ts_l), f'cool: {rel_state}'.lower()+' '+(' |' if hardbeet else '--')]
            disp.print_list(_)
                                                            
            sleep(1)
  
def comm_thread():
    global lock, temp_str_l, set_temp_l
    
    uart = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5),timeout = 2, timeout_char = 2) # 2 dni
    
    while True:
        _ = None
        il = input().split()
        #print('cmd:',il)
        try:
            if il[0]=='tr':
                lock.acquire()
                if temp_str_l:
                    print(temp_str_l)
                lock.release() 
            elif il[0]=='ts' and len(il)==2:
                _ = float(il[1].strip().strip('.'))
                f =open('set-temp.txt','w')
                f.write(str(_))
                f.close()
                lock.acquire()
                set_temp_l = _
                lock.release()
            elif il[0]=='cs':
                uart.write("s\n")
                r = uart.readline()
                print(r)
            elif il[0]=='ct':
                uart.write("t\n")
                r = uart.readline()
                print(r)
            elif il[0]=='cr':
                uart.write("r\n")
                r = uart.readline()
                print(r)
            elif il[0]=='cC':
                uart.write("C\n")
                r = uart.readline()
                print(r)
            elif il[0]=='cc':
                uart.write("c\n")
                r = uart.readline()
                print(r)
            else:
                raise Exception()
        except:
            print('error command decoding')
        
        if _:
            print(_)

             
# create a global lock
lock = _thread.allocate_lock()
 
second_thread = _thread.start_new_thread(temp_stab_thread , ())
comm_thread()