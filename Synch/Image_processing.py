from my_serial import my_serial,read_byte,writeln,read

SYNCHRONIZER_COM = 1
CAMERA_COM = 2

PULSE_DELAY = int((1.9*2500)*10)

sample_ctr = 0

with my_serial(CAMERA_COM) as sr_camera:
    with  my_serial(SYNCHRONIZER_COM) as sr_selector:
        print(read(sr_camera))
        print(read(sr_selector))
        
        last_sample = 1
        stop_bit = 0
        
        while True:
            rcvd_byte = int(read_byte(sr_camera))
            curr_sample = rcvd_byte & 0x1
            if(last_sample == 0 and curr_sample == 1):
                
                timestamp = sample_ctr+PULSE_DELAY                
                writeln(sr_selector, f't {timestamp}')
                print(f'Sample    : {sample_ctr}; Timestamp : {timestamp}',)
                #print(read(sr_selector),'\n')
            last_sample = curr_sample
            sample_ctr += 10

