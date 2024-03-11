import typing
import serial

from PyQt5 import QtWidgets, QtGui, QtCore


from src.gui.widgets.CPanelView import CPanelView



class CPanel( QtWidgets.QWidget, CPanelView ):
    def __init__(self, parent = None, *args ) -> None:
        super().__init__(parent, *args)
        super( QtWidgets.QWidget, self ).__init__()


        self.UnitChangeInThisFrame = True
        # Setup User Interface
        self.setupUI( self )
        self.setCallbacks()
        self.setTimers()

    def CheckConnect ( self ):
        try:
            if self.ports:
                ser = serial.Serial(timeout = 100)
                ser.baudrate = 115200
                ser.port = self.port_selection()
                ser.open()
                ser.write(b'?C\r') #la b es para decirle que lo pase en ascii
                r1 = ser.readline()


                try:
                    r1 = r1[:-2]
                    r1 = r1.split(b" ")
                    r1[0] = float(r1[0])
                    print(r1[0])
                except Exception:
                    r1 = None
                    print("Invalid Port")

                else:
                    self.TorqueUpdate(r1[0])
                    self.GraphUpdate()
                    self.validar_conexion()

                ser.close()

            else:
                print("No device connected")
                #self.port_update   (no funciono)

        except Exception:
            print("Device disconnected")

    def ChangeUnits( self ):
        self.UnitChangeInThisFrame = True



    def setCallbacks( self ):
        self.load_button.clicked.connect( self.CheckConnect) #( self._loadButtonCallback )
        self.update_port_button.clicked.connect( self.port_update)
        self.polling_value.valueChanged.connect(self.PollingRateUpdate)
        self.unit_list.currentTextChanged.connect(self.ChangeUnits)


    def readSensor( self, ser ):
        ser.write(b'?C\r')
        r1 = ser.readline()
        r1 = r1[:-2]
        r1 = r1.split(b" ")
        r1[0] = float(r1[0])
        self.TorqueUpdate(r1[0])

    def run( self ):
        # Esto se ejecuta cada 1000/FPS milisegundos
        if self.ConexionValida == True:
            try:

                ser = serial.Serial(timeout = 100)
                ser.baudrate = 115200
                ser.port = self.port_selection()
                ser.open()
                self.readSensor(ser)

                if self.UnitChangeInThisFrame == True:
                    command = self.UnitsUpdate()
                    if command != False:
                        print("Command:",command)
                        ser.write( bytes(command, "ascii" ) + b"\r\n")
                self.UnitChangeInThisFrame = False

                self.GraphUpdate()

            except Exception:
                self.ConexionValida = False

        DPS = self.GetPollingRate()
        self.pcpm_timer.setInterval( int( 1000 / DPS ) )


    def setTimers( self ):
        #DPS = CONFIG_FILE.get( "Polling_rate" )
        DPS = self.GetPollingRate()
        print("polling rate:", DPS)
        self.pcpm_timer = QtCore.QTimer()
        self.pcpm_timer.setInterval( int( 1000 / DPS ) )
        self.pcpm_timer.timeout.connect( self.run )
        self.pcpm_timer.start()

