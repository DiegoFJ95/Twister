import serial

ser = serial.Serial(timeout = 100)
ser.baudrate = 115200
ser.port = self.selected_port()
ser.open()
ser.write(b'?C\r') #la b es para decirle que lo pase en ascii
r1 = ser.readline()