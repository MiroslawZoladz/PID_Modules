import serial, time
import sys

COM_NR = 2

if len(sys.argv) > 1:
    COM_NR = sys.argv[1]

print(f'COMM: {COM_NR}')

def read_chipboards_sn(COM_NR):
    try:
        comm = serial.Serial(f'Com{COM_NR}',115200,timeout=1)
    except:
        print("ERROR: Can't communicte with module - check comm nr\n")
    else:
        try:
            comm.write("cs\r\n".encode('UTF-8'))
            comm.flushOutput()
            for i in range(2):
                _ = comm.readline().decode("utf-8").strip().replace('\\','').replace('r','').replace('n','').replace("'",'')
            if 'bi' in  _:
                return _.split(';')[1:]
        finally:
            comm.close()
_ = read_chipboards_sn(COM_NR)
if _:
    for i,sn in enumerate(read_chipboards_sn(COM_NR)):
        print(f'{i}: {sn}')
else:
    print(_)