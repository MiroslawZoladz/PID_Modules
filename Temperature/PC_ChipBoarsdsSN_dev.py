import serial, time
import sys

COM_NR = 2

try:
    comm = serial.Serial(f'Com{COM_NR}',115200,timeout=2)
except:
    print("ERROR: Can't communicte with module - check comm nr\n")
else:
    try:
        comm.write("cs\r\n".encode('UTF-8'))
        # comm.flushOutput()
        _ = comm.readline()
        print(_)
    finally:
        comm.close()
            
