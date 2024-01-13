import contextlib,serial

@contextlib.contextmanager
def my_serial(com_nr):
    with serial.Serial(port = "COM"+str(com_nr), baudrate=115200, bytesize = 8, timeout = None, stopbits=serial.STOPBITS_ONE) as sr:
        yield sr

@contextlib.contextmanager        
def my_serial_9600(com_nr):
    with serial.Serial(port = "COM"+str(com_nr), baudrate=9600, bytesize = 8, timeout = None, stopbits=serial.STOPBITS_ONE) as sr:
        yield sr
        
def write(sr, msg):
    sr.write((msg).encode('utf-8'))
    
def writeln(sr, msg):
    sr.write((msg+'\n').encode('utf-8'))
    
def read(sr):
    return sr.readline().decode('utf-8').strip().strip() 

def read_byte(sr):
    return sr.read().decode('utf-8')