from serial.tools import list_ports

for port, desc, _ in list_ports.comports():
    print("{}".format(port))
