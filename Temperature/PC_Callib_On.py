import serial, time
import sys

COM_NR = 2

if len(sys.argv) > 1:
    COM_NR = sys.argv[1]

print(f'COMM: {COM_NR}')

try:
    comm = serial.Serial(f'Com{COM_NR}',115200,timeout=1)
except:
    print("ERROR: Can't communicte with module - check comm nr\n")
else:
    try:
        comm.write("cC\r\n".encode('UTF-8'))
        comm.flushOutput()
    finally:
        comm.close()
