import serial
import sys

from timescale.crud import create

# global
SERIALPORT = "/dev/tty.usbmodem1302"
# SERIALPORT = "COM6" # Windows
BAUDRATE = 115200

class MBSerial:
    def __init__(self):
        self.ser = serial.Serial()

        self.ser.port       =   SERIALPORT
        self.ser.baudrate   =   BAUDRATE
        self.ser.bytesize   =   serial.EIGHTBITS
        self.ser.parity     =   serial.PARITY_NONE
        self.ser.stopbits   =   serial.STOPBITS_ONE
        self.ser.timeout    =   None # lecture bloquante sur readline
        self.ser.xonxoff    =   False
        self.ser.rtscts     =   False
        self.ser.dsrdtr     =   False
        pass

    def __open(self):
        try:
            self.ser.open()
        except serial.SerialException:
            print(f"Serial {SERIALPORT} port not available")
            sys.exit(1)
    
    def __handle_msg(self, line):
        key, value = line.split(':', 1)
        key = key.strip()
        value = value.strip()
        print(f"Received from micro:bit -> {key} = {value}")
        create(value, key)
    
    def start(self):
        self.__open()

        # Boucle de lecture du port série : lire ligne par ligne pour éviter les fragments JSON
        while self.ser.isOpen() or True:
            line = self.ser.readline().decode(errors="replace").strip()
            if line and ':' in line:
                self.__handle_msg(line)
    
    def send(self, msg):
        self.ser.write(msg.encode())
        print(f"Message <{msg}> sent to micro-controller.")
    
    def close(self):
        self.ser.close()