
#Documentation at:
# Pyserial:                         https://pythonhosted.org/pyserial/
# Sensor manual and instructions:   https://mark-10.com/downloads/product-downloads/manualM7I.pdf
# Mark-10 drivers:                  https://mark-10.com/resources/software-drivers/
# Pyqt5:                            https://doc.qt.io/qtforpython-5/quickstart.html

import serial

ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM3'
ser.open()
ser.write(b'LBIN\r') #la b es para decirle que lo pase en ascii       #NM, LBFT, NCM, LBIN, OZIN
#r1 = ser.readline()
#print(r1)

ser.close()

"""with serial.Serial( "COM1", 115200 ) as ser:
    ser.write( b"?C\r" )
    print( ser.read() )"""
