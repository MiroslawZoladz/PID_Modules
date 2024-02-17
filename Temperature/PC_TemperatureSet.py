import serial, time
import sys

COM_NR = 2
TEMP = 25.0

if len(sys.argv) == 2:
    TEMP = float(sys.argv[1])
elif len(sys.argv) == 3:
    TEMP = float(sys.argv[2])
    COM_NR = sys.argv[3]
else:
    print("ERROR: missing arguments") 
    sys.exit()

print(f'COMM: {COM_NR}')

try:
    comm = serial.Serial(f'Com{COM_NR}',115200,timeout=1)
except:
    print("ERROR: Can't communicte with module - check comm nr\n")
else:
    try:
        comm.write(f"ts {TEMP}\r\n".encode('UTF-8'))
        _ = comm.readline().decode("utf-8").strip()
        print(_)
        # comm.write("tr\r\n".encode('UTF-8'))        
        # for i in range(2):
        #     _ = comm.readline().decode("utf-8").strip()
        # print(_)
    finally:
        comm.close()
        comm.close
