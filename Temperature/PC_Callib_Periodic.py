import serial, time
import sys

COM_NR = 2
print(f'Started')

try:
    comm = serial.Serial(f'Com{COM_NR}',115200,timeout=1)
except:
    print("ERROR: Can't communicte with module - check comm nr\n")
else:
    try:
        while(True):
            comm.write("cC\r\n".encode('UTF-8'))
            comm.flushOutput()
            for i in range(2):
                _ = comm.readline()
                
            time.sleep(0.1)
            
            comm.write("cc\r\n".encode('UTF-8'))
            comm.flushOutput()
            for i in range(2):
                _ = comm.readline()
            
            time.sleep(0.4)
    except:
        print("Stopped")            
    finally:
        comm.close()
